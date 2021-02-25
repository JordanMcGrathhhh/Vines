import random

char_map = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26
}


def generateCode():

    code = []

    for x in range(0, 8):
        y = random.randint(1, 34)
        print(str(x) + ":" + str(y))
        if y < 26:
            code.append(str(list(char_map.keys())[list(char_map.values()).index(y)]))
        else:
            code.append(str(y - 26))

    return ''.join(code)
