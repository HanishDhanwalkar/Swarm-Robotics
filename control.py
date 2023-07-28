import requests 
import time

url='http://192.168.4.1/control?'

requests.get(url+'right')
time.sleep(2)
requests.get(url+'off')