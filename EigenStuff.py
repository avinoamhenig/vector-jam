from tkinter import *
from la import Matrix
from math import *
from Vector import Vector
import random

class EigenStuff:

    def __init__(self, canvas, master, evRow, probRow, color, num, ebWidth):
        self.canvas = canvas['canvas']
        self.cDiag = canvas['diagonal']
        self.color = color
        self.evLabel = Label(master, text='', fg=color, width=20)
        self.evLabel.grid(row=evRow, columnspan=2)
        self.probLabel = Label(master, text='', fg=color, width=20)
        self.probLabel.grid(row=probRow, columnspan=2)
        self.ev = self.canvas.create_line(0,0,0,0,fill=color, dash=[10,15])
        self.projEv = self.canvas.create_line(0,0,0,0, fill='cyan', arrow='last', width=1, tag='proj')
        self.projEvDash = self.canvas.create_line(0,0,0,0, fill='cyan', dash=[10,5], width=1, tag='proj')
        self.eb = Vector(canvas, master, None, color, ebWidth)
        self.num = num #for labels
        self.vals = None

    def setEvLabel(self, eigenVal):
        if eigenVal.imag == 0:
            self.evLabel['text'] = "λ" + str(self.num) + " = " + str(round(eigenVal.real, 2))
        else:
            self.evLabel['text'] = "λ" + str(self.num) + " = " + str(
                round(eigenVal.real, 2)) + ' + ' + str(round(eigenVal.imag, 2)) + 'i'

    def setProbLabel(self, prob):
        self.probLabel['text'] = 'P' + str(self.num) + ' = ' + str(round(prob, 2))

    def setVals(self, evs):
        self.vals = evs
        self.eb.setVals(evs)

    def drawLine(self, unitSize):
        cWidth = int(self.canvas['width'])
        cHeight = int(self.canvas['height'])
        x1, y1 = (-self.cDiag * self.vals).vals()
        x2, y2 = (self.cDiag * self.vals).vals()
        self.canvas.coords(self.ev,
                           cWidth/2 + x1*unitSize, cHeight/2 - y1*unitSize,
                           cWidth/2 + x2*unitSize, cHeight/2 - y2*unitSize)

    def setEvLabelBackground(self, color):
        self.evLabel['bg'] = color

    def probView(self, view):
        if view:
            self.probLabel.grid()
        else:
            self.probLabel.grid_remove()

    def drawProjections(self, x2, y2, amp, unitSize):
        cWidth = int(self.canvas['width'])
        cHeight = int(self.canvas['height'])
        x, y = (amp * self.vals).vals()
        self.canvas.coords(self.projEv,
                           cWidth/2, cHeight/2,
                           cWidth/2 + x*unitSize,
                           cHeight/2 + -y*unitSize
                           )
        self.canvas.coords(self.projEvDash,
                           cWidth/2+x*unitSize,
                           cHeight/2 + -y*unitSize,
                           cWidth/2 + x2*unitSize,
                           cHeight/2 + -y2*unitSize
                           )

    def drawEigenBasis(self, unitSize):
        self.eb.drawVector(unitSize)

    def setComplexMode(self, complexMode):
        self.eb.setComplexMode(complexMode)
        self.canvas.coords(self.ev, 0, 0, 0, 0)
