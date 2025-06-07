from machine import Pin, time_pulse_us
from time import sleep, sleep_ms, sleep_us

# LED-uri (GPIO 15, 14, 13)
red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

# Senzor HC-SR04 pe GP9 (TRIG) și GP10 (ECHO)
trig = Pin(9, Pin.OUT)
echo = Pin(10, Pin.IN)

# Buzzer activ pe GP8
buzzer = Pin(8, Pin.OUT)

# Funcție de măsurare a distanței în cm
def read_distance_cm():
    trig.low()
    sleep_ms(2)
    trig.high()
    sleep_us(10)
    trig.low()

    duration = time_pulse_us(echo, 1, 30000)
    if duration <= 0:
        return None

    distance_cm = duration * 0.0343 / 2
    return distance_cm

# Buclă principală: semafor inteligent
while True:
    distance = read_distance_cm()

    if distance is None:
        print("Eroare: senzorul nu a detectat nimic.")
        red.value(1)
        yellow.value(0)
        green.value(0)
        buzzer.value(0)  # Oprește buzzerul
        sleep(0.2)
        continue

    print("Distanta:", round(distance, 2), "cm")

    # Buzzer dacă e prea aproape
    if distance < 15:
        buzzer.value(1)
    else:
        buzzer.value(0)

    if distance < 30:
        # Mașină detectată: semafor trece în verde
        red.value(0)
        yellow.value(1)
        sleep(0.5)
        yellow.value(0)
        green.value(1)
        sleep(3)
        green.value(0)
        yellow.value(1)
        sleep(1)
        yellow.value(0)
    else:
        # Nicio mașină: roșu aprins
        red.value(1)
        yellow.value(0)
        green.value(0)
        sleep(0.2)

