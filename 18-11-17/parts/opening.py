import storyeng as s

forest = """
So you are now in the forest and now you can accsess your bag.
typin the word BAG.
"""

car = """
So you are now in the car and now you can accsess your bag.
typin the word BAG.
"""

s.parts.Start = {
    'onenter': 'Welcome to mygreat game.',
    'oninput': 'Name'
}

def _oninput(e):
    s.data['name'] = e.line
    s.go('Feild')

s.parts.Name = {
    'onenter': "I'm MATTHEW, your narrator. What's your name?",
    'oninput': _oninput,
    'onleave': "Well nice to meet you, {name}."
}

def _oninput(e):
    if e.lower == "car":
        s.go('Car')
    elif e.lower == "forest":
        s.go('Forest')
    else:
        s.go('Feild')

s.parts.Feild = {
    'onenter': "You are in a feild {name}, do you go into the Forest or your CAR?",
    'oninput': _oninput
}

def _oninput(e):
    if e.lower == "bag":
        s.go('Bag')
    else:
        print("you had one job.")

s.parts.Forest = {
    'onenter': forest,
    'oninput': _oninput
}

s.parts.Car = {
    'onenter': car,
    'oninput': _oninput
}

def Bag_Things():
    print("you have a "["food","laptop","book","gameboy"])

s.parts.Bag = {
    'oninput': Bag_Things
}