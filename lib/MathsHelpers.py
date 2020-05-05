import math
import random as rd

def generateRandomSizeInCm(amplitude, minimum):
    return round(100 * (amplitude/(2+math.exp(9-rd.randint(0, 20)))+minimum))/100

def convertFromCmToInch(sizeInCm):
    return round(100*sizeInCm/2.54)/100