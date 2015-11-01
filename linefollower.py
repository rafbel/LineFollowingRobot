#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import RPi.GPIO as GPIO


# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

leftSensor = 22
rightSensor = 18
middleSensor = 11

enableSensor = 10

lapCounter = 0

servoZero = 400

rightservoMin = 390
rightservoMed = 380
rightservoMax = 370

leftservoMin = 410  # Min pulse length out of 4096
leftservoMed = 420
leftservoMax = 430  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
GPIO.setmode(GPIO.BCM)

GPIO.setup(leftSensor,GPIO.IN)
GPIO.setup(rightSensor,GPIO.IN)
GPIO.setup(middleSensor,GPIO.IN)
GPIO.setup(enableSensor, GPIO.IN)

time.sleep (10)

hitStartLine = False
wasDisabled = True


while (True):
	
	left   = GPIO.input(leftSensor)
	middle = GPIO.input(middleSensor)
	right  = GPIO.input(rightSensor)
	enable = GPIO.input(enableSensor)	

	print 'L:' + str(left) + ' M:' + str(middle) + ' R:' + str(right) + ' E: ' + str(enable)
 
	if enable: 

		if wasDisabled:
			hasntHitFlag = False

		wasDisabled = False

	if not enable:

		print "Disabling"

		pwm.setPWM(1,0,servoZero)
		pwm.setPWM(0,0,servoZero)

		wasDisabled = True		

	elif hasntHitFlag and right:
		pwm.setPWM(1,0,leftservoMin)
		pwm.setPWM(0,0,rightservoMed)
		if middle and right:
			hasntHitFlag = False

	elif hasntHitFlag and left:
		pwm.setPWM(1,0,leftservoMed)
		pwm.setPWM(0,0,rightservoMin)
		if middle and left:
			hasntHitFlag = False	

	elif middle and left and right:
		lapCounter += 1

		if (hitStartLine == False):
			hitStartLine = True
			
			pwm.setPWM(1,0,servoZero)
			pwm.setPWM(0,0,servoZero)			

			time.sleep(2)		

		pwm.setPWM(1,0,leftservoMax)
		pwm.setPWM(0,0,rightservoMax)
	
	elif middle and left:

		pwm.setPWM(1, 0, leftservoMed)
  		pwm.setPWM(0, 0, rightservoMax)
	
	elif left:
		
		pwm.setPWM(1,0,servoZero)
		pwm.setPWM(0,0,rightservoMin)

	elif right and middle:
		
		pwm.setPWM(1,0,leftservoMax)
		pwm.setPWM(0,0,rightservoMed)

	elif right:
		
		pwm.setPWM(1,0,leftservoMin)
		pwm.setPWM(0,0,servoZero)

	elif middle:

		pwm.setPWM(1,0,leftservoMed)
		pwm.setPWM(0,0,rightservoMed)

	else:
		
		pwm.setPWM(1,0,leftservoMin)
		pwm.setPWM(0,0,rightservoMin)

	
 	time.sleep(0.01)
