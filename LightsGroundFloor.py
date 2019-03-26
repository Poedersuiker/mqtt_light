# Python imports
from time import sleep
# 3rd party imports

# module imports
from MQTTLight import MQTTLight

kitchen_light = MQTTLight("GroundFloor", "Kitchen", 1, 7)

i = 0
while i < 10:
    kitchen_light.switch_light()
    sleep(5)
    i += 1
