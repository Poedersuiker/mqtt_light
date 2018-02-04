import pyudmx
import random
import time
import threading


class Lights:
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


class Light(threading.Thread):
    def __init__(self, dmx_channel, on_change):
        threading.Thread.__init__(self)
        self.running = False
        self.dmx_channel = dmx_channel
        self.brightness = 0
        self.step_speed = 0.0
        self.target = 0
        self.wait = 0
        self.on_change = on_change

    def run(self):
        self.running = True
        while self.running:
            self.step()
            time.sleep(self.step_speed)

    def step(self):
        if self.wait:
            time.sleep(self.wait)
            self.wait = 0

        if self.brightness == self.target:
            self.wait = random.randint(0, 5)
            self.brightness = random.randint(0, 255)
            self.step_speed = random.randint(0, 100) / 1000.0
        elif self.brightness < self.target:
            self.brightness += 1
            self.on_change(self.dmx_channel, self.brightness)
        else:
            self.brightness -= 1
            self.on_change(self.dmx_channel, self.brightness)

    def stop(self):
        self.running = False


if __name__ == '__main__':
    lights = Lights()
    light1 = Light(1, lights.on_change)
    light1.start()
    light2 = Light(2, lights.on_change)
    light2.start()
    lights.add_light(light1)
    lights.add_light(light2)