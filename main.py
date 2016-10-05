from tkinter import *
from la import *

WIDTH = 500
HEIGHT = 400
UNIT_SIZE = 20

class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=WIDTH,height=HEIGHT)
        c = self.canvas

        self.matrix = [[0, 1],
                       [1, 0]]


        self.canvas.bind("<ButtonPress-1>", self.onMouseDown)
        self.canvas.bind("<B1-Motion>", self.onMouseMove)

        self.v1_vals = [4, 1]
        self.v2_vals = [r[0] for r in matrixMul(self.matrix, self.v1_vals)]

        #Matrix entry objects
        self.a = Entry(master, bd = 5, width=3)
        self.a.insert(END, 0)
        self.b = Entry(master, bd = 5, width=3)
        self.b.insert(END, 1)
        self.c = Entry(master, bd = 5, width=3)
        self.c.insert(END, 1)
        self.d = Entry(master, bd = 5, width=3)
        self.d.insert(END, 0)


        #Matrix grid
        self.a.grid(row=1, column=0)
        self.b.grid(row=1, column=1)
        self.c.grid(row=2, column=0)
        self.d.grid(row=2, column=1)
        
        #Canvas
        c.grid(row=0,column=3,rowspan=20)
        
        #Buttons
        update = Button(master, text="Update", command= lambda: self.updateMatrix(self.a.get(), self.b.get(), self.c.get(), self.d.get()))
        update.grid(row=3, column=0)
        submit = Button(master, text="Adjoint", command = self.adjoint)
        submit.grid(row=3, column=1)

        #Labels
        self.hermitian = Label(master, text="Hermitian")
        self.hermitian.grid(row=5, columnspan=2)
        self.blue = Label(master, text=str(self.v1_vals)+"^T", fg="blue", width=20)
        self.blue.grid(row=6, columnspan=2)
        self.red = Label(master, text=str(self.v2_vals)+"^T", fg="red", width=20)
        self.red.grid(row=7, columnspan=2)
        

        self.drawGrid()
        self.v1 = self.makeVector(self.v1_vals, "blue")
        self.v2 = self.makeVector(self.v2_vals, "red")




    def updateMatrix(self, a, b, c, d):
        self.matrix = [[float(a), float(b)],[float(c),float(d)]]
        self.updateV2()
        
        if self.isHermitian():
            self.hermitian.grid()
        else:
            self.hermitian.grid_remove()
        
    def updateCoords(self):
        self.blue['text'] = str([round(x, 2) for x in self.v1_vals])+"^T"
        self.red['text'] = str([round(x, 2) for x in self.v2_vals])+"^T"
                               
    def adjoint(self):
        b_value = self.b.get()
        c_value = self.c.get()
        self.b.delete(0, END)
        self.c.delete(0, END)
        self.b.insert(0,c_value)
        self.c.insert(0,b_value)
        self.updateMatrix(float(self.a.get()), float(c_value), float(b_value), float(self.d.get()))

    def getCurrentMatrix(self):
        return[[self.a.get(), self.b.get()],[self.c.get(), self.d.get()]]
        
    def isHermitian(self):
        return self.getCurrentMatrix() == [[self.a.get(), self.c.get()],[self.b.get(), self.d.get()]]

    def unitary(

    def onMouseDown(self, event):
        self.moveV1(event.x, event.y)
        self.updateV2()

    def onMouseMove(self, event):
        self.moveV1(event.x, event.y)
        self.updateV2()

    def drawGrid(self):
        color="#eee"

        for x in range(UNIT_SIZE, WIDTH, UNIT_SIZE):
                self.canvas.create_line(x, 0, x, HEIGHT, fill=color)
        for y in range(UNIT_SIZE, WIDTH, UNIT_SIZE):
                self.canvas.create_line(0, y, WIDTH, y, fill=color)

        self.canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT)
        self.canvas.create_line(0, HEIGHT/2, WIDTH, HEIGHT/2)

    def makeVector(self, v, color):
        return self.canvas.create_line(
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + v[0]*UNIT_SIZE, HEIGHT/2 + -v[1]*UNIT_SIZE,
            fill=color, arrow="last"
        )

    def moveV1(self, x, y):
        a = (x - WIDTH/2) / UNIT_SIZE
        b = (HEIGHT/2 - y) / UNIT_SIZE
        self.v1_vals = [a, b]
        self.canvas.coords(self.v1, WIDTH/2, HEIGHT/2, x, y)

    def updateV2(self):
        self.v2_vals = [r[0] for r in matrixMul(self.matrix, self.v1_vals)]
        self.canvas.coords(self.v2,
            WIDTH/2, HEIGHT/2,
            WIDTH/2 + self.v2_vals[0]*UNIT_SIZE,
            HEIGHT/2 + -self.v2_vals[1]*UNIT_SIZE
        )
        self.updateCoords()


root = Tk()
all = App(root)
root.title('vectorJAM')
root.mainloop()
