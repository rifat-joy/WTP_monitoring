import gpio
from time import sleep

def pureWater():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openPureWaterValve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closePureWaterValve()
    #gpio.clearTank()

def rawWater():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openRawWaterValve()
        sleep(1)  
    print(gpio.readFloatStatus())
    gpio.closeRawWaterValve()
    #gpio.clearTank()

def ironFilerting():
    print(gpio.readFloatStatus() == 0)
    while gpio.readFloatStatus():
        gpio.openIronFilertingValve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closeIronFilertingValve()
    #gpio.clearTank()

def sandFiltering():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openSandFilteringValve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closeSandFilteringValve()
    #gpio.clearTank()

def hardnessFiltering():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openHardnessFilteringValve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closeHardnessFilteringValve()
    #gpio.clearTank()

def jaPaniAsRemoval_1():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openJaPaniAsRemoval_1Valve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closeJaPaniAsRemoval_1Valve()
    #gpio.clearTank()

def jaPaniAsRemoval_2():
    print(gpio.readFloatStatus())
    while gpio.readFloatStatus() == 0:
        gpio.openJaPaniAsRemoval_2Valve()
        sleep(1)
    print(gpio.readFloatStatus())
    gpio.closeJaPaniAsRemoval_2Valve()
    #gpio.clearTank()

gpio.gpioInit()

#tanklist = ["pureWater","jaPaniAsRemoval_2","jaPaniAsRemoval_1","hardnessFiltering","sandFiltering","ironFilerting","rawWater"]

try:
  while True:
    #gpio.clearTank()
    #gpio.openPureWaterValve()
    #gpio.openJaPaniAsRemoval_1Valve()
    #gpio.openHardnessFilteringValve()
    #gpio.openSandFilteringValve()
    #gpio.openIronFilertingValve()
    #gpio.openRawWaterValve()
    gpio.clearTank()
    #gpio.openPureWaterValve()
    
except KeyboardInterrupt:
  print("GPIO cleared")
  gpio.gpioLow()
