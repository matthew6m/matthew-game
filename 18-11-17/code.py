import random
import string
import time

def Roll():
    X = random.choice(string.ascii_letters)
    return X

count = 1

while True:
    Name = Roll() + Roll() + Roll()
    print(Name)
    count += 1
    if Name == "Rob":
        print("It took",count,"times.")
        time.sleep(10)