import threading
import json
import pyudmx
import mqtt_client


class Light:
    def __init__(self, name, floor, dmx_channel, on_change):
        self.name = name
        self.floor = floor
        self.dmx_channel = dmx_channel
        self.on_change = on_change

        self.topic_prefix = 'hassio/light/{0}/{1}/'.format(self.floor, self.name)
        self.set_topic = '{0}{1}'.format(self.topic_prefix, 'set')
        self.state_topic = '{0}{1}'.format(self.topic_prefix, 'state')
        self.config_topic = '{0}{1}'.format(self.topic_prefix, 'config')

        self.capabilities = {}
        self.capabilities["name"] = self.name
        self.capabilities["platform"] = 'mqtt_json'
        self.capabilities["state_topic"] = self.state_topic
        self.capabilities["command_topic"] = self.set_topic
        self.capabilities["brightness"] = "true"
        self.capabilities["brightness_command_topic"] = self.set_topic
        self.capabilities["effect"] = "true"
        self.capabilities["effect_list"] = ["starlight", "flash", "postapoc", "solid"]
        self.capabilities["effect_command_topic"] = self.set_topic
        self.capabilities["confg_topic"] = self.config_topic

        self.status = {}
        self.status["brightness"] = 200
        self.status["color_temp"] = 155  # not used
        self.status["color"] = {"r": 255, "g": 255, "b": 255, "x": 0.123, "y": 0.123}  # not implemented
        self.status["effect"] = "solid"
        self.status["transition"] = 2
        self.status["white_value"] = 150

        self.mqtt = mqtt_client.mqtt_client(name)

    def json_config(self):
        return json.dumps(self.capabilities)

    def json_state(self):
        return json.dumps(self.status)

    def on_message(self, client, userdata, msg):
        pass

    def set_brightness(self, level):
        self.status["brightness"] = level
        self.on_change(self.dmx_channel, self.level)

    def send_state(self):
        self.mqtt.send_status(self.json_state())

    def send_config(self):
        self.mqtt.send_config(self.json_config())


class MqttLights:
    def __init__(self):
        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()
        self.lights = {}

    def add_light(self, light):
        channel = light.dmx_channel
        self.lights[channel] = light

    def remove_light(self, channel):
        self.lights.pop(channel, None)

    def on_change(self, channel, level):
        self.udmx.send_single_value(channel, level)
        print('Set {0} to {1}'.format(channel, level))


if __name__ == '__main__':
    mqtt_lights = MqttLights()