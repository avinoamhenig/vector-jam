from tkinter import *
from la import Matrix
from math import *

class Vector:

    def __init__(self, canvas, master, labelRow, color):
        self.canvas = canvas['canvas']
        self.cWidth = canvas['width']
        self.cHeight = canvas['height']
        self.color = color
        self.vals = None
        self.vector = self.canvas.create_line(0,0,0,0, fill=color, arrow='last', width=3)
        self.label = Label(master, text="", fg=color, width=20)
        self.label.grid(row=labelRow, columnspan=2)

    def setVals(self, vals):
        #vals will be a matrix
        self.vals = vals

    def drawVector(self, unitSize):
        self.canvas.coords(self.vector,
                           self.cWidth/2, self.cHeight/2,
                           self.cWidth/2 + self.vals.vals()[0]*unitSize,
                           self.cHeight/2 + -self.vals.vals()[1]*unitSize
                           )

    def setLabel(self):
        self.label['text'] = str([round(x, 2) for x in self.vals.vals()])+"^T"

        
        
        
        

    
