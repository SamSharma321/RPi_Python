# Jarvis_GPIO.py
import RPi.GPIO as GPIO
import time

# Setup GPIO channels
red_line = 2
blue_line = 4
green_line = 3


def led_check():
	GPIO.output(red_line, GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(red_line, GPIO.HIGH)

	GPIO.output(blue_line, GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(blue_line, GPIO.HIGH)
	
	GPIO.output(green_line, GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(green_line, GPIO.HIGH)

def init_gpio():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)  # Using broadcom SoC channels
	GPIO.setup(red_line, GPIO.OUT) # TODO suppress warnings
	GPIO.setup(blue_line, GPIO.OUT)
	GPIO.setup(green_line, GPIO.OUT)

	GPIO.output(red_line, GPIO.HIGH)
	GPIO.output(blue_line, GPIO.HIGH)
	GPIO.output(green_line, GPIO.HIGH)
	
	# check if all colors of LEDs are working fine
	led_check()

def turn_on_led(line1 = False, line2 = False, line3 = False):
	GPIO.output(red_line, GPIO.HIGH)
	GPIO.output(blue_line, GPIO.HIGH)
	GPIO.output(green_line, GPIO.HIGH)
	
	if line1 is True:
		GPIO.output(red_line, GPIO.LOW)
	
	if line2 is True:
		GPIO.output(blue_line, GPIO.LOW)
	
	if line3 is True:
		GPIO.output(green_line, GPIO.LOW)


