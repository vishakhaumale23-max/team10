print("hi")
# Import Module
from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Welcome to Medication Reminder")
# Set geometry (widthxheight)
root.geometry('350x200')
# adding a label to the root window
lbl = Label(root, text = "Please take tablet")
lbl.grid()
# all widgets will be here
# Execute Tkinter
root.mainloop()