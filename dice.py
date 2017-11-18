from random import random
import math
import time
#---------------------------------------

def roll(sides):
    r = random()
    rolled = r * sides + 1
    rolled = math.floor(rolled)
    return rolled

while True:
    total = roll(10) + roll(6)
    print(total)
    time.sleep(0.005)
    if total > 6:
        break
