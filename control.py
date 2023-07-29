import requests 
import time

url='http://192.168.4.1/control?'

def control(id,vright,vleft):
    res=requests.get(url+f"id={id}&vright={vright}&vleft={vleft}")
    print(res,vleft,vright)
    
def MagnetOn(id):
    requests.get(url,f"id={id}&magnet=1")

def MagnetOff(id):
    requests.get(url,f"id={id}&magnet=0")