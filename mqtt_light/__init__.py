# Python imports
from time import sleep
# 3rd party imports
import RPi.GPIO as GPIO
# module imports
from mqtt_client import mqtt_client


class mqtt_light:
    """
    Software link to the Raspberry pi 8 relay board.
    Relay pins: (relay, chip pin, header pin) -- Init uses header pin number
    1   P5  29
    2   P6  31
    3   P13 33
    4   P16 36
    5   P19 35
    6   P20 38
    7   P21 40
    8   P26 37

    Future:
    - sensor pin for on/off state

    """

    def __init__(self, name, relay, sensor_pin, mqtt_host='localhost', mqtt_port=1883):
        self.name = name
        self.relay = relay
        self.sensor_pin = sensor_pin
        self.light_state = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relay, GPIO.OUT)

        self.mqtt_client = mqtt_client(self.name, mqtt_host, mqtt_port)
