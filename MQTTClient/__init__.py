import paho.mqtt.client as mqtt
import threading


class MQTTClient(threading.Thread):
    def __init__(self, name, host="localhost", port=1883):
        self.mqtt_client = mqtt.Client()
        self.host = host
        self.port = port
        self.name = name

    def set_on_connect(self, on_connect):
        self.mqtt_client.on_connect = on_connect

    def set_on_message(self, on_message):
        self.mqtt_client.on_message = on_message

    def connect(self, config_topic, state_topic, set_topic, cap_json, status_json):
        self.config_topic = config_topic
        self.state_topic = state_topic
        self.set_topic = set_topic

        self.mqtt_client.connect(self.host, self.port, 60)
        self.mqtt_client.subscribe(self.config_topic)
        self.mqtt_client.subscribe(self.state_topic)
        self.mqtt_client.subscribe(self.set_topic)

        self.send_config(cap_json)
        self.send_status(status_json)
        self.send_config(cap_json)
        self.send_status(status_json)

    def send_config(self, json):
        self.mqtt_client.publish(self.config_topic, json)

    def send_status(self, json):
        self.mqtt_client.publish(self.state_topic, json)

    def run(self):
        self.mqtt_client.loop_forever()


def on_connect(client, userdata, flags, rc):
    print('Connected with result code: '.format(rc))

def on_message(client, userdata, msg):
    print('{0} : {1}'.format(msg.topic, msg.payload))


if __name__ == '__main__':
    mqtt_c = MQTTClient('test')
    mqtt_c.set_on_connect(on_connect)
    mqtt_c.set_on_message(on_message)
    mqtt_c.connect('hassio/test/config', 'hassio/test/state', 'hassio/test/set', '{1}', '{2}')
    mqtt_c.start()