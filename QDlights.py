# Python imports
from time import sleep
from threading import Timer
import logging

# 3rd party imports
import RPi.GPIO as GPIO
from phue import Bridge

# module imports

pin1 = 13
pin2 = 15
relay1 = 29
relay2 = 31


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

pin1_state = GPIO.input(pin1)
pin2_state = GPIO.input(pin2)


def switch_light(nr):
    GPIO.output(nr, not GPIO.input(nr))


def my_callback1(channel):
    print("falling edge detected on {0}".format(channel))
    if pin1_state != GPIO.input(pin1):
        print("State changed for {0}".format(channel))


def my_callback2(channel):
    print("falling edge detected on {0}".format(channel))
    if pin2_state != GPIO.input(pin2):
        print("State changed for {0}".format(channel))


GPIO.add_event_detect(pin1, GPIO.FALLING, callback=my_callback1, bouncetime=300)
GPIO.add_event_detect(pin2, GPIO.FALLING, callback=my_callback2, bouncetime=300)

while True:
    try:
        sleep(5)
        print("5 secs waiting")
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit
