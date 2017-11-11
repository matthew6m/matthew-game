from random import random
from time import sleep

def Stat(xd):
    lol = round(random()*xd)
    return lol


def Name():
    name = input("> ")
    print(name, "has ", Stat(1000), " XP")

Name()