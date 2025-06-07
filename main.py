# main.py
from time import sleep, ticks_ms, ticks_diff
from machine import UART
from components.leds import LedController
from components.sensor import DistanceSensor
from components.buzzer import Buzzer

uart = UART(0, baudrate=9600)
leds = LedController(red_pin=15, yellow_pin=14, green_pin=13)
sensor = DistanceSensor(trig_pin=9, echo_pin=10)
buzzer = Buzzer(pin=8)

semafor_activ = True
mod_fortat = False

leds.green_on()

while True:
    if uart.any():
        cmd = uart.read().decode().strip().lower()
        print("Comanda Bluetooth:", cmd)

        if cmd == "stop":
            semafor_activ = False
            mod_fortat = False
            leds.off_all()
            buzzer.off()

        elif cmd == "start":
            semafor_activ = True
            mod_fortat = False
            leds.set_color("verde")

        elif cmd == "rosu":
            mod_fortat = True
            if leds.is_green():
                leds.to_red(buzzer)
            else:
                leds.set_color("rosu")

        elif cmd == "verde":
            mod_fortat = True
            if not leds.is_green():
                leds.to_green()

    if not semafor_activ or mod_fortat:
        sleep(0.2)
        continue

    distance = sensor.read_distance_cm()
    if distance is None:
        print("Eroare: senzorul nu a detectat nimic.")
        buzzer.off()
        sleep(0.2)
        continue

    print("Distanta:", round(distance, 2), "cm")

    if distance < 15:
        buzzer.beep()
    else:
        buzzer.off()

    if distance < 30 and leds.is_green():
        leds.to_red(buzzer)

        while True:
            dist = sensor.read_distance_cm()
            print("Monitorizare:", dist)

            if dist is not None and dist < 15:
                buzzer.beep()
            else:
                buzzer.off()

            if dist is not None and dist > 15:
                print("Obiectul s-a retras, aștept 5s...")
                sleep(5)
                break

            sleep(0.1)

        leds.to_green()

        print("Perioadă de trecere: 5 secunde protejate")
        start_time = ticks_ms()
        while ticks_diff(ticks_ms(), start_time) < 5000:
            sleep(0.1)


