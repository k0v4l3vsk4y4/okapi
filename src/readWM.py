import numpy as np

def readWM(wmPath):
    # File read
    with open(wmPath, "r") as file:
        content = file.read()

    # Divideix en línies
    lines = content.split('\n')[0:-1]

    v = [int(line) for line in lines]
    v = np.array(v)
    return (v)