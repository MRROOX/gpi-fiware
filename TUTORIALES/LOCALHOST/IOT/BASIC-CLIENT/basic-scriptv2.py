import http.client

conn = http.client.HTTPConnection("localhost")

payload = "t|22|h|34"

headers = {
    'Content-Type': "text/plain",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "546d860d-7d25-4f88-a17f-4056e825066c,e3384371-9107-4fe3-9110-c2092c8de542",
    'Host': "localhost:7896",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "9",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

conn.request("POST", "iot,d", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))