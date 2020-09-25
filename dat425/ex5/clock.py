import tkinter as tk
import counters
import datetime

class Clock():
	def __init__(self, master):
		self.master   = master
		self.labels   = self.__init_ui__()
		self.counters = self.__init_counters__()

	def __init_ui__(self):
		hourLabel = tk.Label(self.master, font=("Courier", 44), anchor=tk.E, width=2, bg="black", fg="white")
		hourLabel.grid(row=1,column=1)

		minLabel = tk.Label(self.master, font=("Courier", 44), anchor=tk.E, width=2, bg="gray", fg="white")
		minLabel.grid(row=1,column=2)

		secLabel = tk.Label(self.master, font=("Courier", 44), anchor=tk.E, width=2, bg="black", fg="white")
		secLabel.grid(row=1,column=3)

		return (hourLabel, minLabel, secLabel)

	def __init_counters__(self):
		t = datetime.datetime.now()

		hourCounter = counters.ChainedCounter(t.hour,12,None)
		minCounter  = counters.ChainedCounter(t.minute,60,hourCounter)
		secCounter  = counters.ChainedCounter(t.second,60,minCounter)
		return (hourCounter, minCounter, secCounter)

	def update(self):
		for i in range(3):
			self.labels[i].configure(text=str(self.counters[i].getValue()).rjust(2,"0"))

		self.counters[2].count()

		self.master.after(1000,self.update)

master = tk.Tk()
master.title("Clock")

clock = Clock(master)
clock.update()

master.mainloop()
