from tkinter import *
from la import Matrix
from math import sqrt

root = Tk()
root.grid_columnconfigure(3, weight=2)
root.grid_rowconfigure(29, weight=2)

class App:
    def __init__(self, master):
        self.cWidth = 800
        self.cHeight = 600
        self.unitSize = 100
        self.cDiag = sqrt(self.cWidth**2 + self.cHeight**2)

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
                [float(self.a.get()), float(self.b.get())],
                [float(self.c.get()), float(self.d.get())]
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

        self.normalizeVectorButton = Button(master, text="Normalize Vector", command=self.normalizeVector)
        self.normalizeVectorButton.grid(row=20, columnspan=2)


        #Built-In Matrices
        var = StringVar(master)
        built_in_matrices = OptionMenu(master, var,"Up/Down", "Right/Left", "In/Out", "C1", "C2", "C3", "Unitary")
        built_in_matrices.grid(row=16, columnspan=2)
        built_in_matrices.config(width = 10)
        def clicked():
            m = var.get()
            built_in_choice = {"Up/Down": [[1, 0], [0, -1]],#divide by 0
                               "Right/Left": [[0, 1], [1, 0]],
                               "In/Out": [[0, -1j], [1j, 0]], #can't convert complex to float
                               "C1": [[1, 0], [0, -1]], #divide by 0
                               "C2": [[-.5, .866], [.866, .5]],
                               "C3": [[-.5, -.866], [-.866, .5]],
                               "Unitary": [[.5, -.866], [.866, .5]]
                               }.get(m)
            self.setMatrix(Matrix(built_in_choice))
        self.useBuiltInMatrix = Button(master, text= "Use Built In Matrix", command=clicked)
        self.useBuiltInMatrix.grid(row=17, columnspan=2)

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
        self.blue = Label(master, text="", fg="blue", width=20)
        self.blue.grid(row=6, columnspan=2)
        self.red = Label(master, text="", fg="red", width=20)
        self.red.grid(row=7, columnspan=2)

        self.ev1_label = Label(master, text="", fg="green yellow", width=20)
        self.ev1_label.grid(row=8, columnspan=2)
        self.ev2_label = Label(master, text="", fg="orange", width=20)
        self.ev2_label.grid(row=9, columnspan=2)

        self.prob1_label = Label(master, text="", fg="green yellow", width=20)
        self.prob1_label.grid(row=10, columnspan=2)
        self.prob2_label = Label(master, text="", fg="orange", width=20)
        self.prob2_label.grid(row=11, columnspan=2)

        self.drawGrid()

        self.ev1 = self.canvas.create_line(
            0, 0, 0, 0, fill="green yellow", dash=[10, 5])
        self.ev2 = self.canvas.create_line(
            0, 0, 0, 0, fill="orange", dash=[10, 5])
        self.eb1 = self.canvas.create_line(
            0, 0, 0, 0, fill="magenta", arrow="last")
        self.eb2 = self.canvas.create_line(
            0, 0, 0, 0, fill="magenta", arrow="last")

        self.v1 = self.canvas.create_line(
            0, 0, 0, 0, fill="blue", arrow="last", width = 3)
        self.v2 = self.canvas.create_line(
            0, 0, 0, 0, fill="red", arrow="last", width = 3)

        self.v1_vals = Matrix([[4], [1]])
        self.setMatrix( Matrix([[0, 1], [1, 0]]) )

    def setMatrix(self, m):
        self.matrix = m

        a, b, c, d = m.vals()
        self.a.delete(0, END)
        self.b.delete(0, END)
        self.c.delete(0, END)
        self.d.delete(0, END)
        self.a.insert(0, a)
        self.b.insert(0, b)
        self.c.insert(0, c)
        self.d.insert(0, d)

        eigenvals, evs = m.eigen()
        self.eigenvals = eigenvals
        self.ev1_vals = evs[0].normalize()
        self.ev2_vals = evs[1].normalize()

        self.setVector(self.v1_vals)
        self.drawMatrix()

    def setVector(self, v):
        self.v1_vals = v
        self.v2_vals = self.matrix * self.v1_vals
        self.drawVectors()

    def drawVectors(self):
        self.canvas.coords(self.v1,
            self.cWidth/2, self.cHeight/2,
            self.cWidth/2 + self.v1_vals.vals()[0]*self.unitSize,
            self.cHeight/2 + -self.v1_vals.vals()[1]*self.unitSize
        )
        self.canvas.itemconfigure(self.v2, state="normal" if self.showProductVector else "hidden")
        self.canvas.coords(self.v2,
            self.cWidth/2, self.cHeight/2,
            self.cWidth/2 + self.v2_vals.vals()[0]*self.unitSize,
            self.cHeight/2 + -self.v2_vals.vals()[1]*self.unitSize
        )
        self.projections()
        self.blue['text'] = str([round(x, 2) for x in self.v1_vals.vals()])+"^T"
        self.red['text'] = str([round(x, 2) for x in self.v2_vals.vals()])+"^T"

    def drawMatrix(self):
        if self.matrix.isHermitian():
            self.hermitian.grid()
            self.projections()
            self.prob1_label.grid()
            self.prob2_label.grid()
        else:
            self.hermitian.grid_remove()
            self.prob1_label.grid_remove()
            self.prob2_label.grid_remove()
            #also hide the projections
        if self.matrix.isUnitary():
            self.unitary.grid()
            self.stepButton.grid()
            self.stepBackButton.grid()
        else:
            self.unitary.grid_remove()
            self.stepButton.grid_remove()
            self.stepBackButton.grid_remove()


        x1, y1 = (-self.cDiag * self.ev1_vals).vals()
        x2, y2 = (self.cDiag * self.ev1_vals).vals()

        self.canvas.coords(self.ev1,
            self.cWidth/2 + x1*self.unitSize, self.cHeight/2 - y1*self.unitSize,
            self.cWidth/2 + x2*self.unitSize, self.cHeight/2 - y2*self.unitSize,
        )
        x1, y1 = (-self.cDiag * self.ev2_vals).vals()
        x2, y2 = (self.cDiag * self.ev2_vals).vals()
        self.canvas.coords(self.ev2,
            self.cWidth/2 + x1*self.unitSize, self.cHeight/2 - y1*self.unitSize,
            self.cWidth/2 + x2*self.unitSize, self.cHeight/2 - y2*self.unitSize,
        )
        x, y = self.ev1_vals.vals()
        self.canvas.coords(self.eb1,
            self.cWidth/2, self.cHeight/2,
            self.cWidth/2 + x*self.unitSize, self.cHeight/2 - y*self.unitSize,
        )
        x, y = self.ev2_vals.vals()
        self.canvas.coords(self.eb2,
            self.cWidth/2, self.cHeight/2,
            self.cWidth/2 + x*self.unitSize, self.cHeight/2 - y*self.unitSize,
        )

        self.ev1_label['text'] = str(
          round(self.eigenvals[0].real, 4) + self.eigenvals[0].imag*1j)
        self.ev2_label['text'] = str(
          round(self.eigenvals[1].real, 4) + self.eigenvals[1].imag*1j)

    def step(self):
        self.setVector(self.v2_vals)

    def stepBack(self):
        self.setVector(self.matrix.adjoint() * self.v1_vals)

    def normalizeVector(self):
        self.setVector(self.v1_vals.normalize())

    def projections(self):
        normalized = self.v1_vals.normalize()
        amp1 = normalized.innerProduct(self.ev1_vals)
        amp2 = normalized.innerProduct(self.ev2_vals)
        prob1 = amp1.rows()[0][0]**2
        prob2 = amp2.rows()[0][0]**2

        #will be different with complex numbers
        self.prob1_label['text'] = "P1=",round(prob1, 4)
        self.prob2_label['text'] = "P2=",round(prob2, 4)

        return (prob1, prob2)

    def adjoint(self):
        self.setMatrix(self.matrix.adjoint())

    def vectorFromCoords(self, x, y):
        return Matrix([
            [(x - self.cWidth/2) / self.unitSize],
            [(self.cHeight/2 - y) / self.unitSize]
        ])
    def onMouseDown(self, event):
        self.setVector(self.vectorFromCoords(event.x, event.y))
    def onMouseMove(self, event):
        self.setVector(self.vectorFromCoords(event.x, event.y))

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

all = App(root)
root.title('vectorJAM')
root.mainloop()
