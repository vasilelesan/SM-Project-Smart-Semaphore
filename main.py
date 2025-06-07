# main.py
# sistem de control semafor cu senzor ultrasonic si comenzi bluetooth

from time import sleep, ticks_ms, ticks_diff
from machine import UART
from components.leds import LedController
from components.sensor import DistanceSensor
from components.buzzer import Buzzer

# initializare uart pentru comunicatie bluetooth
uart = UART(0, baudrate=9600)

# initializare componente
leds = LedController(red_pin=15, yellow_pin=14, green_pin=13)
sensor = DistanceSensor(trig_pin=9, echo_pin=10)
buzzer = Buzzer(pin=8)

# stari de control
semafor_activ = True
mod_fortat = False

# pornim cu lumina verde
leds.green_on()

while True:
    # verificare comenzi primite prin bluetooth
    if uart.any():
        cmd = uart.read().decode().strip().lower()
        print("comanda bluetooth:", cmd)

        if cmd == "stop":
            # dezactivare semafor si toate componentele
            semafor_activ = False
            mod_fortat = False
            leds.off_all()
            buzzer.off()

        elif cmd == "start":
            # activare mod automat
            semafor_activ = True
            mod_fortat = False
            leds.set_color("verde")

        elif cmd == "rosu":
            # fortare lumina rosie cu tranzitie daca era verde
            mod_fortat = True
            if leds.is_green():
                leds.to_red(buzzer)
            else:
                leds.set_color("rosu")

        elif cmd == "verde":
            # fortare lumina verde cu tranzitie daca era rosu
            mod_fortat = True
            if not leds.is_green():
                leds.to_green()

    # daca semaforul este inactiv sau in mod fortat, sarim peste logica senzorului
    if not semafor_activ or mod_fortat:
        sleep(0.2)
        continue

    # citim distanta de la senzorul ultrasonic
    distance = sensor.read_distance_cm()
    if distance is None:
        print("eroare: senzorul nu a detectat nimic.")
        buzzer.off()
        sleep(0.2)
        continue

    print("distanta:", round(distance, 2), "cm")

    # daca obiectul este foarte aproape (<15cm), buzzer-ul emite beep
    if distance < 15:
        buzzer.beep()
    else:
        buzzer.off()

    # daca suntem pe verde si obiectul este aproape (<30cm), trecem pe rosu
    if distance < 30 and leds.is_green():
        leds.to_red(buzzer)

        # monitorizam cat timp obiectul ramane in apropiere
        while True:
            dist = sensor.read_distance_cm()
            print("monitorizare:", dist)

            if dist is not None and dist < 15:
                buzzer.beep()
            else:
                buzzer.off()

            if dist is not None and dist > 15:
                print("obiectul s-a retras, astept 5s...")
                sleep(5)
                break

            sleep(0.1)

        # revenim pe verde
        leds.to_green()

        # pauza de 5 secunde in care ignoram senzorul
        print("perioada de trecere: 5 secunde protejate")
        start_time = ticks_ms()
        while ticks_diff(ticks_ms(), start_time) < 5000:
            sleep(0.1)
