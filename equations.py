from math import * 
from matrix import *

#keyboard
class Keyboard:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill = "white", width = 3)

#2D graphing
def customFunc(s, x):
    if 'csc' in s:
        s = s.replace('csc', '1/sin')
    if 'sec' in s:
        s = s.replace('sec', '1/cos')
    if 'cot' in s:
        s = s.replace('cot', '1/tan')
    if s == '':
        return 0
    try:
        return eval(s)
    except:
        return None

#normal equations
def normal(x, k, mu, sigma, b=0):
    return k * exp(-(x - mu)**2 / (2 * sigma**2)) + b

def bivarNormal(x, k, mu, sigma, b=0):
    xm = [[xi-mui for xi, mui in zip(x, mu)]]
    c = 1 / sqrt((2*pi)**2 * matDet2D(sigma))
    sigmaInv = matInv2D(sigma)
    t = matMul(xm, matMul(sigmaInv, transpose(xm)))[0][0]
    
    return - k * c * exp(-t / 2) + b