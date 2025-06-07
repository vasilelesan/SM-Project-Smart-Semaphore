# components/sensor.py
# clasa pentru senzorul ultrasonic hc-sr04

from machine import Pin, time_pulse_us
from time import sleep_ms, sleep_us

class DistanceSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def read_distance_cm(self):
        # calculeaza distanta in centimetri
        self.trig.low()
        sleep_ms(2)
        self.trig.high()
        sleep_us(10)
        self.trig.low()
        duration = time_pulse_us(self.echo, 1, 30000)
        if duration <= 0:
            return None
        return duration * 0.0343 / 2