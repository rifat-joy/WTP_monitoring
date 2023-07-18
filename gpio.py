import RPi.GPIO as GPIO
from time import sleep

rawWaterValve = 5
ironFilertingValve = 6
sandFilteringValve = 13
hardnessFilteringValve = 16
japaniFiltervalve_1 = 19
japaniFiltervalve_2 = 20
pureWaterValve = 21
sampleTankClearValve = 26
floatStatus = 12

#def gpioInit(): 

def openRawWaterValve():
    GPIO.output(rawWaterValve, GPIO.HIGH)

def closeRawWaterValve():
    GPIO.output(rawWaterValve, GPIO.LOW)

def openIronFilertingValve():
    GPIO.output(ironFilertingValve, GPIO.HIGH)

def closeIronFilertingValve():
    GPIO.output(ironFilertingValve, GPIO.LOW)

def openSandFilteringValve():
    GPIO.output(sandFilteringValve, GPIO.HIGH)

def closeSandFilteringValve():
    GPIO.output(sandFilteringValve, GPIO.LOW)

def openJaPaniAsRemoval_1Valve():
    GPIO.output(japaniFiltervalve_1, GPIO.HIGH)

def closeJaPaniAsRemoval_1Valve():
    GPIO.output(japaniFiltervalve_1, GPIO.LOW)

def openHardnessFilteringValve():
    GPIO.output(hardnessFilteringValve, GPIO.HIGH)

def closeHardnessFilteringValve():
    GPIO.output(hardnessFilteringValve, GPIO.LOW)

def openJaPaniAsRemoval_2Valve():
    GPIO.output(japaniFiltervalve_2, GPIO.HIGH)

def closeJaPaniAsRemoval_2Valve():
    GPIO.output(japaniFiltervalve_2, GPIO.LOW)

def openPureWaterValve():
    GPIO.output(pureWaterValve, GPIO.HIGH)

def closePureWaterValve():
    GPIO.output(pureWaterValve, GPIO.LOW)

def openTankValve():
    GPIO.output(sampleTankClearValve, GPIO.HIGH)

def closeTankValve():
    GPIO.output(sampleTankClearValve, GPIO.LOW)

def clearTank():
    GPIO.output(sampleTankClearValve, GPIO.HIGH)
    sleep(40)
    print("Sample tank empty")
    GPIO.output(sampleTankClearValve, GPIO.LOW)

def readFloatStatus():
    value = GPIO.input(floatStatus)

    return value

def gpioInit():
    GPIO.setup(rawWaterValve, GPIO.OUT)
    GPIO.setup(ironFilertingValve, GPIO.OUT)
    GPIO.setup(sandFilteringValve, GPIO.OUT)
    GPIO.setup(japaniFiltervalve_1, GPIO.OUT)
    GPIO.setup(hardnessFilteringValve, GPIO.OUT)
    GPIO.setup(japaniFiltervalve_2, GPIO.OUT)
    GPIO.setup(pureWaterValve, GPIO.OUT)
    GPIO.setup(sampleTankClearValve, GPIO.OUT)
    #GPIO.setup(floatStatus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(floatStatus, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def gpioLow():
    GPIO.output(rawWaterValve,GPIO.LOW)
    GPIO.output(ironFilertingValve,GPIO.LOW)
    GPIO.output(sandFilteringValve,GPIO.LOW)
    GPIO.output(japaniFiltervalve_1,GPIO.LOW)
    GPIO.output(hardnessFilteringValve,GPIO.LOW)
    GPIO.output(japaniFiltervalve_2,GPIO.LOW)
    GPIO.output(pureWaterValve,GPIO.LOW)
    GPIO.output(sampleTankClearValve,GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.cleanup()



