import threading
import pyudmx


class light:
    def __init__(self):
        pass

class mqtt_lights:
    def __init__(self, udmx):
        self.udmx = udmx

if __name__ == '__main__':
    udmx = pyudmx.uDMXDevice()