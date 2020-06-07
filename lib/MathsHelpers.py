import math
import random as rd

def roundToSetDecimalPlace(toBeRoundedNumber, decimalPlaces):
    shiftMagnitude = pow(10, decimalPlaces)
    return round(shiftMagnitude*toBeRoundedNumber)/shiftMagnitude

def generateRandomSizeInCm(amplitude, minimum):
    return minimum + amplitude/(2+math.exp(9-rd.randint(0, 16)))

def convertFromCmToInch(sizeInCm):
    return sizeInCm/2.54
