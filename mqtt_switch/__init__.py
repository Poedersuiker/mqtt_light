# Python imports

# 3rd party imports
import RPi.GPIO as GPIO
# module imports
from mqtt_client import mqtt_client


class mqtt_switch:
    '''
    Link between the hardware button and HASS.IO

    GPIO.add_event_detect(io_port, GPIO.BOTH, toggle_self)
    '''

    def __init__(self, name, io_port, mqtt_host='localhost', mqtt_port=1883):
        self.name = name
        self.io_port = io_port
        self.state = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.add_event_detect(io_port, GPIO.BOTH, self.toggle_self())

        self.mqtt_client = mqtt_client(self.name, mqtt_host, mqtt_port)

    def toggle_self(self):
        if self.state:
            self.switch_off()
        else:
            self.switch_on()

    def switch_off(self):
        self.state = False

    def switch_on(self):
        self.state = True

    def mqtt_receive_message(self, client, userdata, msg):
        print(msg.topic)
        if msg.topic == 'OFF':
            self.switch_off()
        elif msg.topic == 'ON':
            self.switch_on()