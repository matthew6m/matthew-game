from random import random
import time

def Stat(duplicator):
    R = round(random()*duplicator)
    return R

count = 1
line = 0
while True:
    equal = Stat(1500)
    while line < equal:
        print(count)
        count *= 2
        line += 1
        time.sleep(0.005)

    while line > 0:
        line -= 1
        print(count)
        count //= 2
        time.sleep(0.005)