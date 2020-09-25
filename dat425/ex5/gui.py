import tkinter as tk
import counters
import datetime

class GUI():
	def __init__(self, master):
		self.master   = master

		self.label = tk.Label(self.master, font=("Courier", 44), width=2, bg="black", fg="white")
		self.label.pack(fill=tk.BOTH, expand=True)

		countButton = tk.Button(master, text="Count", command=self.onCount)
		countButton.pack(side=tk.LEFT)
		resetButton = tk.Button(master, text="Reset", command=self.onReset)
		resetButton.pack(side=tk.LEFT)

		self.counter = counters.BoundedCounter(0, 10)
		#self.counter = counters.SimpleCounter()

	def update(self):
		self.label.configure(text=str(self.counter.getValue()).rjust(2,"0"))
		
	def onCount(self):
		self.counter.count()
		self.update()

	def onReset(self):
		self.counter.reset()
		self.update()

master = tk.Tk()
master.title("Counter")

gui = GUI(master)
gui.update()

master.mainloop()
