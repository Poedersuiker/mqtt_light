# Python imports
from time import sleep
import json
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
    RELAY = [False, 29, 31, 33, 36, 35, 38, 40, 37]

    def __init__(self, floor, name, relay, sensor_pin, mqtt_host='localhost', mqtt_port=1883):
        self.name = name
        self.sensor_pin = sensor_pin
        self.set_relay(relay)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relay, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.mqtt_client = MQTTClient(self.name, mqtt_host, mqtt_port)

        self.topic_prefix = 'hassio/light/{0}/{1}/'.format(self.floor, self.name)
        self.set_topic = '{0}{1}'.format(self.topic_prefix, 'set')
        self.state_topic = '{0}{1}'.format(self.topic_prefix, 'state')
        self.config_topic = '{0}{1}'.format(self.topic_prefix, 'config')

        self.capabilities = {}
        self.capabilities["name"] = self.name
        self.capabilities["platform"] = 'mqtt_json'
        self.capabilities["state_topic"] = self.state_topic
        self.capabilities["command_topic"] = self.set_topic
        self.capabilities["brightness"] = "false"
        self.capabilities["effect"] = "false"
        self.capabilities["confg_topic"] = self.config_topic

        self.status = {}
        self.status["brightness"] = 200
        self.status["color_temp"] = 155  # not used
        self.status["color"] = {"r": 255, "g": 255, "b": 255, "x": 0.123, "y": 0.123}  # not implemented
        self.status["effect"] = "solid"
        self.status["transition"] = 2
        self.status["white_value"] = 150

        self.mqtt_client.set_on_connect(self.on_connect)
        self.mqtt_client.set_on_message(self.on_message)
        self.mqtt_client.connect(self.config_topic, self.state_topic, self.set_topic, self.json_config()
                                 , self.json_state())

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
        json = '{state: {0}}'.format(self.read_state())
        self.mqtt_client.send_status(json)

    def set_relay(self, relay_nr):
        if 1 <= relay_nr <= 8:
            self.relay = self.RELAY[relay_nr]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code: '.format(rc))

    def on_message(self, client, userdata, msg):
        print('{0} : {1}'.format(msg.topic, msg.payload))

    def json_config(self):
        return json.dumps(self.capabilities)

    def json_state(self):
        return json.dumps(self.status)
