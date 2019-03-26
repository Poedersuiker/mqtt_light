# Python imports
from time import sleep
# 3rd party imports
import RPi.GPIO as GPIO
# module imports
from MQTTClient import MQTTClient


class MQTTLight:
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

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relay, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.mqtt_client = MQTTClient(self.name, mqtt_host, mqtt_port)

    def switch_light(self):
        GPIO.output(self.relay, not GPIO.input(self.relay))

    def light_off(self):
        # read state and change if light on
        if self.read_state():
            self.switch_light()

    def light_on(self):
        # read state and change if light off
        if not self.read_state():
            self.switch_light()

    def read_state(self):
        return GPIO.input(self.sensor_pin)

    def send_state(self):
        json = "{state: {0}}".format(self.read_state())
        self.mqtt_client.send_status(json)
