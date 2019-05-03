# Python imports
from time import sleep
from threading import Timer
import logging

# 3rd party imports
import RPi.GPIO as GPIO
from phue import Bridge

# module imports


logger = logging.getLogger('QDlight')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


pin1 = 3
pin2 = 5
pin3 = 7
pin4 = 11
pin5 = 13
pin6 = 15
pin7 = 19
pin8 = 21

relay1 = 29
relay2 = 31
relay3 = 33
relay4 = 36
relay5 = 35
relay6 = 38
relay7 = 40
relay8 = 37

state_change_time = 0.2

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(relay5, GPIO.OUT)
GPIO.setup(relay6, GPIO.OUT)
GPIO.setup(relay7, GPIO.OUT)
GPIO.setup(relay8, GPIO.OUT)

pin1_state = GPIO.input(pin1)
pin2_state = GPIO.input(pin2)
pin3_state = GPIO.input(pin3)
pin4_state = GPIO.input(pin4)
pin5_state = GPIO.input(pin5)
pin6_state = GPIO.input(pin6)
pin7_state = GPIO.input(pin7)
pin8_state = GPIO.input(pin8)


def switch_light(nr):
    GPIO.output(nr, not GPIO.input(nr))


def my_callback1(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin1_state != GPIO.input(pin1):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay1)


def my_callback2(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin2_state != GPIO.input(pin2):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay2)


def my_callback3(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin3_state != GPIO.input(pin3):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay3)


def my_callback4(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin4_state != GPIO.input(pin4):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay4)


def my_callback5(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin5_state != GPIO.input(pin5):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay5)


def my_callback6(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin6_state != GPIO.input(pin6):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay6)


def my_callback7(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin7_state != GPIO.input(pin7):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay7)


def my_callback8(channel):
    logger.info("falling edge detected on {0}".format(channel))
    sleep(state_change_time)
    if pin8_state != GPIO.input(pin8):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay8)


GPIO.add_event_detect(pin1, GPIO.FALLING, callback=my_callback1, bouncetime=300)
GPIO.add_event_detect(pin2, GPIO.FALLING, callback=my_callback2, bouncetime=300)
GPIO.add_event_detect(pin3, GPIO.FALLING, callback=my_callback3, bouncetime=300)
GPIO.add_event_detect(pin4, GPIO.FALLING, callback=my_callback4, bouncetime=300)
GPIO.add_event_detect(pin5, GPIO.FALLING, callback=my_callback5, bouncetime=300)
GPIO.add_event_detect(pin6, GPIO.FALLING, callback=my_callback6, bouncetime=300)
GPIO.add_event_detect(pin7, GPIO.FALLING, callback=my_callback7, bouncetime=300)
GPIO.add_event_detect(pin8, GPIO.FALLING, callback=my_callback8, bouncetime=300)

while True:
    try:
        sleep(5)
        logger.info("5 secs waiting")
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit
