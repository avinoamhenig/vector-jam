from tkinter import *
from la import Matrix
from math import *
import random

class EigenStuff:

    def __init__(self, canvas, master, evRow, probRow, color, num):
        self.canvas = canvas['canvas']
        self.cWidth = canvas['width']
        self.cHeight = canvas['height']
        self.cDiag = canvas['diagonal']
        self.color = color
        self.evLabel = Label(master, text='', fg=color, width=20)
        self.evLabel.grid(row=evRow, columnspan=2)
        self.probLabel = Label(master, text='', fg=color, width=20)
        self.probLabel.grid(row=probRow, columnspan=2)
        self.ev = self.canvas.create_line(0,0,0,0,fill=color, dash=[10,15])
        self.projEv = self.canvas.create_line(0,0,0,0, fill='cyan', arrow='last', width=1, tag='proj')
        self.projEvDash = self.canvas.create_line(0,0,0,0, fill='cyan', dash=[10,5], width=1, tag='proj')
        self.eb = self.canvas.create_line(0,0,0,0, fill='magenta', arrow='last', width=1) #able to make visible/not?
        self.num = num #for labels
        self.vals = None

    def setEvLabel(self, eigenVal):
        self.evLabel['text'] = "λ" + str(self.num) + " = " +str(
          round(eigenVal.real, 4) + eigenVal.imag*1j)

    def setProbLabel(self, prob):
        self.probLabel['text'] = 'P' + str(self.num) + ' = ' + str(round(prob, 4))

    def setVals(self, evs):
        self.vals = evs

    def drawLine(self, unitSize):
        x1, y1 = (-self.cDiag * self.vals).vals()
        x2, y2 = (self.cDiag * self.vals).vals()
        self.canvas.coords(self.ev,
                           self.cWidth/2 + x1*unitSize, self.cHeight/2 - y1*unitSize,
                           self.cWidth/2 + x2*unitSize, self.cHeight/2 - y2*unitSize)
        
    def setEvLabelBackground(self, color):
        self.evLabel['bg'] = color

    def probView(self, view):
        if view:
            self.probLabel.grid()
        else:
            self.probLabel.grid_remove()

    def drawProjections(self, x2, y2, amp, unitSize):
        x, y = (amp * self.vals).vals()
        self.canvas.coords(self.projEv,
                           self.cWidth/2, self.cHeight/2,
                           self.cWidth/2 + x*unitSize,
                           self.cHeight/2 + -y*unitSize
                           )
        self.canvas.coords(self.projEvDash,
                           self.cWidth/2+x*unitSize,
                           self.cHeight/2 + -y*unitSize,
                           self.cWidth/2 + x2*unitSize,
                           self.cHeight/2 + -y2*unitSize
                           )

    def drawEigenBasis(self, unitSize):
        x, y = self.vals.vals()
        self.canvas.coords(self.eb,
                           self.cWidth/2, self.cHeight/2,
                           self.cWidth/2 + x*unitSize,
                           self.cHeight/2 - y*unitSize
                           )
