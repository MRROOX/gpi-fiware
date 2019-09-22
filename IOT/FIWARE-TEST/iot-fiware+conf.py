import requests
import json
from pprint import pprint

json_data_file = open("./config/iot-conf.json", "r").read() # r for reading the file
iot_conf = json.loads(json_data_file)

pprint(iot_conf)

url = "http://"+iot_conf["host_r"]+":"+iot_conf["port_r"]+iot_conf["remote_r"]
print(url)

payloadTem = "temdht22|235"

responseTem = requests.request("POST", url, data=payloadTem, headers=iot_conf["headers"], params=iot_conf["querystring"])

print(responseTem.text)

payloadHum = "humdht22|0523"

responseHum = requests.request("POST", url, data=payloadHum, headers=iot_conf["headers"], params=iot_conf["querystring"])

print(responseHum.text)