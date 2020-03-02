# Python imports
from time import sleep
from threading import Timer
import json
import socket
from uuid import getnode as get_mac
import subprocess
import logging
from uptime import uptime
import signal
import sys
# 3rd party imports
import RPi.GPIO as GPIO
# module imports
from MQTTClient import MQTTClient


class MQTTBoard:
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

    Version 0.1:
    - Create a software switch next to the normal wall switch. Connected through a hotel arrangement.
                /------------------\
       ---(relay)                    (wall switch)----------
                \------------------/

    - MQTT protocol Homie
      https://homieiot.github.io/specification/spec-core-v3_0_1/

    Future:
    - sensor pin for on/off state

    """
    RELAY = [False, 29, 31, 33, 36, 35, 38, 40, 37]
    SENSOR = [False, 3, 5, 7, 11, 13, 15, 19, 21]  # Change to sensor pins
    SENSOR_STATE = [False, None, None, None, None, None, None, None, None]

    def __init__(self, name, mqtt_host='localhost', mqtt_port=1883):
        self.started = 0
        self.stopped = 0

        # MQTT setup
        self.logger = logging.getLogger('MQTTBoard')
        self.logger.setLevel(logging.DEBUG)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)

        self.mqtt_client = MQTTClient(name, mqtt_host, mqtt_port)
        self.logger.info("MQTT connecting to {0}:{1}".format(mqtt_host, mqtt_port))

        self.mqtt_client.set_on_connect(self.mqtt_on_connect)
        self.mqtt_client.set_on_message(self.mqtt_on_message)

        self.mqtt_client.connect()
        self.logger.info("MQTT connected")

        self.mqtt_client.start()

        # GPIO setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RELAY[1], GPIO.OUT)
        GPIO.output(self.RELAY[1], False)
        GPIO.setup(self.RELAY[2], GPIO.OUT)
        GPIO.output(self.RELAY[2], False)
        GPIO.setup(self.RELAY[3], GPIO.OUT)
        GPIO.output(self.RELAY[3], False)
        GPIO.setup(self.RELAY[4], GPIO.OUT)
        GPIO.output(self.RELAY[4], False)
        GPIO.setup(self.RELAY[5], GPIO.OUT)
        GPIO.output(self.RELAY[5], False)
        GPIO.setup(self.RELAY[6], GPIO.OUT)
        GPIO.output(self.RELAY[6], False)
        GPIO.setup(self.RELAY[7], GPIO.OUT)
        GPIO.output(self.RELAY[7], False)
        GPIO.setup(self.RELAY[8], GPIO.OUT)
        GPIO.output(self.RELAY[8], False)

        GPIO.setup(self.SENSOR[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[2], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[3], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[4], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[5], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[6], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[7], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR[8], GPIO.IN, pull_up_down=GPIO.PUD_UP)


        # Publish on MQTT
        self.base_topic = "homie"
        self.device_id = name.replace(' ', '_')  # Use name as device_id. Replacing spaces with underscore
        self.homie = "3.0.1"
        self.name = name
        # self.localip = get_ip()
        # self.mac = get_mac()
        self.fw_name = "RaspiRelayboard"
        self.fw_version = "0.1"
        self.nodes = "light1,light2,light3,light4,light5,light6,light7,light8,switch1,switch2,switch3,switch4,switch5,switch6,switch7,switch8"
        self.implementation = "RaspberryPi"
        self.stats = "uptime,signal,cputemp,cpuload,freeheap,supply"
        self.stats_interval = 60

        self.topic = "{0}/{1}".format(self.base_topic, self.device_id)
        self.logger.info("Using topic {0}".format(self.topic))

        self.mqtt_publish_device()
        self.mqtt_send_stats()
        self.mqtt_send_nodes()

        self.started = 1

        sleep(0.5)
        i = 1
        while i <= 8:
            initial_power_topic = "{0}/light{1}/power".format(self.topic, i)
            self.mqtt_client.publish(initial_power_topic, "false")
            i += 1

        self.mqtt_client.publish(self.topic + "/$state", "ready")

        signal.signal(signal.SIGINT, self.handle_signal)
        self.read_switches()

        self.logger.info("Everything started and running.")

    def mqtt_publish_device(self):
        self.mqtt_client.publish(self.topic + "/$homie", self.homie)
        self.mqtt_client.publish(self.topic + "/$name", self.name)
        # self.mqtt_client.publish(self.topic + "/$localip", self.localip)
        # self.mqtt_client.publish(self.topic + "/$mac", self.mac)
        self.mqtt_client.publish(self.topic + "/$fw/name", self.fw_name)
        self.mqtt_client.publish(self.topic + "/$fw/version", self.fw_version)
        self.mqtt_client.publish(self.topic + "/$nodes", self.nodes)
        self.mqtt_client.publish(self.topic + "/$implementation", self.implementation)
        self.mqtt_client.publish(self.topic + "/$stats", self.stats)

    def mqtt_send_stats(self):
        self.logger.info("Sending stats")
        stats_topic = "{0}/$stats/".format(self.topic)

        self.mqtt_client.publish(stats_topic + "interval", self.stats_interval)

        self.mqtt_client.publish(stats_topic + "uptime", uptime())

        signal = "Not implemented yet"
        self.mqtt_client.publish(stats_topic + "signal", 0)

        cputemp = int(subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])) / 1000
        self.mqtt_client.publish(stats_topic + "cputemp", cputemp)

        cpuload = subprocess.check_output(['cat', '/proc/loadavg']).rstrip()
        self.mqtt_client.publish(stats_topic + "cpuload", cpuload)

        freeheap = subprocess.check_output(['cat', '/proc/meminfo']).decode('utf-8').split('\n')[1].replace(' ', '').split(':')[1][:-2]
        self.mqtt_client.publish(stats_topic + "freeheap", freeheap)

        supply = "Not implemented yet"
        self.mqtt_client.publish(stats_topic + "supply", 0)

        if not self.stopped:  # if not stopped stay alive
            Timer(self.stats_interval - 1, self.mqtt_send_stats).start()

    def mqtt_send_nodes(self):
        i = 1
        while i <= 8:
            self.mqtt_send_light_node(i)
            self.mqtt_send_switch_node(i)
            i += 1

    def mqtt_send_light_node(self, nr):
        self.logger.info("Sending light node {0}".format(nr))
        light_topic = "{0}/light{1}/".format(self.topic, nr)
        self.mqtt_client.publish(light_topic + "$name", "Light{0}".format(nr))
        self.mqtt_client.publish(light_topic + "$type", "light")
        self.mqtt_client.publish(light_topic + "$properties", "power")

        self.mqtt_client.publish(light_topic + "power/$name", "Power light{0}".format(nr))
        self.mqtt_client.publish(light_topic + "power/$settable", "true")
        self.mqtt_client.publish(light_topic + "power/$retained", "true")
        self.mqtt_client.publish(light_topic + "power/$datatype", "boolean")

        if self.started == 0:
            self.mqtt_client.subscribe(light_topic + "power/set")

    def mqtt_send_switch_node(self, nr):
        self.logger.info("Sending switch node {0}".format(nr))
        switch_topic = "{0}/switch{1}/".format(self.topic, nr)
        self.mqtt_client.publish(switch_topic + "$name", "Switch{0}".format(nr))
        self.mqtt_client.publish(switch_topic + "$type", "switch")
        self.mqtt_client.publish(switch_topic + "$properties", "switch")

        self.mqtt_client.publish(switch_topic + "switch/$name", "Switch {0}".format(nr))
        self.mqtt_client.publish(switch_topic + "switch/$settable", "false")
        self.mqtt_client.publish(switch_topic + "switch/$retained", "true")
        self.mqtt_client.publish(switch_topic + "switch/$datatype", "boolean")

    def mqtt_on_connect(self, client, userdata, flags, rc):
        self.logger.info('Connected with result code: '.format(rc))

    def mqtt_on_message(self, client, userdata, msg):
        self.logger.info('{0} : {1}'.format(msg.topic, msg.payload))
        topic = msg.topic.split('/')
        # expecting name like 'light2'
        nr = int(topic[2][5:])
        try:
            if topic[3] == "power" and topic[4] == "set" and msg.payload.decode('utf-8') == "false":
                self.light_off(nr)
                self.logger.info("Trying to turn off light {0}".format(nr))
            elif topic[3] == "power" and topic[4] == "set" and msg.payload.decode('utf-8') == "true":
                self.light_on(nr)
                self.logger.info("Trying to turn on light {0}".format(nr))
            else:
                self.logger.error("Problem with message")
        except Exception as e:
            self.logger.error("Problem {0}".format(e))

    def switch_light(self, nr):
        GPIO.output(self.RELAY[nr], not GPIO.input(self.RELAY[nr]))
        # self.send_state()

    def light_off(self, nr):
        # read state and change if light on
        if self.read_state(nr):
            self.switch_light(nr)

    def light_on(self, nr):
        # read state and change if light off
        if not self.read_state(nr):
            self.switch_light(nr)

    def read_state(self, nr):
        return GPIO.input(self.SENSOR[nr])

    def handle_signal(self, signal, frame):
        print("Program signal: {0}, {1}".format(signal, frame))
        if signal == 2:  # KeyboardInterupt - Stop everything
            self.stop()

    def read_switches(self):
        i = 1
        while i <= 8:
            if self.SENSOR_STATE[i] != self.read_switch(i):
                self.SENSOR_STATE[i] = self.read_switch(i)
                switch_topic = "{0}/switch{1}/".format(self.topic, i)
                self.mqtt_client.publish(switch_topic + "switch", self.SENSOR_STATE[i])
                self.logger.info("Switch{0} changed to {1}".format(i, self.SENSOR_STATE[i]))
            i += 1
        if not self.stopped:
            Timer(0.5, self.read_switches).start()

    def read_switch(self, nr):
        if self.read_state(nr):
            return "true"
        else:
            return "false"

    def stop(self):
        self.stopped = 1
        print("Waiting 5 seconds to close all threads")
        sleep(5)
        self.mqtt_client.publish(self.topic + "/$state", "disconnected")
        self.mqtt_client.disconnect()
        self.started = 0
        sys.exit()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
