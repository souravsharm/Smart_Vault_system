#Libraries
import RPi.GPIO as GPIO
import time 
import requests
#Disable warnings (optional)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



buzzer=23
pir = 21
trigger=15
echo=14
led=4
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(trigger,0)
GPIO.setup(pir,GPIO.IN)



GPIO.output(buzzer,GPIO.LOW)
def distCalc():
    GPIO.output(trigger,1)
    time.sleep(0.0001)
    GPIO.output(trigger,0)
    while GPIO.input(echo)==0:
        pass
    start=time.time()
    while GPIO.input(echo)==1:
        pass
    end=time.time()
    
    dist=(end-start)*17000
    return dist
GPIO.output(led,GPIO.LOW)


def buzz(times):
    GPIO.output(buzzer,GPIO.HIGH)
    
    time.sleep(times) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    
    time.sleep(times)
while True:
    
    dist=distCalc()
    print(dist)
    
    if dist < 40.0:
        
        GPIO.output(led,GPIO.HIGH)
        
    if dist > 40.0:
        
        GPIO.output(led,GPIO.LOW)
        
    if dist < 15:
        r = requests.post('https://maker.ifttt.com/trigger/Intruder_detected_in_room/with/key/mfhMGJgQnDi9joXifIlMbFRfg0-nfFBYOvCfIKQ0vqU', params={"value1":"none","value2":"none","value3":"none"})
        
    if GPIO.input(pir)==1:
        
        print("Motion detected in the safe room, Some intruder found!!")
        buzz(1)
        r = requests.post('https://maker.ifttt.com/trigger/Motion_detected_in_safe/with/key/mfhMGJgQnDi9joXifIlMbFRfg0-nfFBYOvCfIKQ0vqU', params={"value1":"none","value2":"none","value3":"none"})
        
        
    if not GPIO.input(pir):
        print("Motion not on")
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(1)
        
GPIO.output(buzzer, GPIO.LOW)
GPIO.cleanup()