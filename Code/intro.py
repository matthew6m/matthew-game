import random
import string
import time

def Roll():
    X = random.choice(string.ascii_letters)
    return X

count = 1

while True:
    R = Roll()
    print(R)
    time.sleep(0.05)
    count += 1
    if R == "C":
        break

while True:
    R = Roll()
    print("C"+R)
    time.sleep(0.05)
    count += 1
    if R == "a":
        break

while True:
    R = Roll()
    print("Ca"+R)
    time.sleep(0.05)
    count += 1
    if R == "r":
        break

while True:
    R = Roll()
    print("Car"+R)
    time.sleep(0.05)
    count += 1
    if R == "s":
        break

while True:
    R = Roll()
    print("Cars"+R)
    time.sleep(0.05)
    count += 1
    if R == "m":
        break

while True:
    R = Roll()
    print("Carsm"+R)
    time.sleep(0.05)
    count += 1
    if R == "a":
        break

while True:
    R = Roll()
    print("Carsma"+R)
    time.sleep(0.05)
    count += 1
    if R == "t":
        break

while True:
    R = Roll()
    print("Carsmat"+R)
    time.sleep(0.05)
    count += 1
    if R == "t":
        print("It took",count,"times.")
        break
    