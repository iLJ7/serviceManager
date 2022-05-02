#!/usr/bin/env python3
from hashlib import new
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from db import Database

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import models

vehicles = []

class MainFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame()
        container.pack()

        #self.id = tk.StringVar()
        #self.id.set("Mister Smith")

        self.listing = {}

        for p in (homePage, vehiclePage):
            if p == homePage:
                page_name = p.__name__
                frame = p(parent = container, controller = self) # Frame is an instance of each page class.
                frame.grid(row=0, column=0, sticky = 'nsew')
                self.listing[page_name] = frame # We store the page name in a dictionary.

        # We cant to create a series of pages, one for each individual truck / vehicle. 
        # We want to do this here in the main frame. However, our vehicles haven't been made yet.

        global allPages
        allPages = {}

        for i in range((len(vehicles))):
            frame = vehiclePage(parent = container, controller = self, targetVehicle = vehicles[i]) # Creating an instance of the vehicle page class.
            frame.grid(row=0, column=0, sticky = 'nsew')
            allPages[vehicles[i].reg] = frame

        self.up_frame('homePage')
        
    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()


class homePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.id = controller.id
        
        global homeController
        homeController = controller

        global my_label
        my_label = tk.Label(self, text="Vehicle:")
        my_label.pack(pady=(20,0))

        global my_entry
        my_entry = tk.Entry(self)
        my_entry.pack()

        global my_list
        my_list = tk.Listbox(self, width=50)
        my_list.pack(pady=40)


class vehiclePage(tk.Frame):
    def __init__(self, parent, controller, targetVehicle = None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.id = controller.id

        if targetVehicle is not None:
            reg = targetVehicle.reg
        
            regLabel = tk.Label(self, text= reg)
            regLabel.pack(pady=20)

            values = []

            reg, make, model, color, driver = targetVehicle.reg, targetVehicle.make, targetVehicle.model, targetVehicle.color, targetVehicle.driver
            lastService, chassisNo, serviceDueDate = targetVehicle.lastService, targetVehicle.chassisNo, targetVehicle.serviceDueDate
            oilSpec, wheelTorque = targetVehicle.chassisNo, targetVehicle.wheelTorque

            attributes = vars(targetVehicle)
            values = " | ".join(attributes[key] for key in attributes)

            myLabel = tk.Label(self, text=values)
            myLabel.pack()
        

        def openNewWindow():
            newWindow = Toplevel(controller)
            newWindow.title="Add Service"
            newWindow.geometry("500x300")


            top = Frame(newWindow)
            bottom = Frame(newWindow)
            middle = Frame(newWindow)
            submitArea = Frame(newWindow)

            top.pack(side=TOP)
            submitArea.pack(side=BOTTOM, fill=BOTH, expand=True)
            bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
            middle.pack(side=BOTTOM, fill=BOTH, expand=True)

            intro = tk.Label(newWindow,
            text ="You are adding a service for: \n" + target.make + " | " + target.reg)
            intro.pack(in_=top, side=TOP, pady=(5, 0))

            typeLabel = tk.Label(newWindow, text="Type of service: ")
            typeLabel.pack(in_=middle, side=LEFT)

            typeEntry = tk.Entry(newWindow)
            typeEntry.pack(in_=middle, side=LEFT)

            costLabel = tk.Label(newWindow, text="Cost of service: ")
            costLabel.pack(in_=bottom, side=LEFT)
            
            costEntry = tk.Entry(newWindow)
            costEntry.pack(in_=bottom, side=LEFT, padx=(2.5, 0))

            submit = tk.Button(newWindow, text = "Submit", height=2, width=10, command = lambda: [db.insert(typeEntry.get(), costEntry.get()), newWindow.destroy()])

            submit.pack(in_=submitArea, side=TOP, pady=(10, 0))

        addServ = tk.Button(self, text = "Add Service", command=lambda: openNewWindow())

        addServ.pack(pady=(20))

        bou = tk.Button(self, text = "Main Menu", command=lambda: controller.up_frame("homePage"))

        bou.pack(pady=(20))

def update(data):
            # Clear the listbox
    my_list.delete(0, END)
    
        # Add toppings to listbox
    for item in data:
        entry = item.reg + " " + item.make + " " + item.model + " " + item.driver
        my_list.insert(END, entry)
    
def fillout(e):
    my_entry.delete(0, END)

        # Add clicked list item to entry box
    my_entry.insert(0, my_list.get(ACTIVE))

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

def up_frame2(veh):
    veh.tkraise()

def showPage(veh):
    print("Double click detected.")
    up_frame2(veh)

def showSelected(e):
    for i in my_list.curselection():
        print(i)
        print(my_list.get(i))
        selection = my_list.get(i)
        
        global target
        for j in range(len(vehicles)):
            if vehicles[j].reg == selection.split()[0]:
                target = vehicles[j]

        showPage(allPages[target.reg])

# Create the truck objects
def createObjects():
    
    with open('data.txt') as f:
        x = f.readlines()
        for line in x:
            inf = line.split(" ")
            reg, make, model, color, driver = inf[0], inf[1], inf[2], inf[3], inf[4]
            lastService, chassisNo, serviceDue, oilSpec, wheelTorque, img = inf[5], inf[6], inf[7], inf[8], inf[9], inf[10]

            newObject = models.Truck(reg, make, model, color, driver, lastService, chassisNo, serviceDue, oilSpec, wheelTorque, img)
            vehicles.append(newObject)

            assert(isinstance(newObject, models.Truck))

def createBinds():
    my_list.bind("<<ListboxSelect>>", fillout)
    my_list.bind("<Double-Button-1>", showSelected)
    my_entry.bind("<KeyRelease>", check)

# Prints the prompt
def prompt():
    print("Quit using the X on the program:")
    selection = input()
    return selection

def main():
    
    global db
    db = Database('store.db')

    createObjects()
    x = MainFrame()
    x.title('Service Manager')
    x.geometry('1000x500')

    x.grid_rowconfigure(0, weight=1)
    x.grid_columnconfigure(0, weight=1)

    update(vehicles)
    createBinds()
    x.mainloop()
    selection = 'valid'

    while(selection != "quit"):
        selection = prompt()

if __name__ == '__main__':
    main()
