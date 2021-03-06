from tkinter import *
from la import Matrix
from math import *
import random
from PIL import Image, ImageTk
from Vector import Vector
from EigenStuff import EigenStuff

class App:
    def __init__(self, master):
        self.cWidth = 800
        self.cHeight = 600
        self.unitSize = 100
        self.cDiag = sqrt(self.cWidth**2 + self.cHeight**2)

        # Logo
        logoImage = Image.open("vector-jam-logo@2x.jpg")
        logoImage = logoImage.resize((200, 70), Image.ANTIALIAS)
        self.logoPhoto = logoPhoto = ImageTk.PhotoImage(logoImage)
        logoCanvas = Canvas(master, width=220, height=100)
        logoCanvas.grid(row=0, column=0, columnspan=2)
        logoCanvas.create_image(10, 15, image=logoPhoto, anchor=NW)

        #Matrix entry objects
        self.a = Entry(master, bd = 5, width=5)
        self.b = Entry(master, bd = 5, width=5)
        self.c = Entry(master, bd = 5, width=5)
        self.d = Entry(master, bd = 5, width=5)

        #Matrix grid layout
        self.a.grid(row=1, column=0)
        self.b.grid(row=1, column=1)
        self.c.grid(row=2, column=0)
        self.d.grid(row=2, column=1)

        #Canvas
        self.canvas = Canvas(master, width=self.cWidth, height=self.cHeight)
        self.canvas.grid(row=0, column=3, rowspan=31, sticky="SNEW")
        self.canvas.bind("<ButtonPress-1>", self.onMouseDown)
        self.canvas.bind("<B1-Motion>", self.onMouseMove)
        self.canvas.bind('<Configure>', self.canvasResize)

        self.canvasInfo = {"canvas":self.canvas,
                           "width":self.cWidth,
                           "height":self.cHeight,
                           "diagonal":self.cDiag
                           }

        #Buttons
        update = Button(master, text="Update", command=
            lambda: self.setMatrix(Matrix([
                [eval(self.a.get().replace('i', 'j')),
                 eval(self.b.get().replace('i', 'j'))],
                [eval(self.c.get().replace('i', 'j')),
                 eval(self.d.get().replace('i', 'j'))]
            ]))
        )
        update.grid(row=3, column=0)
        submit = Button(master, text="Adjoint", command = self.adjoint)
        submit.grid(row=3, column=1)
        self.stepButton = Button(master, text="Step", command = self.step)
        self.stepButton.grid(row=5, column=1)
        self.stepBackButton = Button(master, text="Step Back", command = self.stepBack)
        self.stepBackButton.grid(row=5, column=0)
        self.productVectorToggle = Checkbutton(master,
            text="Show product vector?", command=self.toggleProductVector)
        self.productVectorToggle.deselect()
        self.productVectorToggle.grid(row=18, column=0, columnspan=3)
        self.showProductVector = False
        self.projToggle = Checkbutton(master,
            text="Show inner products?", command=self.toggleProj)
        self.projToggle.deselect()
        self.projToggle.grid(row=19, column=0, columnspan=3)
        self.showProj = False
        self.eigenToggle = Checkbutton(master,
            text="Show eigenbasis?", command=self.toggleEigen)
        self.eigenToggle.deselect()
        self.eigenToggle.grid(row=20, column=0, columnspan=3)
        self.showEigen = False

        self.normalizeVectorButton = Button(master, text="Normalize Vector", command=self.normalizeVector)
        self.normalizeVectorButton.grid(row=21, columnspan=2)

        self.measureButton = Button(master, text="Measure", command=self.performMeasurement)
        self.measureButton.grid(row=22, columnspan=2)

        self.complexPlaneToggle = Checkbutton(master,
            text="Complex Plane", command=self.complexTransform)
        self.complexPlaneToggle.deselect()
        self.complexPlaneToggle.grid(row=29, columnspan=3)

        self.qubitModeToggle = Checkbutton(master,
            text="Qubit Mode", command=self.toggleQubitMode)
        self.qubitModeToggle.deselect()
        self.qubitModeToggle.grid(row=30, columnspan=3)
        self.qubitMode = False

        self.complexMode = False


        #Built-In Matrices
        built_in_matrices = OptionMenu(master, StringVar(),
            "Up/Down", "Right/Left", "In/Out", "C1", "C2", "C3", "Unitary",
            command=lambda m: self.setMatrix(Matrix({
                "Up/Down": [[1, 0], [0, -1]],
                "Right/Left": [[0, 1], [1, 0]],
                "In/Out": [[0, -1j], [1j, 0]], #can't convert complex to float
                "C1": [[1, 0], [0, -1]],
                "C2": [[-.5, .866], [.866, .5]],
                "C3": [[-.5, -.866], [-.866, .5]],
                "Unitary": [[.5, -.866], [.866, .5]]
            }.get(m)))
        )
        built_in_matrices.grid(row=16, columnspan=2)
        built_in_matrices.config(width = 10)

        # scale slider
        self.scaleSlider = Scale(master, from_=10, to=300, orient=HORIZONTAL,
            width=10, sliderlength=20, showvalue=0, length=170,
            command = self.setScale)
        self.scaleSlider.set(self.unitSize)
        self.scaleSlider.grid(row=31, columnspan=2)

        #Labels
        self.hermitian = Label(master, text="Hermitian")
        self.hermitian.grid(row=4, column=0)
        self.unitary = Label(master, text="Unitary")
        self.unitary.grid(row=4, column = 1)

        self.drawGrid()

        self.ev1 = EigenStuff(self.canvasInfo, master, 8, 10, 'green yellow', 1, 3)
        self.ev2 = EigenStuff(self.canvasInfo, master, 9, 11, 'orange', 2, 1)

        self.v1 = Vector(self.canvasInfo, master, 6, 'blue', 3)
        self.v2 = Vector(self.canvasInfo, master, 7, 'red', 2)

        self.v1.setVals(Matrix([[2],[0]]))
        self.setMatrix( Matrix([[0, 1], [1, 0]]) )

    def setMatrix(self, m):
        self.matrix = m

        if not self.complexMode and self.matrix.isComplex():
            self.complexTransform()
        a, b, c, d = m.vals()
        for box, val in [(self.a, a), (self.b, b), (self.c, c), (self.d, d)]:
            box.delete(0, END)
            box.insert(0, str(val).replace('j', 'i').replace('(', '').replace(')', ''))

        eigenvals, evs = m.eigen(self.complexMode)
        self.eigenvals = eigenvals
        self.ev1.setVals(evs[0].normalize())
        self.ev2.setVals(evs[1].normalize())

        if self.showProj and self.matrix.isHermitian(self.complexMode):
            self.showProj = True
        else:
            self.showProj = False

        self.updateVector(self.v1.vals)
        self.drawMatrix()

    def updateVector(self, v):
        if self.complexMode:
            x, y = v.vals()
            c1, c2 = self.v1.vals.vals()
            d1 = sqrt(abs(x - c1.real)**2 + abs(y - c1.imag)**2)
            d2 = sqrt(abs(x - c2.real)**2 + abs(y - c2.imag)**2)
            if d1 < d2:
                self.setVector(Matrix([[x+y*1j], [c2]]))
            else:
                self.setVector(Matrix([[c1], [x+y*1j]]))
        else:
            self.setVector(v)

    def setVector(self, v):
        if self.qubitMode:
            v = v.normalize()
        self.v1.setVals(v)
        self.v2.setVals(self.matrix * self.v1.vals)
        self.calcProjections()
        self.drawVectors()

    def drawVectors(self):
        self.v1.drawVector(self.unitSize)
        self.v2.setHidden(not self.showProductVector)
        self.v2.drawVector(self.unitSize)

        if not self.complexMode:
          x2, y2 = self.v1.vals.normalize().vals()
          self.ev1.drawProjections(x2, y2, self.amp1, self.unitSize) # some consistency issues with these appearing
          self.ev2.drawProjections(x2, y2, self.amp2, self.unitSize)

        self.v1.setLabel()
        self.v2.setLabel()

        self.ev1.setProbLabel(self.prob1)
        self.ev2.setProbLabel(self.prob2)

        self.ev1.setEvLabelBackground('white')
        self.ev2.setEvLabelBackground('white')


    def drawMatrix(self):
        if self.matrix.isHermitian(self.complexMode):
            self.hermitian.grid()
            self.ev1.probView(True)
            self.ev2.probView(True)
            self.measureButton.grid()
        else:
            self.hermitian.grid_remove()
            self.ev1.probView(False)
            self.ev2.probView(False)
            self.measureButton.grid_remove()
            #also hide the projections
        if self.matrix.isUnitary():
            self.unitary.grid()
            self.stepButton.grid()
            self.stepBackButton.grid()
        else:
            self.unitary.grid_remove()
            self.stepButton.grid_remove()
            self.stepBackButton.grid_remove()

        self.projToggle.grid_remove() if self.complexMode else self.projToggle.grid()

        if self.showProj and not self.complexMode:
            self.projToggle.select()
            self.canvas.itemconfigure("proj", state="normal")
        else:
            self.canvas.itemconfigure("proj", state="hidden")
            self.projToggle.deselect()

        if not self.complexMode:
            self.ev1.drawLine(self.unitSize)
            self.ev2.drawLine(self.unitSize)

        self.ev1.drawEigenBasis(self.unitSize)
        self.ev2.drawEigenBasis(self.unitSize)

        if self.showEigen:
            self.canvas.itemconfigure("eigen", state="normal")
        else:
            self.canvas.itemconfigure("eigen", state="hidden")

        self.ev1.setEvLabel(self.eigenvals[0])
        self.ev2.setEvLabel(self.eigenvals[1])

    def performMeasurement(self):
        random_num = random.random()
        if random_num < self.prob1:
            self.setVector(self.ev1.vals)
            self.ev1.setEvLabelBackground('yellow')
        else:
            self.setVector(self.ev2.vals)
            self.ev2.setEvLabelBackground('yellow')

    def step(self):
        self.updateVector(self.v2.vals)

    def stepBack(self):
        self.updateVector(self.matrix.adjoint(self.complexMode) * self.v1.vals)

    def normalizeVector(self):
        self.setVector(self.v1.vals.normalize())

    def calcProjections(self):
        normalized = self.v1.vals.normalize()
        self.amp1 = normalized.innerProduct(self.ev1.vals, self.complexMode)
        self.amp2 = normalized.innerProduct(self.ev2.vals, self.complexMode)
        self.prob1 = abs(self.amp1)**2
        self.prob2 = abs(self.amp2)**2

    def adjoint(self):
        self.setMatrix(self.matrix.adjoint(self.complexMode))

    def vectorFromCoords(self, x, y):
        return Matrix([
            [(x - self.cWidth/2) / self.unitSize],
            [(self.cHeight/2 - y) / self.unitSize]
        ])
    def onMouseDown(self, event):
        self.updateVector(self.vectorFromCoords(event.x, event.y))
    def onMouseMove(self, event):
        self.updateVector(self.vectorFromCoords(event.x, event.y))

    def canvasResize(self, event):
        w,h = event.width - 6, event.height - 6
        self.cWidth = w
        self.cHeight = h
        self.cDiag = sqrt(w**2 + h**2)
        self.canvas.config(width=w, height=h)
        self.redraw()

    def setScale(self, unitSize):
        self.unitSize = int(unitSize)
        self.redraw()

    def toggleProductVector(self):
        self.showProductVector = not self.showProductVector
        self.drawVectors()

    def toggleProj(self):
        self.showProj = not self.showProj
        self.drawMatrix()

    def toggleEigen(self):
        self.showEigen = not self.showEigen
        self.redraw()

    def toggleQubitMode(self):
        self.qubitMode = not self.qubitMode
        self.normalizeVector()

    def complexTransform(self):
        self.complexMode = not self.complexMode

        if self.complexMode:
            self.complexPlaneToggle.select()
        else:
            self.complexPlaneToggle.deselect()

        self.v1.setComplexMode(self.complexMode)
        self.v2.setComplexMode(self.complexMode)
        self.ev1.setComplexMode(self.complexMode)
        self.ev2.setComplexMode(self.complexMode)

        if not self.complexMode:
            self.setMatrix(self.matrix.decomplexicize())


        self.redraw()

    def drawGrid(self):
        color="#eee"

        xOff = (self.cWidth/2) % self.unitSize
        yOff = (self.cHeight/2) % self.unitSize

        for x in range(0, self.cWidth, self.unitSize):
            self.canvas.create_line(xOff+x, 0, xOff+x, self.cHeight, fill=color, tag="gline")
        for y in range(0, self.cWidth, self.unitSize):
            self.canvas.create_line(0, yOff+y, self.cWidth, yOff+y, fill=color, tag="gline")

        self.canvas.create_line(self.cWidth/2, 0, self.cWidth/2, self.cHeight, tag="gline")
        self.canvas.create_line(0, self.cHeight/2, self.cWidth, self.cHeight/2, tag="gline")

        self.canvas.tag_lower("gline")

    def redraw(self):
        self.canvas.delete("gline")
        self.drawGrid()
        self.drawMatrix()
        self.drawVectors()

root = Tk()
root.grid_columnconfigure(3, weight=2)
root.grid_rowconfigure(29, weight=2)
all = App(root)
root.title('vectorJAM')
root.mainloop()
