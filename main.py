#!/usr/bin/env python3
from tkinter import *
import tkinter as tk

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import models
"""
vehicles = []
app = Tk()
my_label = Label(app, text="Vehicle:")
my_label.pack(pady=20)

my_entry = Entry(app)
my_entry.pack()

my_list = Listbox(app, width=50)
my_list.pack(pady=40)

app.title('Service Manager')
app.geometry('700x350')
"""""
class MainFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame()
        container.grid(row=0, column=0, sticky='nesw')

        self.id = tk.StringVar()
        self.id.set("Mister Smith")

        self.listing = {}

        for p in (homePage, vehiclePage):
            page_name = p.__name__
            frame = p(parent = container, controller = self)
            frame.grid(row=0, column=0, sticky = 'nsew')
            self.listing[page_name] = frame
        
        self.up_frame('homePage')
        
    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()

class homePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        label = tk.Label(self, text = "Home page" + controller.id.get())
        label.pack()

        bou = tk.Button(self, text = "to vehicle page", command= lambda: controller.up_frame("vehiclePage"))

        bou.pack()

class vehiclePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        label = tk.Label(self, text = "Vehicle Page" + controller.id.get())
        label.pack()

        bou = tk.Button(self, text = "to home page", command=lambda: controller.up_frame("homePage"))

        bou.pack()
    # Update entry box with listbox clicked

    """
    def fillout(e):
        my_entry.delete(0, END)

        # Add clicked list item to entry box
        my_entry.insert(0, my_list.get(ACTIVE))
    
    # Check entry vs listbox
    def check(e):
        # grab what was typed
        typed = my_entry.get()

        if typed == '':
            data = vehicles
    
        else:
            data = []
            for item in vehicles:
                target = item.reg + " " + item.make + " " + item.model + " " + item.driver
                if typed.lower() in target.lower():
                    data.append(item)
    
        update(data)
    
    
# Bindings
    my_list.bind("<<ListboxSelect>>", fillout)

    my_entry.bind("<KeyRelease>", check)
    """
def update(data):
    # Clear the listbox
    my_list.delete(0, END)
    
    # Add toppings to listbox
    for item in data:
        entry = item.reg + " " + item.make + " " + item.model + " " + item.driver
        my_list.insert(END, entry)
    
def main():

        x = MainFrame()
        x.mainloop()
        createObjects()
        selection = 'valid'

        while(selection != "quit"):
            selection = prompt()

# Create the truck objects
def createObjects():
    
    with open('data.txt') as f:
        x = f.readlines()
        for line in x:
            inf = line.split(" ")
            reg, make, model, color, driver = inf[0], inf[1], inf[2], inf[3], inf[4]
            lastService, chassisNo, serviceDue, oilSpec, wheelTorque = inf[5], inf[6], inf[7], inf[8], inf[9]

            newObject = models.Truck(reg, make, model, color, driver, lastService, chassisNo, serviceDue, oilSpec, wheelTorque)
            vehicles.append(newObject)

            assert(isinstance(newObject, models.Truck))
    
    update(vehicles)

# Prints the prompt
def prompt():
    print("Quit using the X on the program:")
    selection = input()
    return selection

if __name__ == '__main__':
    main()
