import random
import string
import time

def Roll():
    X = random.choice(string.ascii_letters)
    return X

count = 1

while True:
    R = Roll() + Roll() + Roll() + Roll() + Roll() + Roll() + Roll() + Roll()
    print(R)
    count += 1
    if R == "Carsmatt":
        print("It took",count,"times.")
        break
    