#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import subprocess
 
class keypad():
    # CONSTANTS   
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
     
    ROW = [26,24,22,18]
    COLUMN = [16,21,19]
     
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
     
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > 3:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 2:
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
    attempt = "000"
    passcode = "123"    
    haltcode = "789"
    quitcode = "999"
    led_1 = 13
    led_2 = 7
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
    GPIO.output(led_2,GPIO.HIGH)

    armed = open("armed.txt", "a+")
    armed.write("0")
    armed.close()

    ready = subprocess.Popen("mpg123 ready.mp3", shell=True)
    print "Enter Code"

    while True:
        digit = None
        while digit == None:
            digit = kp.getKey()
     
        attempt = (attempt[1:] + str(digit))  
	if attempt == passcode:
	    print "Turning on alarm"
	    print "30 second until alarm is activiated"
            ready = subprocess.Popen("mpg123 armed.mp3", shell=True)
	    for i in range(0, 180):
	        GPIO.output(led_1,GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(led_1,GPIO.LOW)
		time.sleep(0.1)
    	    armed = open("armed.txt", "r+") 
	    armed.write("1")
	    armed.close()
	    GPIO.output(led_1,GPIO.HIGH)
	    GPIO.output(led_2,GPIO.LOW)
      	if attempt == haltcode:
	    print "Turning off alarm"
            ready = subprocess.Popen("mpg123 disarmed.mp3", shell=True)
    	    armed = open("armed.txt", "r+") 
	    armed.write("0")
	    armed.close()
            GPIO.output(led_2,GPIO.HIGH)
            GPIO.output(led_1,GPIO.LOW)
	if attempt == quitcode:
	    print "Terminating Program"
            ready = subprocess.Popen("mpg123 shutdown.mp3", shell=True)
	    armed = open("armed.txt", "r+")
	    armed.write("2")
	    armed.close()
            GPIO.output(led_1,GPIO.LOW)
            GPIO.output(led_2,GPIO.LOW)
	    break
        time.sleep(0.5)
