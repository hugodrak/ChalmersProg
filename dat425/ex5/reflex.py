import tkinter as tk
import counters

class Reflex():
	def __init__(self, master):
		self.master   = master
		self.labels   = self.__init_ui__()
		self.counters = self.__init_counters__()
		self.u_flag   = 20
		self.flag     = self.u_flag
		self.stopped  = False

	def __init_ui__(self):
		minLabel = tk.Label(self.master, font=("Courier", 44), anchor=tk.E, width=2, bg="gray", fg="white")
		minLabel.grid(row=1,column=2)

		secLabel = tk.Label(self.master, font=("Courier", 44), anchor=tk.E, width=3, bg="black", fg="white")
		secLabel.grid(row=1,column=3)

		return (minLabel, secLabel)

	def __init_counters__(self):
		minCounter  = counters.ChainedCounter(0,60,None)
		secCounter  = counters.ChainedCounter(0,1000,minCounter)
		return (minCounter, secCounter)

	def update(self):
		if self.flag >= self.u_flag or self.stopped:
			self.flag = 0
			for i in range(2):
				self.labels[i].configure(text=str(self.counters[i].getValue()).rjust(2,"0"))
		else:
			self.flag = self.flag + 1

		if not self.stopped:
			self.counters[1].count()

			self.master.after(1,self.update)

	def stop(self):
		self.stopped = True

master = tk.Tk()
master.title("Reflex")

reflex = Reflex(master)
reflex.update()

master.bind("<Key>", lambda e: reflex.stop())

master.mainloop()
