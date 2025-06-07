from machine import Pin, time_pulse_us
from time import sleep, sleep_ms, sleep_us

# LED-uri
red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

# HC-SR04: TRIG = GP9, ECHO = GP10
trig = Pin(9, Pin.OUT)
echo = Pin(10, Pin.IN)

# Buzzer pe GP8
buzzer = Pin(8, Pin.OUT)

# Funcție de măsurare a distanței
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

# Funcție pentru controlul buzzer-ului în timp real
def update_buzzer():
    dist = read_distance_cm()
    if dist is not None and dist < 15:
        buzzer.value(1)
    else:
        buzzer.value(0)

# Buclă principală
while True:
    distance = read_distance_cm()

    if distance is None:
        print("Eroare: senzorul nu a detectat nimic.")
        red.value(1)
        yellow.value(0)
        green.value(0)
        buzzer.value(0)
        sleep(0.2)
        continue

    print("Distanta:", round(distance, 2), "cm")

    if distance < 30:
        red.value(0)
        yellow.value(1)
        for _ in range(5):  # 0.5s divizat în 5x0.1s
            update_buzzer()
            sleep(0.1)
        yellow.value(0)
        green.value(1)
        for _ in range(30):  # 3s în 30x0.1s
            update_buzzer()
            sleep(0.1)
        green.value(0)
        yellow.value(1)
        for _ in range(10):  # 1s în 10x0.1s
            update_buzzer()
            sleep(0.1)
        yellow.value(0)
        buzzer.value(0)  # asigurăm oprirea buzzer-ului
    else:
        red.value(1)
        yellow.value(0)
        green.value(0)
        buzzer.value(0)
        sleep(0.2)

