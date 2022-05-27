#!/usr/bin/env python3
from tkinter import *
import settings
from PIL import ImageTk, Image
from tkinter import font
import tkinter as tk
from PIL import ImageTk, Image
from serviceDB import serviceDB
from datetime import datetime

from ctypes import windll

from truckDB import truckDB
windll.shcore.SetProcessDpiAwareness(1)
import models

vehicles = []
drivers = []
colors = []

class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame()
        container.pack()

        self.listing = {}

        for p in (homePage, vehiclePage):
            if p == homePage:
                page_name = p.__name__
                frame = p(parent = container, controller = self) # Frame is an instance of each page class.
                frame.grid(row=0, column=0, sticky = 'nsew')
                self.listing[page_name] = frame # We store the page name in a dictionary.

        global allPages
        allPages = settings.allPages

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
        for service in servdb.fetch():
            print("Service: " + " ".join(service[1:]))
            if service[2].lower() == target.reg.lower():
                lst.append(" ".join(service[1:]))
            
        print(lst)
        
        lst = "\n".join(lst)
        serviceItems = Label(self, text=lst)
        serviceItems.pack()

        home = tk.Button(self, text = "Main Menu", command=lambda: controller.up_frame("homePage"))
        home.pack(pady=(20), padx=(10))

class vehiclePage(tk.Frame):
    def __init__(self, parent, controller, targetVehicle = None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        if targetVehicle is not None:
           
            self.reg = targetVehicle.reg
            
            details = truckdb.fetch()
            global targetIndex
            for i in range(len(details)):
                if details[i][0] == targetVehicle.reg:
                    txt = details[i]
                    targetIndex = i

            regLabel = tk.Label(self, text= self.reg, font=('Arial', 22))
            regLabel.pack(pady=20)

            self.myLabel = tk.Label(self, text=txt, font=('Arial', 22))
            self.myLabel.pack()

            #self.myLabel.config(text=txt)
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

            details = truckdb.fetch()

            x = findTargetIndex()

            intro = tk.Label(newWindow,
            text ="You are changing the driver for: \n" + details[x][0] + " | " + details[x][1] + "\nThe current driver is: " + details[x][4])
            intro.pack(in_=top, side=TOP, pady=(5, 0))

            bottom.pack(side=BOTTOM)

            global driver_list
            driver_list = tk.Listbox(newWindow, width=50, font=('Arial', 30))
            submit = tk.Button(newWindow, text = "Change Driver", height=3, width=15, command = lambda: [changeDriver(), newWindow.destroy()])
            submit.pack(in_=bottom, side=TOP, pady=(0, 20))

            for item in drivers:
                driver_list.insert(END, item)

            driver_list.pack(pady=40)
        
        def changeColorWindow():
            newWindow = Toplevel(controller)
            newWindow.title="Change Color"
            newWindow.geometry("500x400")

            top = Frame(newWindow)
            bottom = Frame(newWindow)
            
            details = truckdb.fetch()
            x = findTargetIndex()
            top.pack(side=TOP)
            intro = tk.Label(newWindow,
            text ="You are changing the colour for: \n" + details[x][0] + " | " + details[x][1] + "\nThe current colour is: " + details[x][3])

            intro.pack(in_=top, side=TOP, pady=(5, 0))

            bottom.pack(side=BOTTOM)

            global color_list
            color_list = tk.Listbox(newWindow, width=50, font=('Arial', 30))
            submit = tk.Button(newWindow, text = "Change Color", height=3, width=15, command = lambda: [changeColor(), newWindow.destroy()])
            submit.pack(in_=bottom, side=TOP, pady=(0, 20))

            for item in colors:
                color_list.insert(END, item)

            color_list.pack(pady=40)

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
            submit = tk.Button(newWindow, text = "Submit", height=2, width=10, command = lambda: [servdb.insert(today, self.reg, typeEntry.get(), costEntry.get()), newWindow.destroy()])

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

        changeCol = tk.Button(self, text = "Change Color", command=lambda: changeColorWindow())
        changeCol['font'] = myFont
        changeCol.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))

        bou = tk.Button(self, text = "Main Menu", command=lambda: controller.up_frame("homePage"))
        bou['font'] = myFont
        bou.pack(in_=buttons, side=LEFT, pady=(20), padx=(10))

def initialListboxPopulate():
    my_list.delete(0, END)
    
    trucks = truckdb.fetch()

    for truck in trucks:
        truck = " ".join(truck)
        my_list.insert(END, truck)

def update(data):
    # Clear the listbox
    my_list.delete(0, END)
    
    # Add toppings to listbox
    for item in data:
        my_list.insert(END, item)

def fillout(e):
    my_entry.delete(0, END)

    # Add clicked list item to entry box
    my_entry.insert(0, my_list.get(ACTIVE))

def check(e):
    # grab what was typed
    typed = my_entry.get()

    if typed == '':
        trucks = truckdb.fetch()
        newTrucks = []

        for truck in trucks:
            truck = " ".join(truck)
            newTrucks.append(truck)
    
        data = newTrucks

    else:
        trucks = truckdb.fetch()
        data = []
        for truck in trucks:
            target = " ".join(truck)
            if typed.lower() in target.lower():
                data.append(target)
    
    update(data)

def findTargetIndex():
    details = truckdb.fetch()
    global targetIndex
    print(details)
    for i in range(len(details)):
        if details[i][0] == target.reg:
            targetIndex = i
    
    return targetIndex

def changeDriver():
    for i in driver_list.curselection():
        global driverSelection
        driverSelection = driver_list.get(i)
        print("Selection: " + driverSelection)
    
    print("Current driver: " + target.driver)
    
    truckdb.updateDriver(target.reg, driverSelection)

    initialListboxPopulate()

    details = truckdb.fetch()
    for d in details:
        if d[0] == target.reg:
            txt = d
    
    frame = allPages[target.reg]
    frame.myLabel.config(text=txt)

    showPage(allPages[target.reg])

def changeColor():
    for i in color_list.curselection():
        global colorSelection
        colorSelection = color_list.get(i)
        print("Selection: " + colorSelection)

    print("Current color: " + target.color)

    truckdb.updateColor(target.reg, colorSelection)

    initialListboxPopulate()
    
    
    details = truckdb.fetch()
    for d in details:
        if d[0] == target.reg:
            txt = d
    
    frame = allPages[target.reg]
    frame.myLabel.config(text=txt)

    showPage(allPages[target.reg])

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
    
    with open('drivers.txt') as f:
        x = f.readlines()
        for line in x:
            drivers.append(line.strip())

    with open('colors.txt') as f:
        x = f.readlines()
        for line in x:
            colors.append(line.strip())

def createTruckDB():
    
    with open('data.txt') as f:
        x = f.readlines()
        for line in x:
            inf = line.split(" ")
            reg, make, model, color, driver = inf[0], inf[1], inf[2], inf[3], inf[4]

            truckdb.insert(reg, make, model, color, driver)
    
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
    
    global servdb
    servdb = serviceDB('store.db')

    global truckdb
    truckdb = truckDB('trucks.db')
    
    createObjects()
    x = MainFrame()
    x.state("zoomed")
    x.title('Service Manager')
    x.geometry('1000x500')
    initialListboxPopulate()
    createBinds()
    x.mainloop()
    selection = 'valid'

    while(selection != "quit"):
        selection = prompt()

if __name__ == '__main__':
    main()
