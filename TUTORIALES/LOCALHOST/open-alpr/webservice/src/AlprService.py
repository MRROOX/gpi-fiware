import json
import tornado.ioloop
import tornado.web
from tornado import gen
import time
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import threading
import multiprocessing

from pprint import pprint
import requests

from argparse import ArgumentParser

from openalpr import Alpr


HTTP_CODE_BAD_REQUEST = 400

json_data_file = open("/opt/openalprapi/config/alpr-config.json", "r").read()
config_service = json.loads(json_data_file)
pprint(config_service)

if __name__ == "__main__":

    parser = ArgumentParser(description='TrueCar Computer Vision Webservice')

    parser.add_argument("-p", "--port", dest="port", action="store", metavar='port', type=int, required=False, default=8888,
                        help="Port to listen on")

    parser.add_argument("-t", "--threads", dest="threads", action="store", metavar='threads', type=int, required=False, default=2,
                        help="Number of processing threads to handle computer vision jobs.  Should not exceed number of CPU cores")

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help="Show debug output")

    options = parser.parse_args()

    debug = options.debug

    if options.threads > multiprocessing.cpu_count():
        print("Warning, attempting to use %d threads when your system only has %d cores" % (
            options.threads, multiprocessing.cpu_count()))

    executor = ThreadPoolExecutor(options.threads)


class AlprHandler(tornado.web.RequestHandler):

    # Pull the executor into the class
    executor = executor

    alpr_processes = {}

    @gen.coroutine
    def post(self):

        start = time.clock()
        response = {
            'version': 1,
        }

        aplr_fiware_data = {
            'data':{}
        }

        # 
        data_orion = {
            'value': {}
        }

        if 'image' not in self.request.files:
            response['error'] = 'image_missing'
            self.finish(json.dumps(response))
            return

        topn = int(self.get_argument("topn", default=20, strip=True))
        state = self.get_argument("state", default="", strip=True)

        if len(state) > 0 and len(state) != 2:
            self.set_status(HTTP_CODE_BAD_REQUEST)
            response['error'] = 'invalid_state'
            self.finish(json.dumps(response))
            return

        if topn < 0 or topn > 10000:
            self.set_status(HTTP_CODE_BAD_REQUEST)
            response['error'] = 'invalid_topn'
            self.finish(json.dumps(response))
            return

        fileinfo = self.request.files['image'][0]
        jpeg_bytes = fileinfo['body']

        if len(jpeg_bytes) <= 0:
            self.set_status(HTTP_CODE_BAD_REQUEST)
            response['error'] = 'invalid_image_data'
            self.finish(json.dumps(response))
            return

        alpr_results = yield self.alpr_processor(jpeg_bytes, topn, state)

        end = time.clock()
        if debug:
            print("Total POST time: %.2f ms" % ((end - start) * 1000))

        # Data format for Orion Brocker
        data_orion['value']=alpr_results

        aplr_fiware_data['data']=data_orion

        # Send Data To Orion Brocker

        response_orion = requests.request("PATCH", config_service["orion_api"], data=json.dumps(aplr_fiware_data), headers=config_service["headers"])

        self.finish(json.dumps(response_orion.text))

        # self.finish(json.dumps(aplr_fiware_data))
        # self.finish(json.dumps(alpr_results))

    @run_on_executor(executor='executor')
    def alpr_processor(self, image, topn, state):

        thread_id = threading.currentThread().ident

        if thread_id not in self.alpr_processes:
            if debug:
                print("Kicking off new ALPR process")
            self.alpr_processes[thread_id] = Alpr(
                "us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
            self.alpr_processes[thread_id].set_detect_region(True)

        self.alpr_processes[thread_id].set_top_n(topn)
        if state is not None and state != "":
            self.alpr_processes[thread_id].set_default_region(state)

        if debug:
            print("Starting alpr job")
            print("back-queue size: %d" % executor._work_queue.qsize())

            print("args: topn %d, state: %s" % (topn, state))
            print("Thread ID: " + str(threading.currentThread().ident))
        try:
            start = time.clock()
            results = self.alpr_processes[thread_id].recognize_array(image)
            end = time.clock()

            if debug:
                print("ALPR Processing time: %.2f ms" % ((end - start) * 1000))
            return results
        except:
            return {'error': 'alpr_processing_error'}


class InfoHandler(tornado.web.RequestHandler):

    def get(self):

        response = {
            'queue_size': executor._work_queue.qsize(),
            'threads': len(executor._threads)
        }

        self.finish(json.dumps(response))


class HealthcheckHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_status(200)
        self.finish("")


application = tornado.web.Application([
    (r"/v1/identify/plate", AlprHandler),
    (r"/v1/info", InfoHandler),
    (r"/v1/healthcheck", HealthcheckHandler),

])

if __name__ == "__main__":

    print("OpenALPR Web server started on port %d" % (options.port))
    print("Using %d parallel ALPR threads" % (options.threads))
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
