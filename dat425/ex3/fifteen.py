import tkinter as tk
from fifteen_model import *

def pack_labels(master,model,on_click):
  labels = []
  for row in range(4):
    row_labels = []
    for col in range(4):
      label = tk.Label(master, font=("Courier", 44), anchor=tk.E, width=2)
      label.grid(row=row,column=col,sticky=(tk.N, tk.S, tk.E, tk.W), padx=2, pady=2)
      label.bind("<Button-1>",(lambda row,col: lambda e: on_click(row,col))(row,col))
      row_labels.append(label)
    labels.append(row_labels)
  return labels

def update_labels(labels,model):
  for row in range(4):
    for col in range(4):
      val = model.getValue(row,col)
      if val == 0:
        labels[row][col].configure(text="",       fg="white", bg="black")
      elif val % 2 == 0:
        labels[row][col].configure(text=str(val), fg="white", bg="red")
      else:
        labels[row][col].configure(text=str(val), fg="red",   bg="white")

def init_ui(model):
  master = tk.Tk()
  master.title("Fifteen")
  master.configure(bg="black")

  def on_click(row,col):
    model.tryMove(row,col)
    update_labels(labels,model)

  labels = pack_labels(master,model,on_click)
  update_labels(labels,model)

  return master

model = FifteenModel()
model.shuffle()

master = init_ui(model)
master.mainloop()
