import requests 
import time

url='http://192.168.4.1/control?'

def control(id,ip,vright,vleft):
    res=requests.get(f"http://{ip}/control?id={id}&vright={vright}&vleft={vleft}")
    print(res,vleft,vright)
    
def MagnetOn(id,ip):
    requests.get(url,f"http://{ip}/control?id={id}&magnet=1")

def MagnetOff(id,ip):
    requests.get(url,f"http://{ip}/control?id={id}&magnet=0")

# control(4,200,200)