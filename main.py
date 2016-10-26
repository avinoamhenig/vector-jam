from tkinter import *
from la import *
from math import sqrt

WIDTH = 800
HEIGHT = 600
UNIT_SIZE = 100
DIAG = sqrt(WIDTH**2 + HEIGHT**2)

class App:
    def __init__(self, master):
        #Matrix entry objects
        self.a = Entry(master, bd = 5, width=5)
        self.a.insert(END, 0)
        self.b = Entry(master, bd = 5, width=5)
        self.b.insert(END, 1)
        self.c = Entry(master, bd = 5, width=5)
        self.c.insert(END, 1)
        self.d = Entry(master, bd = 5, width=5)
        self.d.insert(END, 0)

        #Matrix grid layout
        self.a.grid(row=1, column=0)
        self.b.grid(row=1, column=1)
        self.c.grid(row=2, column=0)
        self.d.grid(row=2, column=1)

        #Canvas
        self.canvas = Canvas(master, width=WIDTH,height=HEIGHT)
        c = self.canvas
        c.grid(row=0,column=3,rowspan=20)
        self.canvas.bind("<ButtonPress-1>", self.onMouseDown)
        self.canvas.bind("<B1-Motion>", self.onMouseMove)

        #Buttons
        update = Button(master, text="Update", command= lambda: self.setMatrix(self.a.get(), self.b.get(), self.c.get(), self.d.get()))
        update.grid(row=3, column=0)
        submit = Button(master, text="Adjoint", command = self.adjoint)
        submit.grid(row=3, column=1)
        self.stepButton = Button(master, text="Step", command = self.step)
        self.stepButton.grid(row=5, columnspan=2)

        #Built-In Matrices
        var = StringVar(master)
        built_in_matrices = OptionMenu(master, var,"Up/Down", "Right/Left", "In/Out", "C1", "C2", "C3")
        built_in_matrices.grid(row=16, columnspan=2)
        built_in_matrices.config(width = 10)
        def clicked():
            m = var.get()
            built_in_choice = {"Up/Down": (1, 0, 0, -1),#divide by 0
                               "Right/Left": (0, 1, 1, 0),
                               "In/Out": (0, -1j, 1j, 0), #can't convert complex to float
                               "C1": (1, 0, 0, -1), #divide by 0
                               "C2": (-.5, .866, .866, .5),
                               "C3": (-.5, -.866, -.866, .5)
                               }.get(m)
            self.updateEntryMatrix(*built_in_choice)
        self.useBuiltInMatrix = Button(master, text= "Use Built In Matrix", command=clicked)
        self.useBuiltInMatrix.grid(row=17, columnspan=2)

        #Labels
        self.hermitian = Label(master, text="Hermitian")
        self.hermitian.grid(row=4, column=0)
        self.unitary = Label(master, text="Unitary")
        self.unitary.grid(row=4, column = 1)
        self.blue = Label(master, text="", fg="blue", width=20)
        self.blue.grid(row=6, columnspan=2)
        self.red = Label(master, text="", fg="red", width=20)
        self.red.grid(row=7, columnspan=2)

        self.ev1_label = Label(master, text="",
          fg="green yellow", width=20)
        self.ev1_label.grid(row=8, columnspan=2)
        self.ev2_label = Label(master, text="",
          fg="orange", width=20)
        self.ev2_label.grid(row=9, columnspan=2)

        self.drawGrid()

        self.ev1 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="green yellow", dash=[10, 5]
        )
        self.ev2 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="orange", dash=[10, 5]
        )
        self.eb1 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="magenta", arrow="last"
        )
        self.eb2 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="magenta", arrow="last"
        )

        self.v1 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="blue", arrow="last", width = 3
        )
        self.v2 = self.canvas.create_line(
            0, 0, 0, 0,
            fill="red", arrow="last", width = 3
        )

        self.v1_vals = [4, 1]
        self.setMatrix(0, 1,
                       1, 0)

    def updateEntryMatrix(self, v1, v2, v3, v4):
        self.a.delete(0, END)
        self.b.delete(0, END)
        self.c.delete(0, END)
        self.d.delete(0, END)
        self.a.insert(0, v1)
        self.b.insert(0, v2)
        self.c.insert(0, v3)
        self.d.insert(0, v4)
        self.setMatrix(v1, v2, v3, v4)

    def step(self):
        print('you will step here!')
        self.setVector(*self.v2_vals)

    def setMatrix(self, a, b, c, d):
        self.matrix = [[float(a), float(b)],[float(c),float(d)]]

        eigenvals, evs = eigen(float(a), float(b), float(c), float(d))
        self.eigenvals = eigenvals
        if (len(evs) == 0):
          self.ev1_vals = [0,0]
          self.ev2_vals = [0,0]
        else:
          self.ev1_vals = normalize(evs[0])
          self.ev2_vals = normalize(evs[1])

        self.setVector(self.v1_vals[0], self.v1_vals[1])
        self.drawMatrix()

    def setVector(self, x, y):
        self.v1_vals = [float(x), float(y)]
        self.v2_vals = [r[0] for r in matrixMul(self.matrix, self.v1_vals)]
        self.drawVectors()

    def drawVectors(self):
        self.canvas.coords(self.v1,
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + self.v1_vals[0]*UNIT_SIZE,
            HEIGHT/2 + -self.v1_vals[1]*UNIT_SIZE
        )
        self.canvas.coords(self.v2,
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + self.v2_vals[0]*UNIT_SIZE,
            HEIGHT/2 + -self.v2_vals[1]*UNIT_SIZE
        )
        self.blue['text'] = str([round(x, 2) for x in self.v1_vals])+"^T"
        self.red['text'] = str([round(x, 2) for x in self.v2_vals])+"^T"

    def drawMatrix(self):
        self.hermitian.grid() if self.isHermitian() else self.hermitian.grid_remove()
        self.unitary.grid() if self.isUnitary() else self.unitary.grid_remove()
        self.stepButton.grid() if self.isUnitary() else self.stepButton.grid_remove()

        x1, y1 = scalarMul(-DIAG, self.ev1_vals)
        x2, y2 = scalarMul(DIAG, self.ev1_vals)
        self.canvas.coords(self.ev1,
            WIDTH/2 + x1*UNIT_SIZE, HEIGHT/2 - y1*UNIT_SIZE,
            WIDTH/2 + x2*UNIT_SIZE, HEIGHT/2 - y2*UNIT_SIZE,
        )
        x1, y1 = scalarMul(-DIAG, self.ev2_vals)
        x2, y2 = scalarMul(DIAG, self.ev2_vals)
        self.canvas.coords(self.ev2,
            WIDTH/2 + x1*UNIT_SIZE, HEIGHT/2 - y1*UNIT_SIZE,
            WIDTH/2 + x2*UNIT_SIZE, HEIGHT/2 - y2*UNIT_SIZE,
        )
        x, y = self.ev1_vals
        self.canvas.coords(self.eb1,
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + x*UNIT_SIZE, HEIGHT/2 - y*UNIT_SIZE,
        )
        x, y = self.ev2_vals
        self.canvas.coords(self.eb2,
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + x*UNIT_SIZE, HEIGHT/2 - y*UNIT_SIZE,
        )

        self.ev1_label['text'] = str(
          round(self.eigenvals[0].real, 4) + self.eigenvals[0].imag*1j)
        self.ev2_label['text'] = str(
          round(self.eigenvals[1].real, 4) + self.eigenvals[1].imag*1j)

    def adjoint(self):
        b_value = self.b.get()
        c_value = self.c.get()
        self.b.delete(0, END)
        self.c.delete(0, END)
        self.b.insert(0,c_value)
        self.c.insert(0,b_value)
        self.setMatrix(float(self.a.get()), float(c_value), float(b_value), float(self.d.get()))

    def getAdjoint(self):
        return [[float(self.a.get()), float(self.c.get())], [float(self.b.get()), float(self.d.get())]]

    def isHermitian(self):
        return self.matrix == self.getAdjoint()

    def isUnitary(self):
        identity_matrix = [[1,0],[0,1]]
        product = matrixMul(self.matrix, self.getAdjoint())
        product = [[1 if 1-x < .0001 else x for x in r] for r in product] # round to 1 if v close
        return product == identity_matrix

    def onMouseDown(self, event):
        self.setVector((event.x - WIDTH/2) / UNIT_SIZE, (HEIGHT/2 - event.y) / UNIT_SIZE)
    def onMouseMove(self, event):
        self.setVector((event.x - WIDTH/2) / UNIT_SIZE, (HEIGHT/2 - event.y) / UNIT_SIZE)

    def drawGrid(self):
        color="#eee"

        for x in range(UNIT_SIZE, WIDTH, UNIT_SIZE):
                self.canvas.create_line(x, 0, x, HEIGHT, fill=color)
        for y in range(UNIT_SIZE, WIDTH, UNIT_SIZE):
                self.canvas.create_line(0, y, WIDTH, y, fill=color)

        self.canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT)
        self.canvas.create_line(0, HEIGHT/2, WIDTH, HEIGHT/2)


root = Tk()
all = App(root)
root.title('vectorJAM')
root.mainloop()
