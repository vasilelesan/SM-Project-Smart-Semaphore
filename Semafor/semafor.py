from machine import Pin, time_pulse_us, UART
from time import sleep, sleep_ms, sleep_us
import time

# LED-uri
red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

# HC-SR04
trig = Pin(9, Pin.OUT)
echo = Pin(10, Pin.IN)

# Buzzer
buzzer = Pin(8, Pin.OUT)

# Bluetooth UART
uart = UART(0, baudrate=9600)

# Stări de control
semafor_activ = True
mod_fortat = False
culoare_fortata = None

def read_distance_cm():
    trig.low()
    sleep_ms(2)
    trig.high()
    sleep_us(10)
    trig.low()
    duration = time_pulse_us(echo, 1, 30000)
    if duration <= 0:
        return None
    return duration * 0.0343 / 2

# Funcții de tranziție între stări
def verde_to_rosu():
    green.value(0)
    yellow.value(1)
    sleep(0.5)
    yellow.value(0)
    red.value(1)
    for _ in range(3):
        buzzer.value(1)
        sleep(0.1)
        buzzer.value(0)
        sleep(0.1)

def rosu_to_verde():
    red.value(0)
    yellow.value(1)
    sleep(1)
    yellow.value(0)
    green.value(1)

# Pornim pe verde
red.value(0)
yellow.value(0)
green.value(1)

while True:
    # Comenzi Bluetooth
    if uart.any():
        cmd = uart.read().decode().strip().lower()
        print("Comanda Bluetooth:", cmd)

        if cmd == "stop":
            semafor_activ = False
            mod_fortat = False
            red.value(0)
            yellow.value(0)
            green.value(0)
            buzzer.value(0)

        elif cmd == "start":
            semafor_activ = True
            mod_fortat = False
            green.value(1)
            red.value(0)
            yellow.value(0)

        elif cmd == "rosu":
            mod_fortat = True
            if green.value() == 1:
                verde_to_rosu()
            elif yellow.value() == 1:
                yellow.value(0)
                red.value(1)
            else:
                red.value(1)
                green.value(0)
                yellow.value(0)

        elif cmd == "verde":
            mod_fortat = True
            if red.value() == 1:
                rosu_to_verde()
            elif yellow.value() == 1:
                yellow.value(0)
                green.value(1)
            else:
                green.value(1)
                red.value(0)
                yellow.value(0)

    if not semafor_activ:
        sleep(0.2)
        continue

    if mod_fortat:
        sleep(0.2)
        continue

    distance = read_distance_cm()
    if distance is None:
        print("Eroare: senzorul nu a detectat nimic.")
        buzzer.value(0)
        sleep(0.2)
        continue

    print("Distanta:", round(distance, 2), "cm")

    if distance < 15:
        buzzer.value(1)
        sleep(0.1)
        buzzer.value(0)
        sleep(0.1)
    else:
        buzzer.value(0)

    if distance < 30 and green.value() == 1:
        verde_to_rosu()

        while True:
            dist = read_distance_cm()
            print("Monitorizare:", dist)

            if dist is not None and dist < 15:
                buzzer.value(1)
                sleep(0.1)
                buzzer.value(0)
                sleep(0.1)
            else:
                buzzer.value(0)

            if dist is not None and dist > 15:
                print("Obiectul s-a retras, aștept 5s...")
                sleep(5)
                break

            sleep(0.1)

        rosu_to_verde()

        print("Perioadă de trecere: 5 secunde protejate")
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 5000:
            sleep(0.1)

