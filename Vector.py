from tkinter import *
from la import Matrix
from math import *

class Vector:

    def __init__(self, canvas, master, labelRow, color, vWidth=3, tag=""):
        self.canvas = canvas['canvas']
        self.color = color
        self.vals = Matrix([[0],[0]])
        self.vWidth = vWidth
        self.vector = self.canvas.create_line(0,0,0,0, fill=color, arrow='last', width=vWidth, capstyle=ROUND, tag=tag)
        self.vector2 = None
        if labelRow != None:
            self.label = Label(master, text="", fg=color, width=20)
            self.label.grid(row=labelRow, columnspan=2)
        self.complexMode = False
        self.tag = tag

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
            self.label['text'] = '['                    \
                + str(round(c1.real, 1))                \
                + (' + ' if c1.imag  >= 0 else ' - ')   \
                + str(abs(round(c1.imag, 1))) + 'i, '   \
                + str(round(c2.real, 1))                \
                + (' + ' if c2.imag  >= 0 else ' - ')   \
                + str(abs(round(c2.imag, 1))) + 'i]^T'
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
            self.canvas.itemconfig(self.vector, arrow='none')
            self.vector2 = self.canvas.create_line(0,0,0,0, fill=self.color, arrow='none', capstyle=ROUND, width=self.vWidth, dash=[10,5], tag=self.tag)
        else:
            self.canvas.itemconfig(self.vector, arrow='last')
            self.canvas.delete(self.vector2)
            self.vector2 = None
            self.vals = Matrix([[c.real for c in row] for row in self.vals.rows()])
