from tkinter import *
from la import Matrix
from math import *
import cmath
import random
from PIL import Image, ImageTk
from vector_class import Vector

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

        #Buttons
        update = Button(master, text="Update", command=
            lambda: self.setMatrix(Matrix([
                [eval(self.a.get()), eval(self.b.get())],
                [eval(self.c.get()), eval(self.d.get())]
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
        self.productVectorToggle.select()
        self.productVectorToggle.grid(row=18, column=0, columnspan=3)
        self.showProductVector = True
        self.projToggle = Checkbutton(master,
            text="Show inner products?", command=self.toggleProj)
        self.projToggle.select()
        self.projToggle.grid(row=19, column=0, columnspan=3)
        self.showProj = True

        self.normalizeVectorButton = Button(master, text="Normalize Vector", command=self.normalizeVector)
        self.normalizeVectorButton.grid(row=20, columnspan=2)

        self.measureButton = Button(master, text="Measure", command=self.performMeasurement)
        self.measureButton.grid(row=21, columnspan=2)

        self.complexPlaneToggle = Checkbutton(master,
            text="Complex Plane", command=self.complexTransform)
        self.complexPlaneToggle.deselect()
        self.complexPlaneToggle.grid(row=29, columnspan=3)
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
        self.scaleSlider.grid(row=30, columnspan=2)

        #Labels
        self.hermitian = Label(master, text="Hermitian")
        self.hermitian.grid(row=4, column=0)
        self.unitary = Label(master, text="Unitary")
        self.unitary.grid(row=4, column = 1)
        #v1
        self.blue = Label(master, text="", fg="blue", width=20)
        self.blue.grid(row=6, columnspan=2)
        #v2
        self.red = Label(master, text="", fg="red", width=20)
        self.red.grid(row=7, columnspan=2)
        #v3
        self.lBlue = Label(master, text="", fg="light blue", width=20)
        self.blue.grid(row=24, columnspan=2)#
        #v4
        self.lRed = Label(master, text="", fg="pink", width=20)
        self.red.grid(row=25, columnspan=2)#
        

        self.ev1_label = Label(master, text="", fg="green yellow", width=20)
        self.ev1_label.grid(row=8, columnspan=2)
        self.ev2_label = Label(master, text="", fg="orange", width=20)
        self.ev2_label.grid(row=9, columnspan=2)

        self.prob1_label = Label(master, text="", fg="green yellow", width=20)
        self.prob1_label.grid(row=10, columnspan=2)
        self.prob2_label = Label(master, text="", fg="orange", width=20)
        self.prob2_label.grid(row=11, columnspan=2)

        self.drawGrid()

        self.eb1 = Vector("magenta", self.canvas, self.cWidth, self.cHeight, self.unitSize, 1)
        self.eb2 = Vector("magenta", self.canvas, self.cWidth, self.cHeight, self.unitSize, 1)
 #       self.eb3 = Vector("magenta", self.canvas, self.cWidth, self.cHeight, self.unitSize, 1)
 #       self.eb4 = Vector("magenta", self.canvas, self.cWidth, self.cHeight, self.unitSize, 1)
        self.v1 = Vector("blue", self.canvas, self.cWidth, self.cHeight, self.unitSize, 3)
        self.v2 = Vector("red", self.canvas, self.cWidth, self.cHeight, self.unitSize, 3)
        self.v3 = Vector("light blue", self.canvas, self.cWidth, self.cHeight, self.unitSize, 3)
        self.v4 = Vector("pink", self.canvas, self.cWidth, self.cHeight, self.unitSize, 3)

        self.v1.setVals(Matrix([[4], [1]]))

        self.v3.toggleVector()
        self.v4.toggleVector()

        self.ev1 = self.canvas.create_line(
            0, 0, 0, 0, fill="green yellow", dash=[10, 5])
        self.ev2 = self.canvas.create_line(
            0, 0, 0, 0, fill="orange", dash=[10, 5])
        
        self.projEv1 = self.canvas.create_line(
            0, 0, 0, 0, fill="cyan", arrow="last", width = 1, tag="proj") #hide if complex
        self.projEv2 = self.canvas.create_line(
            0, 0, 0, 0, fill="cyan", arrow="last", width = 1, tag="proj") #hide if complex
        self.projEv1Dash = self.canvas.create_line(
            0, 0, 0, 0, fill="cyan", dash=[10, 5], width = 1, tag="proj") #hide if complex
        self.projEv2Dash = self.canvas.create_line(
            0, 0, 0, 0, fill="cyan", dash=[10, 5], width = 1, tag="proj") #hide if complex

        self.setMatrix( Matrix([[0, 1], [1, 0]]) )

    def setMatrix(self, m):
        self.matrix = m

        a, b, c, d = m.vals()
        for box, val in [(self.a, a), (self.b, b), (self.c, c), (self.d, d)]:
            box.delete(0, END)
            box.insert(0, val)

        eigenvals, evs = m.eigen(self.complexMode)
        self.eigenvals = eigenvals

        self.v1.setEigenVals(evs)

            

        if self.matrix.isHermitian() and not self.complexMode:
            self.showProj = True
        else:
            self.showProj = False

        self.v1.setVector(self.v1.vals, self.matrix, self.v2)
        self.drawVectors()
        self.drawMatrix()

    def setVector(self, v):
        self.v1_vals = v
        self.v2_vals = self.matrix * self.v1_vals
        self.calcProjections()
        self.drawVectors()

    def drawVectors(self):
        if self.complexMode:
            xV1, yV1 = self.v1.vals.vals()[0], self.v1.vals.vals()[1]
            self.v1.drawVector(xV1, yV1)
            xV2, yV2 = self.v2.vals.vals()[0], self.v2.vals.vals()[1]
            self.v2.drawVector(xV2, yV2)
            xV3, yV3 = self.v3.vals.vals()[0], self.v3.vals.vals()[1]
            self.v3.drawVector(xV3, yV3)
            xV4, yV4 = self.v4.vals.vals()[0], self.v4.vals.vals()[1]
            self.v4.drawVector(xV4, yV4)
            
        else:
            #draw vector and its projection
            xV1, yV1 = self.v1.vals.vals()[0], self.v1.vals.vals()[1]
            self.v1.drawVector(xV1, yV1)
            
            self.canvas.itemconfigure(self.v2, state="normal" if self.showProductVector else "hidden")

            xV2, yV2 = self.v2.vals.vals()[0], self.v2.vals.vals()[1]
            self.v2.drawVector(xV2, yV2)

            x2, y2 = self.v1.vals.normalize(self.complexMode).vals() ##
            
            x, y = (self.v1.amp1 * self.v1.ev1_vals).vals()
            self.canvas.coords(self.projEv1,
                self.cWidth/2, self.cHeight/2,
                self.cWidth/2 + x*self.unitSize,
                self.cHeight/2 + -y*self.unitSize
            )
            
            self.canvas.coords(self.projEv1Dash,
                self.cWidth/2 + x*self.unitSize,
                self.cHeight/2 + -y*self.unitSize,
                self.cWidth/2 + x2*self.unitSize,
                self.cHeight/2 + -y2*self.unitSize
            )
            
            x, y = (self.v1.amp2 * self.v1.ev2_vals).vals()
            self.canvas.coords(self.projEv2,
                self.cWidth/2, self.cHeight/2,
                self.cWidth/2 + x*self.unitSize,
                self.cHeight/2 + -y*self.unitSize
            )
            
            self.canvas.coords(self.projEv2Dash,
                self.cWidth/2 + x*self.unitSize,
                self.cHeight/2 + -y*self.unitSize,
                self.cWidth/2 + x2*self.unitSize,
                self.cHeight/2 + -y2*self.unitSize
            )

            self.prob1_label['text'] = "P1 =",round(self.v1.prob1, 4)
            self.prob2_label['text'] = "P2 =",round(self.v1.prob2, 4)

            self.ev1_label['bg'] = "white"
            self.ev2_label['bg'] = "white"

    def drawMatrix(self):
        if self.matrix.isHermitian():
            self.hermitian.grid()
            self.prob1_label.grid()
            self.prob2_label.grid()
            self.measureButton.grid()
        else:
            self.hermitian.grid_remove()
            self.prob1_label.grid_remove()
            self.prob2_label.grid_remove()
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

        if self.showProj:
            self.projToggle.select()
            self.canvas.itemconfigure("proj", state="normal")
        else:
            self.canvas.itemconfigure("proj", state="hidden")
            self.projToggle.deselect()

        x1, y1 = (-self.cDiag * self.v1.ev1_vals).vals()
        x2, y2 = (self.cDiag * self.v1.ev1_vals).vals()

        self.canvas.coords(self.ev1,
            self.cWidth/2 + x1*self.unitSize, self.cHeight/2 - y1*self.unitSize,
            self.cWidth/2 + x2*self.unitSize, self.cHeight/2 - y2*self.unitSize,
        )
        x1, y1 = (-self.cDiag * self.v1.ev2_vals).vals()
        x2, y2 = (self.cDiag * self.v1.ev2_vals).vals()
        self.canvas.coords(self.ev2,
            self.cWidth/2 + x1*self.unitSize, self.cHeight/2 - y1*self.unitSize,
            self.cWidth/2 + x2*self.unitSize, self.cHeight/2 - y2*self.unitSize,
        )
        x, y = self.v1.ev1_vals.vals()
        self.eb1.drawVector(x, y)

        x, y = self.v1.ev2_vals.vals()
        self.eb2.drawVector(x, y)

        self.ev1_label['text'] = "λ1 = " +str(
          round(self.eigenvals[0].real, 4) + self.eigenvals[0].imag*1j)
        self.ev2_label['text'] = "λ2 = " +str(
          round(self.eigenvals[1].real, 4) + self.eigenvals[1].imag*1j)

    def performMeasurement(self):
        random_num = random.random()
        if random_num < self.v1.prob1:
            self.v1.setVector(self.v1.ev1_vals, self.matrix, self.v2)
            self.drawVectors()
            self.ev1_label['bg'] = "yellow"
        else:
            self.v1.setVector(self.v1.ev2_vals, self.matrix, self.v2)
            self.drawVectors()
            self.ev2_label['bg'] = "yellow"

    def step(self):
        self.v1.setVector(self.v2.vself.matrix, self.v2)
        self.drawVectors()

    def stepBack(self):
        self.v1.setVector(self.matrix.adjoint(self.complexMode) * self.v1.vals, self.matrix, self.v2)
        self.drawVectors()

    def normalizeVector(self):
        self.v1.setVector(self.v1.vals.normalize(self.complexMode), self.matrix, self.v2)
        self.drawVectors()

    def calcProjections(self):
        normalized = self.v1_vals.normalize(self.complexMode)
        self.amp1 = normalized.innerProduct(self.ev1_vals)
        self.amp2 = normalized.innerProduct(self.ev2_vals)
        self.prob1 = self.amp1**2
        self.prob2 = self.amp2**2
        #will be different with complex numbers

    def adjoint(self):
        self.setMatrix(self.matrix.adjoint(self.complexMode))

    def vectorFromCoords(self, x, y):
        return Matrix([
            [(x - self.cWidth/2) / self.unitSize],
            [(self.cHeight/2 - y) / self.unitSize]
        ])
    def onMouseDown(self, event):
        self.v1.setVector(self.vectorFromCoords(event.x, event.y), self.matrix, self.v2)
        if self.complexMode:
            otherVals = self.adjustOtherComplexVector(self.v1)
            self.v3.setVector(otherVals, self.matrix, self.v4)
        self.drawVectors()
    def onMouseMove(self, event):
        self.v1.setVector(self.vectorFromCoords(event.x, event.y), self.matrix, self.v2)
        if self.complexMode:
            otherVals = self.adjustOtherComplexVector(self.v1)
            self.v3.setVector(otherVals, self.matrix, self.v4)
        self.drawVectors()

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


    def complexTransform(self):
        self.complexMode = not self.complexMode
        self.v1.toggleComplex()
        self.v2.toggleComplex()
        self.v3.toggleComplex()
        self.v4.toggleComplex()
        self.v3.toggleVector()
        self.v4.toggleVector()
        self.toggleProj()
        if self.complexMode:
            self.v1.setVector(Matrix([[.5],[.5]]), self.matrix, self.v2)
            otherVals = self.adjustOtherComplexVector(self.v1)
            self.v3.setVector(otherVals, self.matrix, self.v4)
            self.drawVectors()

    def adjustOtherComplexVector(self, v1):
        vals = v1.vals.vals() #which will be the real and imaginary parts of a complex number
        squared_vals = vals[0]**2 + vals[1]**2 #it freaks out if this gets above 1
        res = sqrt(1 - self.clip(squared_vals))
        newVals = Matrix([[0],[res]]) #arbitrarily choosing to make it all imaginary for now
        return newVals       

    def clip(self,num):
        if num >= 1:
            return .99
        else:
            return num
    
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
