#!/usr/bin/env python3
import string
from tkinter import *
from PIL import ImageTk, Image
from tkinter import font
import tkinter as tk
from PIL import ImageTk, Image
from db import Database
from datetime import datetime

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

        global allPages
        allPages = {}

        for i in range((len(vehicles))):
            frame = vehiclePage(parent = container, controller = self, targetVehicle = vehicles[i]) # Creating an instance of the vehicle page class.
            frame.grid(row=0, column=0, sticky = 'nsew')
            allPages[vehicles[i].reg] = frame

        allPages['serviceHistory'] = vehiclePage(parent = container, controller = self)
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
        my_label = tk.Label(self, text="Vehicle:", font=('Arial', 30))
        my_label.pack(pady=(20,0))

        global my_entry
        my_entry = tk.Entry(self, font=('Verdana', 30))
        my_entry.pack()

        global my_list
        my_list = tk.Listbox(self, width=50, font=('Arial', 30))
        my_list.pack(pady=40)

class servicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        serviceLabel = tk.Label(self, text= target.reg)
        serviceLabel.pack(pady=20)

        lst = []
        for service in db.fetch():
            if service[1] == target.reg:
                lst.append(" ".join(service[1:]))
        
        lst = "\n".join(lst)
        serviceItems = Label(self, text=lst)
        serviceItems.pack()

        home = tk.Button(self, text = "Main Menu", command=lambda: controller.up_frame("homePage"))
        home.pack(pady=(20), padx=(10))

class vehiclePage(tk.Frame):
    def __init__(self, parent, controller, targetVehicle = None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.id = controller.id

        if targetVehicle is not None:
           
            self.reg = targetVehicle.reg
            
            regLabel = tk.Label(self, text= self.reg, font=('Arial', 22))
            regLabel.pack(pady=20)

            values = []

            attributes = vars(targetVehicle)
            values = " | ".join(attributes[key] for key in attributes)

            myLabel = tk.Label(self, text=values, font=('Arial', 22))
            myLabel.pack()

            frame = Frame(self)
            frame.pack(side=TOP, expand=True)
            self.img = Image.open(targetVehicle.image)
            resized_image = self.img.resize((300, 300))
            self.img = ImageTk.PhotoImage(resized_image)

            # Create a Label Widget to display the text or Image
            self.label = Label(frame, image = self.img)
            self.label.pack()
        
        def createServicePage():
            frame = servicePage(parent, controller)
            frame.grid(row=0, column=0, sticky = 'nsew')
            allPages['servicesPage'] = frame
            showPage(frame)
        
        def changeDriverWindow():
            newWindow = Toplevel(controller)
            newWindow.title="Change Driver"
            newWindow.geometry("500x400")

            top = Frame(newWindow)
            bottom = Frame(newWindow)

            top.pack(side=TOP)
            intro = tk.Label(newWindow,
            text ="You are changing the driver for: \n" + target.make + " | " + target.reg + "\nThe current driver is: " + target.driver)
            intro.pack(in_=top, side=TOP, pady=(5, 0))

            bottom.pack(side=BOTTOM)

            global driver_list
            driver_list = tk.Listbox(newWindow, width=50, font=('Arial', 30))
            submit = tk.Button(newWindow, text = "Change Driver", height=3, width=15, command = lambda: [changeDriver(), newWindow.destroy()])
            submit.pack(in_=bottom, side=TOP, pady=(0, 20))

            drivers = []
            for veh in vehicles:
                drivers.append(veh.driver)

            for item in drivers:
                driver_list.insert(END, item)

            driver_list.pack(pady=40)

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

            today = datetime.now()
            today = today.strftime("%d/%m/%Y %H:%M:%S")
            print(today)
            submit = tk.Button(newWindow, text = "Submit", height=2, width=10, command = lambda: [db.insert(today, self.reg, typeEntry.get(), costEntry.get()), newWindow.destroy()])

            submit.pack(in_=submitArea, side=TOP, pady=(10, 0))
        
        buttons = Frame(self)
        buttons.pack(side=BOTTOM, expand=True)

        myFont = font.Font(family='Arial', size=22)

        addServ = tk.Button(self, text = "Add Service", command=lambda: openNewWindow())
        addServ['font'] = myFont
        addServ.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))

        viewServ = tk.Button(self, text="View Services", command=lambda: createServicePage())
        viewServ['font'] = myFont
        viewServ.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))

        changeDriv = tk.Button(self, text = "Change Driver", command=lambda: changeDriverWindow())
        changeDriv['font'] = myFont
        changeDriv.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))

        bou = tk.Button(self, text = "Main Menu", command=lambda: controller.up_frame("homePage"))
        bou['font'] = myFont
        bou.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))
        
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

def changeDriver():
    for i in driver_list.curselection():
        global selection
        selection = driver_list.get(i)
        print("Selection: " + selection)

        location = 0
        global newDriversTruck
        for j in range(len(vehicles)):
            if vehicles[j].driver == selection:
                newDriversTruck = vehicles[j]
                location = j

    # To change the driver, the text file needs to be changed.
    # The target vehicle's driver field needs to be changed.
    my_file = open("data.txt")
    string_list = my_file.readlines()
    my_file.close()

    global index

    for i in range(len(string_list)):
        if string_list[i].split()[4] == target.driver:
            index = i

    listToChange = string_list[index].split()
    listToChange[4] = selection

    string_list[index] = " ".join(listToChange)
    string_list[index] = string_list[index] + "\n"
    print("Current driver: " + target.driver + " New driver: " + newDriversTruck.driver)
    
    my_file = open("data.txt", "w")
    my_file.write("".join(string_list))
    my_file.close()

def showPage(veh):
    print("Double click detected.")
    veh.tkraise()

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
    x.state("zoomed")
    x.title('Service Manager')
    x.geometry('1000x500')
    update(vehicles)
    createBinds()
    x.mainloop()
    selection = 'valid'

    while(selection != "quit"):
        selection = prompt()

if __name__ == '__main__':
    main()
