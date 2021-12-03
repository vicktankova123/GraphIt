import tkinter as tk
import math 

def frange(start, end, step):
    rangeList = []
    value = start
    while value < end:
        rangeList.append(value)
        value += step
    return rangeList

class Grid:
    def __init__(self, x, y, width, height, scale = 1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.scale = scale
        self.origin = dict(x=self.x + width//2, 
                           y=self.y + height//2)
        self.gapSize = 10
        self.axisTextFont = "Arial 13 bold"
        self.limits = dict(xNeg = 0, xPos = 0, yNeg = 0, yPos = 0)

    def setScale(self, scale):
        self.scale = scale

    def calcRulerPos(self):
        ox = self.origin['x'] - self.x
        oy = self.origin['y'] - self.y

        leftStart =  ox % self.gapSize
        leftStep =  ox // self.gapSize
        rulerPosL = list(range(leftStart, ox, self.gapSize))
        # boldPosL = [pos for idx, pos in enumerate(rulerPosL.reverse()) if idx%5 == 0]
        self.limits['xNeg'] = -len(rulerPosL)

        rightStart = ox + self.gapSize
        rightStep = (self.width -ox) // self.gapSize
        rulerPosR = list(range(rightStart, self.width, self.gapSize))
        # boldPosR = [pos for idx, pos in enumerate(rulerPosR.reverse()) if idx%5 == 0]
        self.limits['xPos'] = len(rulerPosR)

        topStart = oy % self.gapSize
        topStep = oy // self.gapSize
        rulerPosT = list(range(topStart, self.height, self.gapSize))
        # boldPosR = [pos for idx, pos in enumerate(rulerPosR.reverse()) if idx%5 == 0]
        self.limits['yPos'] = len(rulerPosT)

        bottomStart = oy + self.gapSize
        bottomStep = (self.height -oy) // self.gapSize
        rulerPosB = list(range(bottomStart, self.height, self.gapSize))
        # boldPosR = [pos for idx, pos in enumerate(rulerPosR.reverse()) if idx%5 == 0]
        self.limits['yNeg'] = -len(rulerPosB)


    def _drawAxisText(self, canvas):
        textFrequency = 5 
        # x-axis
        startXPos = (self.width//2) % self.gapSize//textFrequency
        halfSteps = (self.width//2) // self.gapSize//textFrequency
        textValueList = [s*textFrequency*self.scale for s in list(range(-halfSteps, halfSteps+1))]
        textPosList = [s*self.gapSize*textFrequency for s in range(len(textValueList))]

        for idx in range(1,len(textValueList)-1):            
            canvas.create_text(self.x+ startXPos + textPosList[idx],
                                self.origin['y']+self.gapSize,
                                text=f'{textValueList[idx]}',
                                anchor=tk.CENTER,
                                font=self.axisTextFont,
                                fill='black')

        # y-axis
        startYPos = (self.height//2) % self.gapSize//textFrequency
        halfSteps = (self.height//2) // self.gapSize//textFrequency
        textValueList = [s*textFrequency*self.scale for s in list(range(-halfSteps, halfSteps+1))]
        textValueList.reverse()
        textPosList = [s*self.gapSize*textFrequency for s in range(len(textValueList))]
        
        for idx in range(1,len(textValueList)-1):            
            canvas.create_text( self.origin['x']+self.gapSize,
                                self.y+ startYPos +textPosList[idx],
                                text=f'{textValueList[idx]}',
                                anchor=tk.CENTER,
                                font=self.axisTextFont,
                                fill='black')
            
    # draw grid
    def draw(self, canvas):
        self.calcRulerPos()
        drawnCount =4
        for i in range(self.x, self.x + self.width, self.gapSize):
            drawnCount += 1
            lineWidth = 1.0
            if drawnCount % 5 == 0:
                lineWidth = 2.0
            canvas.create_line(i, self.y, i, self.y + self.height, 
                                fill="blue", width=lineWidth)

        drawnCount = 9
        for j in range(self.y, self.y + self.height, self.gapSize):
            drawnCount += 1
            lineWidth = 1.0
            if drawnCount % 5 == 0:
                lineWidth = 2.0
            canvas.create_line(self.x, j, self.x + self.width, j, fill="blue", 
                                width=lineWidth)
        #main axes
        canvas.create_line(self.x, 
                            (self.y + self.height + self.y)/2, 
                            self.x + self.width, 
                            (self.y + self.height + self.y)/2, 
                            fill = "black", width = 3)
        canvas.create_line((self.x + self.width +self.x)/2 , 
                            self.y, (self.x + self.width+self.x)/2, 
                            self.y + self.height, fill = "black", width = 3)
        
        # Draw axis text on top of grid
        self._drawAxisText(canvas)


    #Draw function:
    def plotFunction(self, app, canvas):
        (xStart, xEnd) = self.limits['xNeg'], self.limits['xPos']
        xList = range(xStart, xEnd+1)
        xList = []
        yList = []
        for x in frange(xStart, xEnd+1, 0.01):
            try:
                y = app.selectedFunc(app.customFuncStr,x*self.scale)
                yList.append(y)
                xList.append(x)
            except:
                for delta in [-0.8, -0.6, -0.4, -0.1, 0, 0.1, 0.4, 0.8]:
                    if delta == 0:
                        xList.append(None)
                        yList.append(None)
                    else:
                        xd = x+delta
                        y = app.selectedFunc(app.customFuncStr,xd*self.scale)
                        yList.append(y)
                        xList.append(xd)    

        #draw line at the closest point to asymptote:           
        for idx in range(1,len(xList)):
            if xList[idx] != None and xList[idx-1] != None and yList[idx] != None and yList[idx-1] != None:
                dist = math.sqrt(((xList[idx-1]-xList[idx])**2 + (yList[idx-1]-yList[idx])**2))          
                if dist > 5:
                    continue
                else:
                    if xList[idx] != None and xList[idx-1] != None and yList[idx] != None and yList[idx-1] != None:
                        x0 = xList[idx-1] * self.gapSize + self.origin['x']
                        y0 = -yList[idx-1] * self.gapSize/self.scale + self.origin['y']
                        x1 = xList[idx] * self.gapSize + self.origin['x']
                        y1 = -yList[idx] * self.gapSize/self.scale + self.origin['y']
                        canvas.create_line(x0, y0,
                                            x1, y1,
                                            fill=app.lineColour, 
                                            width=app.lineWidth)
    #derivative
    def plotDerivative(self, app, canvas):
        (xStart, xEnd) = self.limits['xNeg'], self.limits['xPos']
        xList = range(xStart, xEnd+1)
        xList = []
        yList = []
        for x in frange(xStart, xEnd+1, 0.01):
            try:
                y = app.selectedFunc(app.dev,x*self.scale)
                yList.append(y)
                xList.append(x)
            except:
                for delta in [-0.8, -0.6, -0.4, -0.1, 0, 0.1, 0.4, 0.8]:
                    if delta == 0:
                        xList.append(None)
                        yList.append(None)
                    else:
                        xd = x+delta
                        y = app.selectedFunc(app.dev,xd*self.scale)
                        yList.append(y)
                        xList.append(xd)

        for idx in range(1,len(xList)):
            if xList[idx] != None and xList[idx-1] != None and yList[idx] != None and yList[idx-1] != None:
                x0 = xList[idx-1] * self.gapSize + self.origin['x']
                y0 = -yList[idx-1] * self.gapSize/self.scale + self.origin['y']
                x1 = xList[idx] * self.gapSize + self.origin['x']
                y1 = -yList[idx] * self.gapSize/self.scale + self.origin['y']
                canvas.create_line(x0, y0,
                                    x1, y1,
                                    fill='green', 
                                    width=app.lineWidth)
        canvas.create_rectangle(400, 20, 595, 70, fill = 'white', width = 2)
        canvas.create_text(500, 45, text = f"f'(x) = {app.dev}", font = 'Arial 15 bold')

                                