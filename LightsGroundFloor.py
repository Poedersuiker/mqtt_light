# Python imports
from time import sleep
# 3rd party imports

# module imports
from MQTTLight import MQTTLight

kitchen_light = MQTTLight("GroundFloor", "Kitchen", 1, 7, '192.168.0.10')

i = 0
while i < 5:
    kitchen_light.switch_light()
    sleep(1)
    i += 1
