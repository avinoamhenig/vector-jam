from la import Matrix
from tkinter import *


class Vector:
    def __init__(self, color, canvas, cWidth, cHeight, unitSize, vecWidth):
        self.vals = Matrix([[0],[0]])
        
        self.canvas = canvas
        self.cWidth = cWidth
        self.cHeight = cHeight
        self.unitSize = unitSize
        self.amp1 = 0
        self.amp2 = 0
        self.ev1_vals = 0
        self.ev2_vals = 0

        self.prob1=0##
        self.prob2=0##

        self.show = True
        self.complex = False 

        self.vec = self.canvas.create_line(0, 0, 0, 0, fill=color, arrow="last", width=vecWidth)

    def setVals(self, vals):
        self.vals = vals

    def setEigenVals(self, eVals):
        self.ev1_vals = eVals[0].normalize()
        self.ev2_vals = eVals[1].normalize()

    def setVector(self, vals, matrix, projected):
        self.vals = vals
        projected.vals = matrix * self.vals
        if not self.complex:
            self.calcProjections()

    def calcProjections(self):
        normalized = self.vals.normalize()
        self.amp1 = normalized.innerProduct(self.ev1_vals)
        self.amp2 = normalized.innerProduct(self.ev2_vals)
        self.prob1 = self.amp1**2
        self.prob2 = self.amp2**2

    def drawVector(self, x, y):
        self.canvas.coords(self.vec,
            self.cWidth/2, self.cHeight/2,
            self.cWidth/2 + x*self.unitSize,
            self.cHeight/2 + -y * self.unitSize
        )

    def toggleVector(self):
        self.show = not self.show
        self.canvas.itemconfigure(self.vec, state="normal" if self.show else "hidden")
    

    def toggleComplex(self):
        self.complex = not self.complex
    
        
        
