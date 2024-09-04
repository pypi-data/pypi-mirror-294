import warnings
warnings.simplefilter('ignore')

import gpiozero
import time

class Relay():
    gpio_number = None
    relay = None

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number

    def on(self):
        self.relay = gpiozero.DigitalOutputDevice(self.gpio_number)

    def off(self):
        self.relay.close()
