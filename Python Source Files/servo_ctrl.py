import pigpio
import time
import os

# servo pin cfg
servo_pin = 13
global pwm

def servo_init(init_angle):
    os.system('sudo pigpiod')
    global pwm
    # set pin as BCM - Broadcom SoC Channel
    pwm = pigpio.pi()
    pwm.set_PWM_frequency(servo_pin, 50)
    if not pwm.connected:
        print("servo failed")
        exit()
    else:
        # pwm.set_servo_pulsewidth(servo_pin, 500) # set at 90 degree
        # time.sleep(0.5)
        # pulse_width = 500 + (init_angle * 2000 / 180)
        # pwm.set_servo_pulsewidth(servo_pin, pulse_width) # set at 90 degree
        # time.sleep(0.5)
        pass

def rotate(start_angle = 0, end_angle = 180):
    global pwm
    incr = 1
    if end_angle < start_angle:
        incr = -1
    if end_angle > 180:
        end_angle = 181
    elif end_angle < -1:
        end_angle = -1
    for angle in range(start_angle, end_angle, incr):
        pulse_width = 500 + (angle * 2000 / 180)
        pwm.set_servo_pulsewidth(servo_pin, pulse_width)
        time.sleep(0.01)
    return end_angle

def set_angle(angle):
    pulse_width = 500 + (angle * 2000 / 180)
    pwm.set_servo_pulsewidth(servo_pin, pulse_width)
    time.sleep(0.01)

def servo_deinit():
    global pwm
    pwm.hardware_PWM(servo_pin, 50, 0)
    pwm.stop()

#servo_init()
##rotate(0, 180)
#rotate(180, -1)
#rotate(0, 90)
#servo_deinit()






