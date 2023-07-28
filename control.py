import requests 
import time

url='http://192.168.4.1/control?'

def control(id,vright,vleft,dt):
    requests.get(url+f"id={id}&vright={vright}&vleft={vleft}")
    time.sleep(dt)
    requests.get(url+'stop')