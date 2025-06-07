# components/buzzer.py
# clasa pentru controlul buzzer-ului

from machine import Pin
from time import sleep

class Buzzer:
    def __init__(self, pin):
        self.buzzer = Pin(pin, Pin.OUT)

    def on(self):
        # activeaza buzzer-ul
        self.buzzer.value(1)

    def off(self):
        # dezactiveaza buzzer-ul
        self.buzzer.value(0)

    def beep(self, duration=0.1):
        # emite un beep scurt
        self.on()
        sleep(duration)
        self.off()
        sleep(duration)
