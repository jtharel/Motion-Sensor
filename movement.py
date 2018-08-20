#!/usr/bin/python

import time
import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)	#BOARD is pin number on Pi

pir_sensor = 12
led_1 = 11
led_2 = 15

def blink(pin1, pin2):
	for i in range(0,5):	
 		GPIO.output(pin1,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(pin2,GPIO.HIGH)
		GPIO.output(pin1,GPIO.LOW)
		time.sleep(1)
		GPIO.output(pin2,GPIO.LOW)
	return

def camera():
	grab_pic = subprocess.Popen("raspistill -o intruder.jpg", shell=True)
#	grab_vid = subprocess.Popen("raspivid -o intruder.h264 -t 10000", shell=True)
#	send_mail = subprocess.Popen("mpack -s \"INTRUDER\" intruder.jpg jtharel@q.com", shell=True)



GPIO.setwarnings(False)
GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)

while True:
    armed = open("armed.txt", "r")
    armed.seek(0, 0)
    status = armed.read(1)
    if status == "1":
        armed.close()
        if GPIO.input(pir_sensor):
            print("MOVEMENT!")
	    alarm = subprocess.Popen("mpg123 alarm.mp3", shell=True)
    	    camera()
	    blink(led_1, led_2)	
	    time.sleep(0.5)
    if status == "2":
        break

