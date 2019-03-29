# Python imports
from time import sleep
from threading import Timer
import json
import socket
from uuid import getnode as get_mac
import subprocess
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

    def __init__(self, name, mqtt_host='localhost'):
        self.mqtt_client = MQTTClient(name, mqtt_host)
        self.mqtt_client.connect()
        self.base_topic = "homie"
        self.device_id = name.replace(' ', '_') # Use name as device_id. Replacing spaces with underscore
        self.homie = "3.0.1"
        self.name = name
        self.localip = get_ip()
        self.mac = get_mac()
        self.fw_name = "Raspi Relayboard"
        self.fw_version = "0.1"
        self.nodes = "lights[]"
        self.implementation = "RaspberryPi"
        self.stats = "uptime,signal,cputemp,cpuload,freeheap,supply"
        self.stats_interval = 60

        self.mqtt_publish_device()
        self.send_stats()
        
        Timer(self.stats_interval, self.send_stats).start()

    def mqtt_publish_device(self):
        topic = "{0}/{1}/".format(self.base_topic, self.device_id)
        self.mqtt_client.publish(topic + "$homie", self.homie)
        self.mqtt_client.publish(topic + "$name", self.name)
        self.mqtt_client.publish(topic + "$localip", self.localip)
        self.mqtt_client.publish(topic + "$mac", self.mac)
        self.mqtt_client.publish(topic + "$fw/name", self.fw_name)
        self.mqtt_client.publish(topic + "$fw/version", self.fw_version)
        self.mqtt_client.publish(topic + "$nodes", self.nodes)
        self.mqtt_client.publish(topic + "$implementation", self.implementation)
        self.mqtt_client.publish(topic + "$stats", self.stats)
        self.mqtt_client.publish(topic + "$stats/interval", self.stats_interval)
        self.mqtt_client.publish(topic + "$state", "ready")

    def mqtt_send_stats(self):
        stats_topic = "{0}/{1}/$stats/".format(self.base_topic, self.device_id)
        uptime = subprocess.check_output(['cat', '/proc/uptime']).decode('utf-8').split()[0]
        self.mqtt_client.publish(stats_topic + "uptime", uptime)

        signal = "Not implemented yet"
        self.mqtt_client.publish(stats_topic + "signal", 0)

        cputemp = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']) / 1000
        self.mqtt_client.publish(stats_topic + "cputemp", cputemp)

        cpuload = subprocess.check_output(['cat', '/proc/loadavg'])
        self.mqtt_client.publish(stats_topic + "cpuload", cpuload)

        freeheap = subprocess.check_output(['cat', '/proc/meminfo']).decode('utf-8').split('\n')[1].replace(' ', '').split(':')[1][:-2]
        self.mqtt_client.publish(stats_topic + "freeheap", freeheap)

        supply = "Not implemented yet"
        self.mqtt_client.publish(stats_topic + "supply", 0)


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

