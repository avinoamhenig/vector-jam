import tkinter as tk

class App(tk.Tk):
		def __init__(self, *args, **kwargs):
				tk.Tk.__init__(self, *args, **kwargs)

				self.canvas = tk.Canvas(width=800, height=600)
				self.canvas.pack(fill="both", expand=True)

				self.circle = self.canvas.create_oval(375, 275, 425, 325, fill="black")

				self.canvas.bind("<ButtonPress-1>", self.onMouseDown)
				self.canvas.bind("<ButtonRelease-1>", self.onMouseUp)
				self.canvas.bind("<B1-Motion>", self.onMouseMove)

		def onMouseDown(self, event):
				self.canvas.coords(self.circle,
					event.x - 25, event.y - 25,
					event.x + 25, event.y + 25)

		def onMouseUp(self, event):
				pass

		def onMouseMove(self, event):
				self.canvas.coords(self.circle,
					event.x - 25, event.y - 25,
					event.x + 25, event.y + 25)

if __name__ == "__main__":
		app = App()
		app.mainloop()
