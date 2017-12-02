from random import random
import math
import time
#---------------------------------------

def roll(sides):
    r = random()
    rolled = r * sides + 1
    rolled = math.floor(rolled)
    return rolled

times = 0

while True:
    total = roll(10)
    print(total)
    times += 1
    if total == 6:
        print("It took",times,"times.")
        times = 0
        time.sleep(1)
        
