import paho.mqtt.client as mqtt
import threading


class MQTTClient(threading.Thread):
    def __init__(self, name, host="192.168.0.10", port=1883):
        threading.Thread.__init__(self, target=self.run)
        self.mqtt_client = mqtt.Client()
        self.host = host
        self.port = port
        self.name = name

    def set_on_connect(self, on_connect):
        self.mqtt_client.on_connect = on_connect

    def set_on_message(self, on_message):
        self.mqtt_client.on_message = on_message

    def connect(self):
        self.mqtt_client.connect(self.host, self.port, 60)

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, msg):
        self.mqtt_client.publish(topic, msg)


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
    mqtt_c.connect()
    mqtt_c.start()