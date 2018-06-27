#!/usr/bin/python
import time
import RPi.GPIO as GPIO


# Use board based pin numbering
GPIO.setmode(GPIO.BOARD)


def ReadDistance(pin):
    print("primera entrada")
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

    time.sleep(0.000002)

    #send trigger signal
    GPIO.output(pin, 1)

    time.sleep(0.000005)
    print("segunda entrada")
    GPIO.output(pin, 0)

    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == 0:
        starttime = time.time()
        print("quinta entrada")    
    print("tercera entrada")
    while GPIO.input(pin) == 1:
        endtime = time.time()
        print("sexta entrada")

    duration = endtime-starttime
    # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s
    distance = duration*34000/2
    print("septima entrada")
    return distance
while True:
   distance = ReadDistance(11)
   print("cuarta entrada")
   print("Distance to object is ", distance, " cm or ", distance*.3937, " inches")
   time.sleep(.5)
