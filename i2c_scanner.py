from machine import Pin, SoftI2C
from time import sleep

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)

print(i2c.scan())
while True:
    print(i2c.readfrom(0x6B, 6))
    sleep(0.1)

