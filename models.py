#!/usr/bin/env python3

# Modelling the truck.

class Truck:
    def __init__(self, reg, make, model, color, driver, lastService, chassisNo, serviceDue, oilSpec, wheelTorque):
        self.reg = reg
        self.make = make
        self.model = model
        self.color = color
        self.driver = driver
        self.lastService = lastService
        self.chassisNo = chassisNo
        self.serviceDueDate = serviceDue
        self.oilSpec = oilSpec
        self.wheelTorque = wheelTorque
        self.serviceHistory = []

class Trailer:
    def __init__(self, id, make, reg, type, lastCheck):
        self.id = id
        self.make = make
        self.reg = reg
        self.type = type
        self.lastCheck = lastCheck
