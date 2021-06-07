#importing important Libraries
import RPi.GPIO as GPIO    
import time                 #importing time 
import requests             #importing requests which is used to coomunicate over the internet

GPIO.setmode(GPIO.BCM)      #Setting up the board to BCM mode
GPIO.setwarnings(False)     #Disabling the warnings


# allocating important pins 
buzzer=23                   #Positive end of the buzzer connected to the pin 23        
pir = 21                    #OUT pin of the PIR motion sensor connected to the pin 21
trigger=15                  #Trigger pin of the HC-SR04 connected to the pin 15 
echo=14                     #Echo pin of the HC-SR04 connected to the pin 15
led=4                       # positive LED is connected to the pin 4 of raspberry pi 

#defining the pins as input or output pins
GPIO.setup(trigger,GPIO.OUT)        
GPIO.setup(led,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(trigger,0)
GPIO.setup(pir,GPIO.IN)



GPIO.output(buzzer,GPIO.LOW)

#function to calculate the distance from the HC-SR04
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

#Firstly the LED is in OFF state 
GPIO.output(led,GPIO.LOW)


#the function for the buzzer
def buzz(times):
    GPIO.output(buzzer,GPIO.HIGH)
    
    time.sleep(times) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    
    time.sleep(times)
    
  #main loop which will always run infinitely until specified otherwise
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
