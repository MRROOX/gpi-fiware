import requests

url = "http://10.11.0.107:7896/iot/d"

querystring = {"k":"4jggokgpepnvsb2uv4s40d59ov","i":"DHT22003"}

payload = "t|10|h|30"
headers = {
    'Content-Type': "text/plain",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "898a71a0-0ee3-496a-998b-ee3eb4885342,3ff8a888-6a51-451b-b68d-d257cf34a885",
    'Host': "10.11.0.107:7896",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "11",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
print('Hola Mundo : ')
response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)
