import tkinter as tk
from la import matrixMul

WIDTH = 800
HEIGHT = 600
UNIT_SIZE = 20

class App(tk.Tk):
		def __init__(self, *args, **kwargs):
				tk.Tk.__init__(self, *args, **kwargs)

				self.canvas = tk.Canvas(width=800, height=600)
				self.canvas.pack(fill="both", expand=True)

				self.drawGrid()

				self.canvas.bind("<ButtonPress-1>", self.onMouseDown)
				self.canvas.bind("<B1-Motion>", self.onMouseMove)

				self.matrix = [
					[0, 1],
					[1, 0]
				]
				self.v1_vals = [1, 0]
				self.v2_vals = [r[0] for r in matrixMul(self.matrix, self.v1_vals)]
				self.v1 = self.makeVector(self.v1_vals, "blue")
				self.v2 = self.makeVector(self.v2_vals, "red")

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

if __name__ == "__main__":
		app = App()
		app.mainloop()
