# import os
# import time
# import Adafruit_DHT

import requests
import json
from pprint import pprint

# DHT_SENSOR = Adafruit_DHT.DHT22
# DHT_PIN = 4

json_data_file = open("./config/iot-conf.json", "r").read() # r for reading the file
iot_conf = json.loads(json_data_file)

pprint(iot_conf)

url = "http://"+iot_conf["host_r"]+":"+iot_conf["port_r"]+iot_conf["remote_r"]
print(url)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    
        payloadTem = "temdht22|{0:0.1f}".format(temperature)
  

        responseTem = requests.request("POST", url, data=payloadTem, headers=iot_conf["headers"], params=iot_conf["querystring"])

        print(responseTem.text)

        payloadHum = "humdht22|{1:0.1f}".format(humidity)

        responseHum = requests.request("POST", url, data=payloadHum, headers=iot_conf["headers"], params=iot_conf["querystring"])

        print(responseHum.text)

    else:
        print("Failed to retrieve data from humidity sensor")
    time.sleep(iot_conf["time_sleep"])
   

