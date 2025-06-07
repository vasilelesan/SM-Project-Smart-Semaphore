from machine import Pin, time_pulse_us, UART
from time import sleep, sleep_ms, sleep_us

# LED-uri
red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

# HC-SR04
trig = Pin(9, Pin.OUT)
echo = Pin(10, Pin.IN)

# Buzzer
buzzer = Pin(8, Pin.OUT)

# Bluetooth UART pe GP0 (TX), GP1 (RX)
uart = UART(0, baudrate=9600)

# Variabilă pentru activare/dezactivare semafor
semafor_activ = True

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

def update_buzzer():
    dist = read_distance_cm()
    if dist is not None and dist < 15:
        buzzer.value(1)
    else:
        buzzer.value(0)

while True:
    # Citim comenzi de la HC-05
    if uart.any():
        comanda = uart.read().decode().strip().lower()
        print("Comanda Bluetooth:", comanda)
        if comanda == "start":
            semafor_activ = True
        elif comanda == "stop":
            semafor_activ = False
            red.value(0)
            yellow.value(0)
            green.value(0)
            buzzer.value(0)

    if not semafor_activ:
        sleep(0.1)
        continue

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
        for _ in range(5):
            update_buzzer()
            sleep(0.1)
        yellow.value(0)
        green.value(1)
        for _ in range(30):
            update_buzzer()
            sleep(0.1)
        green.value(0)
        yellow.value(1)
        for _ in range(10):
            update_buzzer()
            sleep(0.1)
        yellow.value(0)
        buzzer.value(0)
    else:
        red.value(1)
        yellow.value(0)
        green.value(0)
        buzzer.value(0)
        sleep(0.2)

