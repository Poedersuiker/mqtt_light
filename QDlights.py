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
import datetime
import json

# 3rd party imports
import RPi.GPIO as GPIO
from phue import Bridge

# module imports


logger = logging.getLogger('QDlight')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


file_handler = logging.RotatingFileHandler('QDlight.log', mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

bridge = Bridge('192.168.0.20')
bridge.connect()

openHAB_address = 'http://192.168.0.10:8080'
living_room = 'hue_0220_00178866bda2_3_brightness'
diner_room = 'tradfri_0220_gwa0c9a0677d2f_65540_brightness'
kitchen = 'tradfri_0220_gwa0c9a0677d2f_65541_brightness'
cellar = 'tradfri_0220_gwa0c9a0677d2f_65539_brightness'
upstairs = 'hue_0220_00178866bda2_2_brightness'
balcony_white = 'hue_0220_00178866bda2_1_brightness'
bedroom_white = 'tradfri_0220_gwa0c9a0677d2f_65538_brightness'


sun_last_update = 0  # Day of the month, if changes re-get the sunrise and sunset
sunrise_done = False
sunset_done = False
last_hour = 0

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
    logger.info("Switching light {0}".format(nr))


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


def openHAB_get_sunrise_and_sunset():
    """
    Input from REST API
    yyyy-MM-dd'T'HH:mm:ss.SSSZ    2017-07-01T14:59:55.711+0000

    Removing timezone, and hoping REST and Python use the same Timezone!

    :return:
    sunset and sunrise in Python datetime object
    """

    response = requests.get("{0}/rest/items/{1}".format(openHAB_address, "LocalSun_Set_StartTime"))
    content = json.loads(response.content.decode('utf-8'))
    return_sunset = datetime.datetime.strptime(content['state'], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
    # sunset = sunset - datetime.timedelta(minutes=15)

    response = requests.get("{0}/rest/items/{1}".format(openHAB_address, "LocalSun_Rise_EndTime"))
    content = json.loads(response.content.decode('utf-8'))
    return_sunrise = datetime.datetime.strptime(content['state'], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
    # sunrise = sunrise + datetime.timedelta(minutes=15)

    return return_sunset, return_sunrise


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
            # switch_light(relay1)  ## relay1 is connected to pin8 and timer
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
            logger.info("Living room at {0}%".format(state))

            if state > 25:  # constitutes on
                new_state = "0"
            else:
                new_state = "75"

            openHAB_set_status(living_room, new_state)
            openHAB_set_status(diner_room, new_state)
            openHAB_set_status(kitchen, new_state)

            pin3_state = GPIO.input(pin3)
            logger.info("State changed 3")

        """
        pin4 and pin5 are used as light sensors for the outside lights
        
        if pin4_state != GPIO.input(pin4):
            switch_light(relay4)
            pin4_state = GPIO.input(pin4)
            logger.info("State changed 4")
        if pin5_state != GPIO.input(pin5):
            switch_light(relay5)
            pin5_state = GPIO.input(pin5)
            logger.info("State changed 5")
        """

        if pin6_state != GPIO.input(pin6):
            switch_light(relay6)
            pin6_state = GPIO.input(pin6)
            logger.info("State changed 6")
        if pin7_state != GPIO.input(pin7):
            """
            Front door switch (closest to living room)
            If first floor light is off:
                Turn on the diner room light, cellar and first floor light
            If first floor light is on: 
                Turn off all the lights in the house
            """

            state = openHAB_get_status(upstairs)
            logger.info("Living room at {0}%".format(state))

            if state > 25:
                openHAB_set_status(living_room, '0')
                openHAB_set_status(diner_room, '0')
                openHAB_set_status(cellar, '0')
                openHAB_set_status(kitchen, '0')
                openHAB_set_status(upstairs, '0')
                openHAB_set_status(balcony_white, '0')
                openHAB_set_status(bedroom_white, '0')
            else:
                openHAB_set_status(diner_room, '75')
                openHAB_set_status(cellar, '75')
                openHAB_set_status(upstairs, '75')

            # switch_light(relay7)
            pin7_state = GPIO.input(pin7)
            logger.info("State changed 7")
        if pin8_state != GPIO.input(pin8):
            switch_light(relay1)
            logger.info("Driveway light is {0}".format(GPIO.input(pin4)))
            switch_light(relay8)
            logger.info("Frontdoor light is {0}".format(GPIO.input(pin5)))
            pin8_state = GPIO.input(pin8)
            logger.info("State changed 8")


        """
        Manual switch the lights during daytime. After Sunset and before Sunrise + 15min switch does nothing
        """

        if sun_last_update != datetime.datetime.today().day:
            sunset, sunrise = openHAB_get_sunrise_and_sunset()
            sunrise_done = False
            sunset_done = False
            logger.info("Sunrise and Sunset refreshed ({0}, {1})".format(sunrise, sunset))
            sun_last_update = datetime.datetime.today().day

        logger.debug("Sunset: {0} {1}".format(sunset, datetime.datetime.now() > sunset))
        logger.debug("Sunrise: {0} {1}".format(sunrise, datetime.datetime.now() > sunrise))

        if last_hour != datetime.datetime.now().hour:
            logger.info("----------------------------------------------------------------------------")
            logger.info("Current time: {0}".format(datetime.datetime.now()))
            logger.info("Sunset:       {0}    {1}".format(sunset, datetime.datetime.now() > sunset))
            logger.info("Sunset done:  {0}".format(sunset_done))
            logger.info("Sunrise:      {0}    {1}".format(sunrise, datetime.datetime.now() > sunrise))
            logger.info("Sunrise done: {0}".format(sunrise_done))
            logger.info("----------------------------------------------------------------------------")
            last_hour = datetime.datetime.now().hour

        if not sunset_done:
            if datetime.datetime.now() > sunset:
                if GPIO.input(pin4) or GPIO.input(pin5):
                    logger.info("Sunset trigger")
                    logger.info("Driveway : {0}".format(GPIO.input(pin4)))
                    switch_light(relay1)  # relay driveway
                    logger.info("Turning Driveway light on for sunset")
                    logger.info("Driveway : {0}".format(GPIO.input(pin4)))
                    switch_light(relay8)  # relay front door
                    logger.info("Turning Frontdoor light on for sunset")
                sunset_done = True

        if not sunrise_done:
            logger.debug("Sunrise not done")
            if datetime.datetime.now() > sunrise:  # Sunset in this comparison to make sure the update has
                # changed to the next day.
                logger.info("Sunrise trigger")
                logger.info("Turning Frontdoor and Driveway lights off after sunrise")
                if not GPIO.input(pin4):
                    switch_light(relay1)
                if not GPIO.input(pin5):
                    switch_light(relay8)
                sunrise_done = True

    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit


GPIO.cleanup()           # clean up GPIO on normal exit
