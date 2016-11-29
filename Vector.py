from tkinter import *
from la import Matrix
from math import *

class Vector:

    def __init__(self, canvas, master, labelRow, color):
        self.canvas = canvas['canvas']
        self.color = color
        self.vals = Matrix([[0],[0]])
        self.vector = self.canvas.create_line(0,0,0,0, fill=color, arrow='last', width=3)
        self.vector2 = None
        if labelRow != None:
            self.label = Label(master, text="", fg=color, width=20)
            self.label.grid(row=labelRow, columnspan=2)
        self.complexMode = False

    def setVals(self, vals):
        self.vals = vals

    def drawVector(self, unitSize):
        cWidth = int(self.canvas['width'])
        cHeight = int(self.canvas['height'])
        if self.complexMode:
            self.canvas.coords(self.vector,
                               cWidth/2, cHeight/2,
                               cWidth/2 + self.vals.vals()[0].real*unitSize,
                               cHeight/2 + -self.vals.vals()[0].imag*unitSize
                               )
            self.canvas.coords(self.vector2,
                               cWidth/2, cHeight/2,
                               cWidth/2 + self.vals.vals()[1].real*unitSize,
                               cHeight/2 + -self.vals.vals()[1].imag*unitSize
                               )

        else:
            self.canvas.coords(self.vector,
                               cWidth/2, cHeight/2,
                               cWidth/2 + self.vals.vals()[0]*unitSize,
                               cHeight/2 + -self.vals.vals()[1]*unitSize
                               )

    def setLabel(self):
        if self.complexMode:
            c1, c2 = self.vals.vals()
            self.label['text'] = '[' + str(round(c1.real, 2)) + ' + ' + str(round(c1.imag, 2)) + 'i, ' + str(round(c2.real, 2)) + ' + ' + str(round(c2.imag, 2)) + 'i]^T'
        else:
            self.label['text'] = str([round(x, 2) for x in self.vals.vals()])+"^T"

    def setHidden(self, hide):
        show = not hide
        self.canvas.itemconfigure(self.vector, state = "normal" if show else "hidden")
        if self.complexMode:
            self.canvas.itemconfigure(self.vector2, state = "normal" if show else "hidden")

    def setComplexMode(self, complexMode):
        self.complexMode = complexMode
        if complexMode:
            self.vals = (1+0j) * self.vals
            self.vector2 = self.canvas.create_line(0,0,0,0, fill=self.color, arrow='last', width=3, dash=[10,5])
        else:
            self.vals = Matrix([[c.real for c in row] for row in self.vals.rows()])
            self.canvas.delete(self.vector2)
            self.vector2 = None
