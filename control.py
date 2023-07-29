import requests 
import time

url='http://192.168.4.1/control?'

def control(id,vright,vleft):
    requests.get(url+f"id={id}&vright={vright}&vleft={vleft}")
    
def MagnetOn(id):
    requests.get(url,f"id={id}&magnet=1")

def MagnetOff(id):
    requests.get(url,f"id={id}&magnet=0")