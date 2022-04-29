#!/usr/bin/env python3

from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Test")

my_img = ImageTk.PhotoImage(Image.open("restaurant.png"))
my_label = Label(image=my_img)
my_label.pack()

root.mainloop()