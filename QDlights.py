"""
Quick and Dirty implementation of my home switches.

The Raspberry Pi is connected to a relay board. The rest of the pins are available for input and sensors.

There is an option to connect directly to the Philips Hue Bridge. Or via the REST API from OpenHab. All connections are
hard-coded because this is a Q&D sollution.
"""

# Python imports
from time import sleep
from threading import Timer
import logging
import requests
import json

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

bridge = Bridge('192.168.0.20')
bridge.connect()

openHAB_address = 'http://192.168.0.10:8080'
living_room = 'hue_0220_00178866bda2_3_brightness'
diner_room = 'tradfri_0220_gwa0c9a0677d2f_65540_brightness'
kitchen = 'tradfri_0220_gwa0c9a0677d2f_65541_brightness'
cellar = 'tradfri_0220_gwa0c9a0677d2f_65539_brightness'
upstairs = 'hue_0220_00178866bda2_2_color_temperature'


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

state_change_time = 0.5
bounce_time = 1000

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


def switch_hue(nr):
    bridge.set_light(nr, 'on', not bridge.get_light(nr, 'on'))


def openHAB_get_status(light):
    response = requests.get("{0}/rest/items/{1}".format(openHAB_address, light))
    content = json.loads(response.content.decode("utf-8"))
    state = content["state"]
    return int(state)


def openHAB_set_status(light, state):
    response = requests.post("{0}/rest/items/{1}".format(openHAB_address, light), data=state)


def openHAB_switch_light(light):
    status = openHAB_get_status(light)
    if status == 100:
        state = "0"
    else:
        state = "100"
    openHAB_set_status(light, state)


def my_callback1(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin1_state != GPIO.input(pin1):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay1)


def my_callback2(channel):
    logger.info("detected on {0}".format(channel))
    # sleep(state_change_time)
    if pin2_state != GPIO.input(pin2):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay2)


def my_callback3(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin3_state != GPIO.input(pin3):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay3)


def my_callback4(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin4_state != GPIO.input(pin4):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay4)


def my_callback5(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin5_state != GPIO.input(pin5):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay5)


def my_callback6(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin6_state != GPIO.input(pin6):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay6)


def my_callback7(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin7_state != GPIO.input(pin7):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay7)


def my_callback8(channel):
    logger.info("detected on {0}".format(channel))
    sleep(state_change_time)
    if pin8_state != GPIO.input(pin8):
        logger.info("State changed for {0}".format(channel))
        switch_light(relay8)

"""
GPIO.add_event_detect(pin1, GPIO.BOTH, callback=my_callback1, bouncetime=bounce_time)
GPIO.add_event_detect(pin2, GPIO.BOTH, callback=my_callback2, bouncetime=bounce_time)
GPIO.add_event_detect(pin3, GPIO.BOTH, callback=my_callback3, bouncetime=bounce_time)
GPIO.add_event_detect(pin4, GPIO.BOTH, callback=my_callback4, bouncetime=bounce_time)
GPIO.add_event_detect(pin5, GPIO.BOTH, callback=my_callback5, bouncetime=bounce_time)
GPIO.add_event_detect(pin6, GPIO.BOTH, callback=my_callback6, bouncetime=bounce_time)
GPIO.add_event_detect(pin7, GPIO.BOTH, callback=my_callback7, bouncetime=bounce_time)
GPIO.add_event_detect(pin8, GPIO.BOTH, callback=my_callback8, bouncetime=bounce_time)

while True:
    try:
        sleep(600)
        logger.info("10 minutes waiting over")
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit
"""

bridge.set_light(3, 'on', False)
bridge.get_light(3, 'on')

while True:
    try:
        sleep(0.5)
        if pin1_state != GPIO.input(pin1):
            switch_light(relay1)
            pin1_state = GPIO.input(pin1)
            logger.info("State changed 1")
        if pin2_state != GPIO.input(pin2):
            """
            Toilet, simple if switched then switch the relay
            """
            switch_light(relay2)
            pin2_state = GPIO.input(pin2)
            logger.info("State changed 2")
        if pin3_state != GPIO.input(pin3):
            """
            Switch all the lights in the 'living space' (Kitchen, diner and living room). 
            Check if living room is on, if so turn everything off.
            """

            # switch_light(relay3)
            state = openHAB_get_status(living_room)
            logging.info("Living room at {0}%".format(state))

            if state > 25:  # constitutes on
                new_state = "0"
            else:
                new_state = "75"

            openHAB_set_status(living_room, new_state)
            openHAB_set_status(diner_room, new_state)
            openHAB_set_status(kitchen, new_state)

            pin3_state = GPIO.input(pin3)
            logger.info("State changed 3")
        if pin4_state != GPIO.input(pin4):
            switch_light(relay4)
            pin4_state = GPIO.input(pin4)
            logger.info("State changed 4")
        if pin5_state != GPIO.input(pin5):
            switch_light(relay5)
            pin5_state = GPIO.input(pin5)
            logger.info("State changed 5")
        if pin6_state != GPIO.input(pin6):
            switch_light(relay6)
            pin6_state = GPIO.input(pin6)
            logger.info("State changed 6")
        if pin7_state != GPIO.input(pin7):
            switch_light(relay7)
            pin7_state = GPIO.input(pin7)
            logger.info("State changed 7")
        if pin8_state != GPIO.input(pin8):
            switch_light(relay8)
            pin8_state = GPIO.input(pin8)
            logger.info("State changed 8")
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit


GPIO.cleanup()           # clean up GPIO on normal exit
