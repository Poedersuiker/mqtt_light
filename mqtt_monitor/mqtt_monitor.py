import paho.mqtt.client as mqtt
import json
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    client.subscribe("hassio/#")

def on_message(client, userdata, msg):
    print(msg.topic)
    jsonstr = msg.payload.decode("utf-8")
    try:
        pp.pprint(json.loads(jsonstr))
    except:
        pp.pprint(jsonstr)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()