# fan.py
import RPi.GPIO as GPIO
import time

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BCM)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 

'''
while True:
    temp = int(os.popen("vcgencmd measure_temp").readline().strip()[5:]).replace("'C",""))
    if temp > 90:
        pi_pwm.ChangeDutyCycle(100) #provide duty cycle in the range 0-100
    elif temp > 60:
        pi_pwm.ChangeDutyCycle(50) #provide duty cycle in the range 0-100
    elif temp > 50:
        pi_pwm.ChangeDutyCycle(25) #provide duty cycle in the range 0-100
    else:
        pi_pwm.ChangeDutyCycle(0)
    time.sleep(1)
    '''
    
pi_pwm.ChangeDutyCycle(0)
time.sleep(1)
pi_pwm.ChangeDutyCycle(25)
time.sleep(1)
pi_pwm.ChangeDutyCycle(50)
time.sleep(1)
pi_pwm.ChangeDutyCycle(100)
time.sleep(1)
GPIO.output(ledpin, GPIO.LOW)
