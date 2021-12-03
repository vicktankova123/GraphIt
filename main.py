import math
import random
import tkinter as tk
import sympy

from cmu_112_graphics import *
from equations import *
from buttons import PushButton
from grid import Grid 
from matrix import matCol
from palette import Palette
from rendertools import RenderTool

#citations:
# 2D design: Desmos 
# keyboard design: Albert Xu 15-112 Fall 2018 project video (no code just visual)
# 3D:
# all videos below used pygame 
#https://www.youtube.com/watch?v=qw0oY6Ld-L0 
#https://www.youtube.com/watch?v=sQDFydEtBLE 
#https://www.youtube.com/watch?v=sSQIwIx8uT4 
#matrix operations:
#https://www.kite.com/python/answers/how-to-transpose-a-matrix-in-python
#https://www.journaldev.com/32984/numpy-matrix-transpose-array
#https://stackoverflow.com/questions/1828233/optimized-dot-product-in-python

def appStarted(app):
    # Modes 
    app.isFirstScreen = True
    app.board = False 
    app.tDMode = False
    app.squareBoard = False

    # Grid
    app.origin = dict(x=550,y=320)
    app.scale = 1
    app.lineWidth = 3
    app.lineColour = "red"
    app.grid = Grid(0,0,app.width, app.height)

    # Splash screen
    app.introPic = app.loadImage("images/equations_whiteboard.jpeg")
    app.introPicScaled = app.scaleImage(app.introPic, 1/4)
    app.name = app.loadImage("images/Снимок экрана 2021-11-15 в 21.08.30.png")
    app.nameScaled = app.scaleImage(app.name, 19/39)

    # Buttons
    app.twoDButtons = define2DButtons(app)
    app.kbButtons = kbButtons(app)
    app.startButtons = startButtons(app)
    app.threeDButtons = define3DButtons(app)
    app.pushedButton = None

    # Plot functions
    app.drawnFunction = ''
    app.inputFunction = ''
    app.customFuncStr = ''
    app.selectedFunc = customFunc
    app.isPlot = False

    #keyboard
    app.showKeyboard = False
    app.keyboard = Keyboard(0,0,app.width, app.height)

    # 3D
    app.palette = Palette()
    app.renderTool = RenderTool()

    app.clickAnchor = [app.width//2, app.height//2]
    app.rot3D = [0., 0.]  # in degrees
    app.cubeScale = 100.

    app.limits3D = [-5, -5]
    app.scale3D = 20. # float 
    app.pointCloud = None

    #derivative 
    app.isDerivative = False
    app.dev = None
    app.isxDev = False
    app.xDev = None
    app.isyDev = False
    app.yDev = None

def drawFirstScreen(app, canvas):
    canvas.create_image(app.width//2, app.height//2, 
                        image=ImageTk.PhotoImage(app.introPicScaled))
    canvas.create_rectangle(app.width/4, app.height/4, app.width*3/4, 
                            app.height*4/9, fill = "white" , width = 7)
    canvas.create_image(app.width//2, app.height*25/72, 
                        image = ImageTk.PhotoImage(app.nameScaled))

# Typing in func
def drawTextFunction(app, canvas):
    canvas.create_text(app.width//2, app.height//2 - 75, text = app.drawnFunction , 
                        font = "Arial 22 bold", fill = 'black')

################################  buttons   ####################################

def startButtons(app):
    startButtons = dict()
    startButtons['graph'] = PushButton(app, 
                                x=225, y=app.height*5/8, 
                                width=150, height=45,
                                imagePath='images/Снимок экрана 2021-11-18 в 23.57.26.png',
                                pushedImagePath='images/Снимок экрана 2021-11-18 в 23.57.42.png')
    return startButtons

def drawStartButtons(app,canvas):
    for name, button in app.startButtons.items():
        if button == app.pushedButton:
            button.drawPushed(canvas)
        else:
            button.draw(canvas)

def define2DButtons(app):
    twoDButtons = dict()

    twoDButtons['zoomIn'] = PushButton(app, 
                                x=app.width-50, y=app.height-50, 
                                width=30, height=30,
                                imagePath='images/zoom_in_button_1.png',
                                pushedImagePath='images/zoom_in_button_2.png')
    twoDButtons['zoomOut'] = PushButton(app,
                                    x=app.width-50, y=app.height-100, 
                                    width=30, height=30,
                                    imagePath='images/zoom_out_button_1.png',
                                    pushedImagePath='images/zoom_out_button_2.png')
    twoDButtons['keyboard'] = PushButton(app,
                                    x=20, y=app.height-70, 
                                    width=75, height=50,
                                imagePath='images/keyboard.png')
    twoDButtons['3Dmode'] = PushButton(app,
                                    x=20, y=20, 
                                    width=50, height=50,
                                text='3D Mode',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    twoDButtons['2Dmode'] = PushButton(app,
                                    x=80, y=20, 
                                    width=50, height=50,
                                text='2D Mode',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    twoDButtons['derivative'] = PushButton(app,
                                    x=app.width-50, y=app.height-200, 
                                    width=30, height=70,
                                text='d\n__\ndx',
                                imagePath='images/func_button_1 — копия.png',
                                pushedImagePath='images/func_button_2 — копия.png')
    
    
    return twoDButtons

def draw2DButtons(app, canvas):
    for name, button in app.twoDButtons.items():
        if button == app.pushedButton:
            button.drawPushed(canvas)
        else:
            button.draw(canvas)

def define3DButtons(app):
    threeDButtons = dict()
    threeDButtons['keyboard'] = PushButton(app,
                                        x=20, y=app.height-70, 
                                    width=75, height=50,
                                    imagePath='images/keyboard.png')
    threeDButtons['3Dmode'] = PushButton(app,
                                    x=20, y=20, 
                                    width=50, height=50,
                                text='3D Mode',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    threeDButtons['2Dmode'] = PushButton(app,
                                    x=80, y=20, 
                                    width=50, height=50,
                                text='2D Mode',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    threeDButtons['derivative'] = PushButton(app,
                                    x=app.width-50, y=app.height-200, 
                                    width=30, height=70,
                                text='d\n__\ndx',
                                imagePath='images/func_button_1 — копия.png',
                                pushedImagePath='images/func_button_2 — копия.png')
    threeDButtons['yderivative'] = PushButton(app,
                                    x=app.width-50, y=app.height-100, 
                                    width=30, height=70,
                                text='d\n__\ndy',
                                imagePath='images/func_button_1 — копия.png',
                                pushedImagePath='images/func_button_2 — копия.png')
    return threeDButtons

def draw3DButtons(app, canvas):
    for name, button in app.threeDButtons.items():
        if button == app.pushedButton:
            button.drawPushed(canvas)
        else:
            button.draw(canvas)

def kbButtons(app):
    kbButtons = dict() 

    # Running 
    kbButtons['exit'] = PushButton(app, x=540, y=10, 
                                width=50, height=50,
                                text='X',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['go'] = PushButton(app, x=540, y=70, 
                                width=50, height=50,
                                text='go',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')   

    #Trig(ish)
    kbButtons['sine'] = PushButton(app, x=0, y=370, 
                                width=50, height=50,
                                text='sin',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['cosine'] = PushButton(app, x=60, y=370, 
                                width=50, height=50,
                                text='cos',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['tan'] = PushButton(app, x=120, y=370, 
                                width=50, height=50,
                                text='tan',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['csc'] = PushButton(app, x=0, y=430, 
                                width=50, height=50,
                                text='csc',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['sec'] = PushButton(app, x=60, y=430, 
                                width=50, height=50,
                                text='sec',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['cot'] = PushButton(app, x=120, y=430, 
                                width=50, height=50,
                                text='cot',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['exp'] = PushButton(app, x=0, y=490, 
                                width=50, height=50,
                                text='exp',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['ln'] = PushButton(app, x=60, y=490, 
                                width=50, height=50,
                                text='log',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['abs'] = PushButton(app, x=120, y=490, 
                                width=50, height=50,
                                text='abs',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    
    #Nums
    kbButtons['1'] = PushButton(app, x=180, y=370, 
                                width=50, height=50,
                                text='1',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    kbButtons['2'] = PushButton(app, x=240, y=370, 
                                width=50, height=50,
                                text='2',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')  
    kbButtons['3'] = PushButton(app, x=300, y=370, 
                                width=50, height=50,
                                text='3',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    kbButtons['4'] = PushButton(app, x=180, y=430, 
                                width=50, height=50,
                                text='4',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    kbButtons['5'] = PushButton(app, x=240, y=430, 
                                width=50, height=50,
                                text='5',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')  
    kbButtons['6'] = PushButton(app, x=300, y=430, 
                                width=50, height=50,
                                text='6',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')                              
    kbButtons['7'] = PushButton(app, x=180, y=490, 
                                width=50, height=50,
                                text='7',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    kbButtons['8'] = PushButton(app, x=240, y=490, 
                                width=50, height=50,
                                text='8',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')  
    kbButtons['9'] = PushButton(app, x=300, y=490, 
                                width=50, height=50,
                                text='9',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')   
    kbButtons['0'] = PushButton(app, x=360, y=370, 
                                width=50, height=50,
                                text='0',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')    
    kbButtons['('] = PushButton(app, x=360, y=430, 
                                width=50, height=50,
                                text='(',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')  
    kbButtons[')'] = PushButton(app, x=360, y=490, 
                                width=50, height=50,
                                text=')',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png') 
    
    #operations 
    kbButtons['power'] = PushButton(app, x=420, y=370, 
                                width=50, height=50,
                                text='^',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['plus'] = PushButton(app, x=420, y=430, 
                                width=50, height=50,
                                text='+',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['minus'] = PushButton(app, x=420, y=490, 
                                width=50, height=50,
                                text='-',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['divide'] = PushButton(app, x=480, y=370, 
                                width=50, height=50,
                                text='/',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['multiply'] = PushButton(app, x=480, y=430, 
                                width=50, height=50,
                                text='*',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')

    #Variables
    kbButtons['pi'] = PushButton(app, x=480, y=490, 
                                width=50, height=50,
                                text='π',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png') 
    kbButtons['y'] = PushButton(app, x=540, y=310, 
                                width=50, height=50,
                                text='y',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['x'] = PushButton(app, x=480, y=310, 
                                width=50, height=50,
                                text='x',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['backspace'] = PushButton(app, x=540, y=430, 
                                width=50, height=50,
                                text='<--',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['sqrt'] = PushButton(app, x=540, y=370, 
                                width=50, height=50,
                                text='√',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png') 
    kbButtons['clear'] = PushButton(app, x=540, y=490, 
                                width=50, height=50,
                                text='clear',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    kbButtons['norm'] = PushButton(app, x=0, y=310, 
                                width=50, height=50,
                                text='normal',
                                imagePath='images/func_button_1.png',
                                pushedImagePath='images/func_button_2.png')
    return kbButtons

def drawKbButtons(app,canvas):
    for name, button in app.kbButtons.items():
        if button == app.pushedButton:
            button.drawPushed(canvas)
        else:
            button.draw(canvas)

#Was button pressed?
def isPointInButton(x, y, button):
    if x > button.x and\
       x <  button.x+button.width and\
       y > button.y and\
       y < button.y+button.height:
        return True
    return False

################################################################################

#################################    3D     ####################################

def paintDot(canvas, x, y, r, color):
    canvas.create_oval(x-r, y-r,
                       x+r, y+r, 
                       fill=color, outline=color)

def paintLine(canvas, p1, p2, color, lineWidth=1):
    x1, y1 = p1
    x2, y2 = p2
    canvas.create_line(x1, y1, x2, y2, fill=color, width=lineWidth)

#Sphere test: 
def createSphere(app, minVal, maxVal, radius):
    radius = 10
    limits = [minVal, maxVal]

    # find pts which we graph
    rangeList = []
    step = 0.5
    value = limits[0]
    while value < limits[1]:
        rangeList.append(value)
        value += step

    points3D = []
    for x in rangeList:
        for y in rangeList:
            try:
                z = math.sqrt(radius*radius - x*x - y*y)
                points3D.append([x, z, -y])
                points3D.append([x, -z, -y])
            except:
                continue

    yVals = matCol(points3D, 1)
    minY, maxY = min(yVals), max(yVals)

    colors = []
    for x, y, z in points3D:
        colors.append(app.palette.getColorHexStr(y, minY, maxY))
    
    return dict(points=points3D, colors=colors)

#Function from kb input
def randomFunction(app, minVal, maxVal, func):
    # dimensions of grid (maybe change)
    limits = [minVal, maxVal]

    rangeList = []
    step = 0.25
    value = limits[0]
    while value < limits[1]:
        rangeList.append(value)
        value += step

    points3D = []
    for x in rangeList:
        for y in rangeList:
            try:
                if 'csc' in func:
                    func = func.replace('csc', '1/sin')
                if 'sec' in func:
                    func = func.replace('sec', '1/cos')
                if 'cot' in func:
                    func = func.replace('cot', '1/tan')
                z = eval(func)
                points3D.append([x, -z, y])
            except:
                continue
    
    yVals = matCol(points3D, 1)
    if yVals != []:
        minY, maxY = min(yVals), max(yVals)

    colors = []
    for x, y, z in points3D:
        colors.append(app.palette.getColorHexStr(y, minY, maxY))   

    return dict(points=points3D, colors=colors)

def renderGrid3D(app, canvas):
    limits = [-15, 15]

    xAngle = app.rot3D[0]
    yAngle = app.rot3D[1]

    grid3D = []
    for s in range(limits[0], limits[1]):
        grid3D.append([s, 0, limits[0]])
        grid3D.append([s, 0, limits[1]])
        grid3D.append([limits[0], 0, s])
        grid3D.append([limits[1], 0, s])

    grid3D.append([0, limits[0], 0])
    grid3D.append([0, limits[1], 0])

    grid3DRot = app.renderTool.rotate3DPoints(grid3D, yAngle, xAngle, 0.)
    grid3DProj = app.renderTool.project3Dto2D(grid3DRot, scale=20.)
    grid3DProj = app.renderTool.trans2D(grid3DProj, app.width//2, app.height//2)

    for idx in range(1, len(grid3DProj), 2):
        x0, y0, z0 = grid3D[idx-1]
        lineWidth = 1
        color = '#D3D3D3'
        # if x0 % 5 == 0 or z0 % 5 == 0:
        #     lineWidth = 1
        if x0 == 0 or z0 == 0:
            lineWidth = 3
            color = 'black'
        
        paintLine(canvas, grid3DProj[idx-1], grid3DProj[idx], 
                  color, lineWidth)

def renderPointCloud(app, canvas):
    if app.pointCloud != None:
        # Set the center of the projected render on screen
        cx, cy = app.width//2, app.height//2

        # Rotation angle according to X and Y movement of the mouse
        xAngle = app.rot3D[0]
        yAngle = app.rot3D[1]

        # Load 3D points and rotate
        points3D = app.pointCloud['points']
        points3DRot = app.renderTool.rotate3DPoints(points3D, yAngle, xAngle, 0.)

        # Project the rotated 3D points into 2D for display on screen
        points2D = app.renderTool.project3Dto2D(points3DRot, scale=20.)

        # Translate the projected points to the area where we want to render
        points2D = app.renderTool.trans2D(points2D, cx, cy)

        # Paint point cloud as dots
        for idx in range(len(points3D)):
            x, y = points2D[idx]
            paintDot(canvas, x, y, 2, app.pointCloud['colors'][idx])
        
        # Paint dot connections as lines
        if 'conns' in app.pointCloud:
            for i, j in app.pointCloud['conns']:
                paintLine(canvas, points2D[i], points2D[j], app.pointCloud['colors'][i])

def createNormal3D(app, minVal, maxVal):
    radius = 10
    limits = [minVal, maxVal]

    rangeList = []
    step = 0.25
    value = limits[0]
    while value < limits[1]:
        rangeList.append(value)
        value += step

    mean = [0, 0]
    covar = [[1, 0],
             [0, 1]]
    points3D = []
    for x in rangeList:
        for y in rangeList:
            try:
                z = bivarNormal([x, y], 25, mean, covar)
                points3D.append([x, z, -y])  # When plotting Y-axis is vertical
            except:
                continue

    yVals = matCol(points3D, 1)
    minY, maxY = min(yVals), max(yVals)

    colors = []
    for x, y, z in points3D:
        colors.append(app.palette.getColorHexStr(y, minY, maxY))
    
    return dict(points=points3D, colors=colors)

################################################################################

################################ derivatives ###################################

#all derivative operations from: https://www.askpython.com/python/examples/derivatives-in-python-sympy
#                                https://stackoverflow.com/questions/30791504/python-partial-derivatives-easy
def getDerivative(app, func):
    x = sympy.Symbol('x')
    if func != '':
        if 'csc' in func:
            i = func.find('csc')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sec' in func:
            i = func.find('sec')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'cot' in func:
            i = func.find('cot')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sin' in func:
            i = func.find('sin')
            func = func[:i] + 'sympy.' +func[i:]
        if 'cos' in func:
            i = func.find('cos')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'tan' in func:
            i = func.find('tan')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'log' in func:
            i = func.find('log')
            func = func[:i] + 'sympy.' +func[i:]  
        if 'sqrt' in func:
            i = func.find('sqrt')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'exp' in func:
            i = func.find('exp')
            func = func[:i] + 'sympy.' +func[i:]     
        f = eval(func)
        derivative = f.diff(x)
        return str(derivative)

def getxDev(app,func):
    if func != '':
        if 'csc' in func:
            i = func.find('csc')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sec' in func:
            i = func.find('sec')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'cot' in func:
            i = func.find('cot')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sin' in func:
            i = func.find('sin')
            func = func[:i] + 'sympy.' +func[i:]
        if 'cos' in func:
            i = func.find('cos')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'tan' in func:
            i = func.find('tan')
            func = func[:i] + 'sympy.' +func[i:]  
        if 'log' in func:
            i = func.find('log')
            func = func[:i] + 'sympy.' +func[i:]
        if 'sqrt' in func:
            i = func.find('sqrt')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'exp' in func:
            i = func.find('exp')
            func = func[:i] + 'sympy.' +func[i:]     
        x, y = sympy.symbols('x y', real = True)
        f = eval(func)
        return str(sympy.diff(f, x))

def getyDev(app,func):
    if func != '':
        if 'csc' in func:
            i = func.find('csc')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sec' in func:
            i = func.find('sec')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'cot' in func:
            i = func.find('cot')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sin' in func:
            i = func.find('sin')
            func = func[:i] + 'sympy.' +func[i:]
        if 'cos' in func:
            i = func.find('cos')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'tan' in func:
            i = func.find('tan')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'log' in func:
            i = func.find('log')
            func = func[:i] + 'sympy.' +func[i:] 
        if 'sqrt' in func:
            i = func.find('sqrt')
            func = func[:i] + 'sympy.' +func[i:]   
        if 'exp' in func:
            i = func.find('exp')
            func = func[:i] + 'sympy.' +func[i:]    
        x, y = sympy.symbols('x y', real = True)
        f = eval(func)
        return str(sympy.diff(f, y))
################################################################################
       
def mousePressed(app, event):
    # Set the anchor point for the mouse drag 3D
    app.clickAnchor = [event.x, event.y]
    
    #init
    if isPointInButton(event.x, event.y, app.startButtons['graph']):
        app.pushedButton = app.startButtons['graph']
        app.isFirstScreen = False
        app.board = True
    
    #2D Mode
    if app.board and app.tDMode == False and app.showKeyboard == False:
        if isPointInButton(event.x, event.y, app.twoDButtons['zoomIn']):
            app.pushedButton = app.twoDButtons['zoomIn']
            app.scale = app.scale / 2
            app.grid.setScale(app.scale)
        elif isPointInButton(event.x, event.y, app.twoDButtons['zoomOut']):
            app.pushedButton = app.twoDButtons['zoomOut']
            app.scale = app.scale * 2
            app.grid.setScale(app.scale)
        elif isPointInButton(event.x, event.y, app.twoDButtons['derivative']):
            app.pushedButton = app.twoDButtons['derivative']
            if app.isDerivative == False:
                app.isDerivative = True
                app.dev = getDerivative(app, app.customFuncStr)
            else:
                app.isDerivative = False
        elif isPointInButton(event.x, event.y, app.twoDButtons['keyboard']):
            app.pushedButton = app.twoDButtons['keyboard']
            app.showKeyboard = True
            app.isDerivative = False
            app.isPlot = False
        elif isPointInButton(event.x, event.y, app.threeDButtons['keyboard']):
            app.pushedButton = app.threeDButtons['keyboard']
            app.showKeyboard = True
            app.isPlot = False
        elif isPointInButton(event.x, event.y, app.twoDButtons['3Dmode']):
            app.pushedButton = app.twoDButtons['3Dmode']
            app.customFuncStr = ''
            app.tDMode = True
        elif isPointInButton(event.x, event.y, app.twoDButtons['2Dmode']):
            app.pushedButton = app.twoDButtons['2Dmode']
            app.customFuncStr = ''
            app.tDMode = False 
            app.board = True
        elif isPointInButton(event.x, event.y, app.threeDButtons['3Dmode']):
            app.pushedButton = app.threeDButtons['3Dmode']
            app.customFuncStr = ''
            app.tDMode = True
            app.board = False

    #3D buttons  
    if app.tDMode and app.showKeyboard == False:
        if isPointInButton(event.x, event.y, app.twoDButtons['keyboard']):
            app.pushedButton = app.twoDButtons['keyboard']
            app.showKeyboard = True
        elif isPointInButton(event.x, event.y, app.threeDButtons['2Dmode']):
            app.pushedButton = app.threeDButtons['2Dmode']
            app.drawnFunction = ''
            app.customFuncStr = ''
            app.tDMode = False 
            app.board = True
        elif isPointInButton(event.x, event.y, app.threeDButtons['2Dmode']):
            app.pushedButton = app.threeDButtons['2Dmode']
            app.customFuncStr = ''
            app.tDMode = False 
            app.board = True
        elif isPointInButton(event.x, event.y, app.threeDButtons['derivative']):
            app.pushedButton = app.threeDButtons['derivative']
            if app.isDerivative == False:
                app.isxDev = True
                app.xDev = getxDev(app,app.customFuncStr)
                app.pointCloud = randomFunction(app, -14, 14, app.xDev)
                app.scale3D = 25
            else:
                app.isxDev = False
        elif isPointInButton(event.x, event.y, app.threeDButtons['yderivative']):
            app.pushedButton = app.threeDButtons['yderivative']
            if app.isyDev == False:
                app.isyDev = True
                app.yDev = getyDev(app,app.customFuncStr)
                app.pointCloud = randomFunction(app, -14, 14, app.yDev)
                app.scale3D = 25
            else:
                app.isxDev = False

    #keyboard
    if app.showKeyboard:
        if isPointInButton(event.x, event.y, app.kbButtons['exit']):
            app.pushedButton = app.kbButtons['exit']
            app.showKeyboard = False
        if isPointInButton(event.x, event.y, app.kbButtons['backspace']):
            app.pushedButton = app.kbButtons['backspace']
            app.drawnFunction = app.drawnFunction[:-1]
        if isPointInButton(event.x, event.y, app.kbButtons['sine']):
            app.pushedButton = app.kbButtons['sine']
            app.drawnFunction += "sin"
        elif isPointInButton(event.x, event.y, app.kbButtons['cosine']):
            app.pushedButton = app.kbButtons['cosine']
            app.drawnFunction += "cos"
        elif isPointInButton(event.x, event.y, app.kbButtons['tan']):
            app.pushedButton = app.kbButtons['tan']
            app.drawnFunction += "tan"
        elif isPointInButton(event.x, event.y, app.kbButtons['csc']):
            app.pushedButton = app.kbButtons['csc']
            app.drawnFunction += "csc"
        elif isPointInButton(event.x, event.y, app.kbButtons['sec']):
            app.pushedButton = app.kbButtons['sec']
            app.drawnFunction += "sec"
        elif isPointInButton(event.x, event.y, app.kbButtons['cot']):
            app.pushedButton = app.kbButtons['cot']
            app.drawnFunction += "cot"
        elif isPointInButton(event.x, event.y, app.kbButtons['exp']):
            app.pushedButton = app.kbButtons['exp']
            app.drawnFunction += "exp"
        elif isPointInButton(event.x, event.y, app.kbButtons['ln']):
            app.pushedButton = app.kbButtons['ln']
            app.drawnFunction += "log"
        elif isPointInButton(event.x, event.y, app.kbButtons['abs']):
            app.pushedButton = app.kbButtons['abs']
            app.drawnFunction += "abs"

        #numbers
        elif isPointInButton(event.x, event.y, app.kbButtons['1']):
            app.pushedButton = app.kbButtons['1']
            app.drawnFunction += "1"
        elif isPointInButton(event.x, event.y, app.kbButtons['2']):
            app.pushedButton = app.kbButtons['2']
            app.drawnFunction += "2"
        elif isPointInButton(event.x, event.y, app.kbButtons['3']):
            app.pushedButton = app.kbButtons['3']
            app.drawnFunction += "3"
        elif isPointInButton(event.x, event.y, app.kbButtons['4']):
            app.pushedButton = app.kbButtons['4']
            app.drawnFunction += "4"
        elif isPointInButton(event.x, event.y, app.kbButtons['5']):
            app.pushedButton = app.kbButtons['5']
            app.drawnFunction += "5"
        elif isPointInButton(event.x, event.y, app.kbButtons['6']):
            app.pushedButton = app.kbButtons['6']
            app.drawnFunction += "6"
        elif isPointInButton(event.x, event.y, app.kbButtons['7']):
            app.pushedButton = app.kbButtons['7']
            app.drawnFunction += "7"
        elif isPointInButton(event.x, event.y, app.kbButtons['8']):
            app.pushedButton = app.kbButtons['8']
            app.drawnFunction += "8"
        elif isPointInButton(event.x, event.y, app.kbButtons['9']):
            app.pushedButton = app.kbButtons['9']
            app.drawnFunction += "9"
        elif isPointInButton(event.x, event.y, app.kbButtons['0']):
            app.pushedButton = app.kbButtons['0']
            app.drawnFunction += "0"
        elif isPointInButton(event.x, event.y, app.kbButtons['(']):
            app.pushedButton = app.kbButtons['(']
            app.drawnFunction += "("
        elif isPointInButton(event.x, event.y, app.kbButtons[')']):
            app.pushedButton = app.kbButtons[')']
            app.drawnFunction += ")"

        #operations
        elif isPointInButton(event.x, event.y, app.kbButtons['power']):
                app.pushedButton = app.kbButtons['power']
                app.drawnFunction += "**"
        elif isPointInButton(event.x, event.y, app.kbButtons['plus']):
                app.pushedButton = app.kbButtons['plus']
                app.drawnFunction += "+"
        elif isPointInButton(event.x, event.y, app.kbButtons['minus']):
                app.pushedButton = app.kbButtons['minus']
                app.drawnFunction += "-"
        elif isPointInButton(event.x, event.y, app.kbButtons['divide']):
                app.pushedButton = app.kbButtons['divide']
                app.drawnFunction += "/"
        elif isPointInButton(event.x, event.y, app.kbButtons['multiply']):
                app.pushedButton = app.kbButtons['multiply']
                app.drawnFunction += "*"
        elif isPointInButton(event.x, event.y, app.kbButtons['pi']):
                app.pushedButton = app.kbButtons['pi']
                app.drawnFunction += "π"
        elif isPointInButton(event.x, event.y, app.kbButtons['x']):
                app.pushedButton = app.kbButtons['x']
                app.drawnFunction += "x"
        elif isPointInButton(event.x, event.y, app.kbButtons['y']):
                app.pushedButton = app.kbButtons['y']
                app.drawnFunction += "y"
        elif isPointInButton(event.x, event.y, app.kbButtons['sqrt']):
                app.pushedButton = app.kbButtons['sqrt']
                app.drawnFunction += "sqrt"
        elif isPointInButton(event.x, event.y, app.kbButtons['clear']):
                app.pushedButton = app.kbButtons['clear']
                app.drawnFunction = ""
        elif isPointInButton(event.x, event.y, app.kbButtons['norm']):
                app.pushedButton = app.kbButtons['norm']
                if app.tDMode:
                    app.pointCloud = createNormal3D(app, -10, 10)
                    app.scale3D = 25
                    app.showKeyboard = False
        elif isPointInButton(event.x, event.y, app.kbButtons['go']):
                app.pushedButton = app.kbButtons['go']
                app.showKeyboard = False
                app.isPlot = True
                if app.tDMode:
                    app.pointCloud = randomFunction(app, -14, 14, app.customFuncStr)
                    app.scale3D = 25
                    app.tDMode = True

        app.customFuncStr = app.drawnFunction

def mouseReleased(app, event):
    app.pushedButton = None

def mouseDragged(app, event):
    # Calculate the deltas in both directions
    dX = app.clickAnchor[0] - event.x
    dY = app.clickAnchor[1] - event.y

    # Rotation
    dXDeg = - 360 * dX/app.width
    dYDeg = 360 * dY/app.height
    app.rot3D = [app.rot3D[0] + dXDeg,
                 app.rot3D[1] + dYDeg]

    # Update anchor for next drag event
    app.clickAnchor = [event.x, event.y]

def keyPressed(app, event):   
    if event.key == '1':
        app.drawnFunction += '1'
    if event.key == '2':
        app.drawnFunction += '2'
    if event.key == '3':
        app.drawnFunction += '3'
    if event.key == '4':
        app.drawnFunction += '4'
    if event.key == '5':
        app.drawnFunction += '5'
    if event.key == '6':
        app.drawnFunction += '6'
    if event.key == '7':
        app.drawnFunction += '7'
    if event.key == '8':
        app.drawnFunction += '8'
    if event.key == '9':
        app.drawnFunction += '9'
    if event.key == '0':
        app.drawnFunction += '0'
    if event.key == '(':
        app.drawnFunction += '('
    if event.key == ')':
        app.drawnFunction += ')'
    if event.key == '/':
        app.drawnFunction += '/'
    if event.key == '-':
        app.drawnFunction += '-'
    if event.key == '+':
        app.drawnFunction += '+'
    if event.key == '=':
        app.drawnFunction += '='
    if event.key == 'x':
        app.drawnFunction += 'x'
    if event.key == 'y':
        app.drawnFunction += 'y'

def redrawAll(app, canvas):
    if (app.isFirstScreen):
        drawFirstScreen(app, canvas)
        drawStartButtons(app,canvas)
    if app.squareBoard == True:
        squareBoard(app,canvas)
    if app.board:
        # Select if we want to plot in 3D or 2D
        if app.tDMode:
            draw3DButtons(app, canvas)
            renderGrid3D(app, canvas)
            renderPointCloud(app, canvas)
            if app.isxDev and app.showKeyboard == False:
                renderPointCloud(app, canvas)

            if app.showKeyboard:
                app.keyboard.draw(canvas)
                drawKbButtons(app,canvas)
                drawTextFunction(app, canvas)
        else:
            if app.showKeyboard:
                app.keyboard.draw(canvas)
                drawKbButtons(app,canvas)
                drawTextFunction(app, canvas)
            else:
                app.grid.draw(canvas)         
                draw2DButtons(app, canvas)
            if app.isPlot:
                app.grid.plotFunction(app, canvas)
            if app.isDerivative and app.showKeyboard == False:
                app.grid.plotDerivative(app,canvas)
            
runApp(width = 600, height = 600)
