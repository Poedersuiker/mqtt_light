# Python imports
from time import sleep
# 3rd party imports
import RPi.GPIO as GPIO
# module imports
from MQTTClient import MQTTClient


class mqtt_switch:
    """
    Link between the hardware button and HASS.IO

    GPIO.add_event_detect(io_port, GPIO.BOTH, toggle_self)
    """

    def __init__(self, name, io_port, mqtt_host='localhost', mqtt_port=1883):
        self.name = name
        self.io_port = io_port
        self.state = False
        self.switch_state = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.io_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(io_port, GPIO.BOTH, self.read_switch, bouncetime=50)

        self.mqtt_client = MQTTClient(self.name, mqtt_host, mqtt_port)

    def read_switch(self, msg=""):
        sleep(0.1)
        switch = GPIO.input(self.io_port)
        print("Read switch {0}: {1} {2}".format(msg, self.switch_state, switch))
        if self.switch_state == switch:
            pass
        else:
            self.switch_state = switch
            self.toggle_self(msg)

    def toggle_self(self, msg=""):
        print("Diff switch: {0}".format(msg))
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


if __name__ == '__main__':
    switch1 = mqtt_switch("test1", 16)
    switch2 = mqtt_switch("test2", 18)
