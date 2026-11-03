from tkinter import *
from tkinter import ttk

root = Tk()
root.title = ("Dashboard")
root.geometry("300x200")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.place(x = 0, y = 0, width = 300, height = 200)

ttk.Label(mainframe, text="Dashboard").place(x = 80, y = 10)
ttk.Label(mainframe, text="Welcome Back").place(x = 80, y = 40)

ttk.Button(mainframe, text="Exit", command=root.destroy).place(x = 10, y = 80)

root.mainloop()