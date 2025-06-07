# components/buzzer.py
from machine import Pin
from time import sleep

class Buzzer:
    def __init__(self, pin):
        self.buzzer = Pin(pin, Pin.OUT)

    def on(self):
        self.buzzer.value(1)

    def off(self):
        self.buzzer.value(0)

    def beep(self, duration=0.1):
        self.on()
        sleep(duration)
        self.off()
        sleep(duration)