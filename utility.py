# Create the truck objects
drivers = []

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

