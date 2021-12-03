from cmu_112_graphics import *

class PushButton:
    def __init__(self, app, x, y, width, height, text='',
                 imagePath=None, pushedImagePath=None,
                 textColor="#808080", pushedTextColor='#FFD800'):
        # Coords
        self.x = x
        self.y = y
        # Size
        self.width = width
        self.height = height
        # Text
        self.text = text
        self.textColor = textColor
        self.pushedTextColor = pushedTextColor
        # Image
        self.image = None
        if imagePath is not None:
            self.image = app.loadImage(imagePath)
        # Pushed Image
        self.pushedImage = None
        if pushedImagePath is not None:
            self.pushedImage = app.loadImage(pushedImagePath)
    
    def draw(self, canvas):
        if self.image is not None:
            canvas.create_image(self.x+self.width//2, self.y+self.height//2,
                                image=ImageTk.PhotoImage(self.image))
        if self.text != '':
            canvas.create_text(self.x + self.width//2,
                               self.y + self.height//2,
                               text=self.text,
                               font="Arial 10 bold",
                               fill=self.textColor)
    
    def drawPushed(self, canvas):
        if self.pushedImage is not None:
            canvas.create_image(self.x+self.width//2, self.y+self.height//2,
                                image=ImageTk.PhotoImage(self.pushedImage))
        if self.text != '':
            canvas.create_text(self.x + self.width//2,
                               self.y + self.height//2,
                               text=self.text,
                               font="Arial 10 bold",
                               fill=self.pushedTextColor)
