import os
import time
import signal
import Adafruit_DHT

import requests
import json

from pprint import pprint

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

json_data_file = open("./config/iot-agent.conf.json", "r").read()
iot_conf = json.loads(json_data_file)
pprint(iot_conf)

url = "http://"+iot_conf["host_r"]+":"+iot_conf["port_r"]+iot_conf["remote_r"]
print(url)

print("DHT22 ---to--> Fiware")

try:
    while True:
        print(iot_conf["nombre"])
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            
            Temperatura = "{0:0.1f}".format(temperature, humidity)
            Humedad = "{1:0.1f}".format(temperature, humidity)
            
            print("Temperatura="+Temperatura)
            print("Humedad="+Humedad)

            payloadTem = "t|"+Temperatura
    
            responseTem = requests.request("POST", url, data=payloadTem, headers=iot_conf["headers"], params=iot_conf["querystring"])

           # print(responseTem.text)

            payloadHum = "h|"+Humedad

            responseHum = requests.request("POST", url, data=payloadHum, headers=iot_conf["headers"], params=iot_conf["querystring"])

            # print(responseHum.text)

        else:
            print("Error, al obtener datos del sensor DHT22")

        print("Esperando "+str(iot_conf["time_sleep"])+" segundos...")    
        time.sleep(iot_conf["time_sleep"])

except KeyboardInterrupt:
    print("Se ha interrumpido la ejecución del script...")    

print("Finalizando ...")

   
