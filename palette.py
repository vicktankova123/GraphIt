import math
from equations import normal


class Palette:
    def __init__(self):
        # We like the rainbow like a unicorn!!
        self.colorMap = [ [0.0, (230/255, 38/255, 31/255)],    # red
                          [0.20, (235/255, 117/255, 50/255)],  # orange
                          [0.40, (247/255, 208/255, 56/255)],  # yellow
                          [0.60, (38/255, 230/255, 72/255)],  # green
                          [0.80, (52/255, 38/255, 230/255)],  # blue
                          [0.90, (67/255, 85/255, 219/255)],   # indigo
                          [1.00, (117/255, 59/255, 231/255)]]  # violet
        self.numColors = len(self.colorMap)

    def int2Hex(self, val):
        # Converts an integer into hex string values without 0x header
        hexStr = hex(val).replace('0x', '')
        if len(hexStr) < 2:
            hexStr = f'0{hexStr}'

        return hexStr

    def getColor(self, val, minVal, maxVal, spread=1):
        # Gets the gradient color according to the value in the minVal-maxVal range
        val -= minVal
        width = maxVal - minVal

        r = sum([normal(val, c[1][0], c[0] * width, width/(spread*self.numColors)) for c in self.colorMap])
        g = sum([normal(val, c[1][1], c[0] * width, width/(spread*self.numColors)) for c in self.colorMap])
        b = sum([normal(val, c[1][2], c[0] * width, width/(spread*self.numColors)) for c in self.colorMap])

        return min(1.0, r), min(1.0, g), min(1.0, b)

    def getColorHexStr(self, val, minVal, maxVal, spread=1):
        # Gets the gradient color hex string ready to use!!!!
        r, g, b = [int(c*255) for c in self.getColor(val, minVal, maxVal, spread)]

        return f'#{self.int2Hex(r)}{self.int2Hex(g)}{self.int2Hex(b)}'
