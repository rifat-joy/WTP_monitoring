import sensors
import MQTT
import gpio
from time import sleep
import json

gpio.gpioInit()

gpio.gpioLow()

def publishKpi():
    i = 0
    while (i < 61):
        sleep(1)
        try:
            sensors.startMeasurements()  #sending measurement command
        except AttributeError:
            print("Error code Published")
            MQTT.clientPing.publish("Error_code", e_code06)
        sleep(1)
        MQTT.clientPing.publish("current_status", "Publishing sensor Kpi")
        try:
            #if sensors.getMeasurementStatusC4E() == 0:      # Reading measurements C4E
            C4Ekpi = sensors.readC4Ekpi(tank)              
            MQTT.clientPing.publish("newvisiontopic/Temperature", C4Ekpi[0])
            MQTT.clientPing.publish("newvisiontopic/Conductivity",C4Ekpi[1])
            MQTT.clientPing.publish("newvisiontopic/Salinity",C4Ekpi[2])
            MQTT.clientPing.publish("newvisiontopic/TDS",C4Ekpi[3])
            #else:
                #MQTT.clientPing.publish("newvisiontopic/C4E_status", "Measurement failed:Current Status -> {}".format(sensors.getMeasurementStatusC4E()))
        except AttributeError:
            print("Error code Published")
            MQTT.clientPing.publish("Error_code", e_code03)

        try:
            #if sensors.getMeasurementStatuspH() == 0:       # Reading measurements pH
            MQTT.clientPing.publish("newvisiontopic/pH",sensors.readpHkpi(tank))
            #else:
                #MQTT.clientPing.publish("newvisiontopic/pH_status","Measurement failed:Current Status -> {}".format(sensors.getMeasurementStatuspH()))
        except AttributeError:
            print("Error code Published")
            MQTT.clientPing.publish("Error_code", e_code04)

        try:
            #if sensors.getMeasurementStatusTurbi != 0:       # Reading measurements Turbidity
            MQTT.clientPing.publish("newvisiontopic/Turbidity",sensors.readTurbiKpi(tank))
            #else:
                #MQTT.clientPing.publish("newvisiontopic/Turbidity_status", "Measurement failed:Current Status -> {}".format(sensors.getMeasurementStatusTurbi()))
        except AttributeError:
            print("Error code Published")
            MQTT.clientPing.publish("Error_code", e_code05)

        sleep(1)
        print(sensors.timeNow(),"Sensor KPI published.")
        i = i+1
        print("Iteration: ",i)
    sensors.client.close()

def pureWater():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openPureWaterValve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closePureWaterValve()
    sleep(10)
    publishKpi() 
    MQTT.clientPing.publish("newvisiontopic/Cycle", cycleStart)
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

def rawWater():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openRawWaterValve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeRawWaterValve()
    MQTT.clientPing.publish("newvisiontopic/Cycle", cycleEnd)
    sleep(10)
    publishKpi()
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

def ironFilerting():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openIronFilertingValve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeIronFilertingValve()
    sleep(10)
    publishKpi() 
    gpio.clearTank()

def sandFiltering():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openSandFilteringValve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeSandFilteringValve()
    sleep(10)
    publishKpi() 
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

def hardnessFiltering():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openHardnessFilteringValve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeHardnessFilteringValve()
    sleep(10)
    publishKpi() 
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

def jaPaniAsRemoval_1():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openJaPaniAsRemoval_1Valve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeJaPaniAsRemoval_1Valve()
    sleep(10)
    publishKpi()
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

def jaPaniAsRemoval_2():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openJaPaniAsRemoval_2Valve()
        sleep(1)
        MQTT.clientPing.publish("current_status", "Filling up {} tank water".format(tank))
    print(gpio.readFloatStatus())
    gpio.closeJaPaniAsRemoval_2Valve()
    sleep(10)
    publishKpi() 
    gpio.clearTank()
    MQTT.clientPing.publish("current_status", "cleared {} tank water".format(tank))

cycleStart = json.dumps({"cycle": "start"})
cycleEnd = json.dumps({"cycle": "end"})

e_code01 = json.dumps({"code" : "101"})
e_code02 = json.dumps({"code" : "102"})
e_code03 = json.dumps({"code" : "103"})
e_code04 = json.dumps({"code" : "104"})
e_code05 = json.dumps({"code" : "105"})
e_code06 = json.dumps({"code" : "106"})

if gpio.readFloatStatus() == 1:
    print("clearing tank")
    gpio.clearTank()

tanklist = ["pureWater","jaPaniAsRemoval_2","jaPaniAsRemoval_1","hardnessFiltering","sandFiltering","ironFiltering","rawWater"]

print(sensors.timeNow(),"Connection status",sensors.connectionStatus())
print (sensors.timeNow(), "Configuring sensor..")

sleep(1)
print (sensors.timeNow(), "Sensor configured..!")

sensors.configC4E()     #configuring C4E for measurements:
sensors.configpH()      #configuring pH for measurements:
sensors.configTurbi()   #configuring turbidity for measurements:

try:
    while sensors.connectionStatus():
        try:
           sensors.startMeasurements()
        except AttributeError:
           print("Error code Published")
           MQTT.clientPing.publish("Error_code", e_code06)

        sleep(1)

        for tank in tanklist:
            if tank == "pureWater":
                pureWater()

            elif tank == "jaPaniAsRemoval_2":
                jaPaniAsRemoval_2()

            elif tank == "jaPaniAsRemoval_1":
                jaPaniAsRemoval_1()

            elif tank == "hardnessFiltering":
                hardnessFiltering()

            elif tank == "sandFiltering":
                sandFiltering()

            if tank == "ironFiltering":
                ironFilerting()
                
            elif tank == "rawWater":
                rawWater()
except KeyboardInterrupt:
  print("GPIO cleared")
  gpio.gpioLow()
