import requests
import time
from threading import Thread
y = []
def ping():
    start = time.time()
    nf = requests.get('http://192.168.105.38:9000/api/ping')
    page = nf.text
    end = time.time()
    y.append(((end - start) * 1000))

y = []
print("starting test")
for i in range(10):
    ping()
print(y)
print('done sleeping')
time.sleep(5)


y = []
print("starting test")
for i in range(10):
    ping()
print(y)
print('done sleeping')
time.sleep(5)

y = []
print("starting test")
for i in range(10):
    ping()
print(y)
print('done sleeping')
time.sleep(5)

print('---- stop ----')
