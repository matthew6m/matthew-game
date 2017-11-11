from random import random
from time import sleep

def Stat(xd):
    global lol
    lol = round(random()*xd)
    return print(lol)

while True:
    Stat(10)
    sleep(0.005)
    if lol == 6:
        sleep(1)
    Stat(100)
    sleep(0.005)
    if lol == 66:
        sleep(1)
    Stat(1000)
    sleep(0.005)
    if lol == 666:
        sleep(1)