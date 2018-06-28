#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import take_photo as tpho

GPIO.setmode(GPIO.BOARD)
def ReadDistance(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    time.sleep(0.000002)
    GPIO.output(pin, 1)
    time.sleep(0.000005)
    GPIO.output(pin, 0)
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == 0:
        starttime = time.time()
    while GPIO.input(pin) == 1:
        endtime = time.time()
    duration = endtime-starttime
    # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s
    distance = duration*34000/2
    return distance
i = 0
while True:
    distance = ReadDistance(11)
    print(distance)
    if distance < 150:
        tpho.take_photo(i)
        i += 1
    time.sleep(.5)