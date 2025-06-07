# components/leds.py
from time import sleep
from machine import Pin

class LedController:
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.red = Pin(red_pin, Pin.OUT)
        self.yellow = Pin(yellow_pin, Pin.OUT)
        self.green = Pin(green_pin, Pin.OUT)

    def off_all(self):
        self.red.value(0)
        self.yellow.value(0)
        self.green.value(0)

    def green_on(self):
        self.off_all()
        self.green.value(1)

    def red_on(self):
        self.off_all()
        self.red.value(1)

    def yellow_on(self):
        self.off_all()
        self.yellow.value(1)

    def is_green(self):
        return self.green.value() == 1

    def to_red(self, buzzer=None):
        self.green.value(0)
        self.yellow.value(1)
        sleep(0.5)
        self.yellow.value(0)
        self.red.value(1)
        if buzzer:
            for _ in range(3):
                buzzer.on()
                sleep(0.1)
                buzzer.off()
                sleep(0.1)

    def to_green(self):
        self.red.value(0)
        self.yellow.value(1)
        sleep(1)
        self.yellow.value(0)
        self.green.value(1)

    def set_color(self, color):
        self.off_all()
        if color == "verde":
            self.green.value(1)
        elif color == "galben":
            self.yellow.value(1)
        elif color == "rosu":
            self.red.value(1)

