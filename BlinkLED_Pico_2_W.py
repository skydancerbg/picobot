from machine import Pin
from sys import implementation
import time

print(implementation._machine)
led = Pin("LED", Pin.OUT)

while True:
    led.value(1)
    time.sleep(1.0)
    led.value(0)
    time.sleep(1.0)