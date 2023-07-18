import time
import serial
from datetime import datetime
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder 
from pymodbus.constants import Endian
import gpio

#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

conductivitySensor= 30
phSensor = 20
turbiditySensor = 40


def timeNow():
    currentDateAndTime= datetime.now()
    currentTime= currentDateAndTime.strftime("%H:%M:%S")
    return currentTime + "->"

def getSamplingDelayC4E():
    samplingDelayC4E = client.read_holding_registers(address= 0x00A4,count= 1,unit= conductivitySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(samplingDelayC4E.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    measurementDelayC4E = decoder.decode_16bit_uint()
    return measurementDelayC4E
    
def getSamplingDelaypH():
    samplingDelaypH = client.read_holding_registers(address= 0x00A4,count= 1,unit= phSensor)
    decoder= BinaryPayloadDecoder.fromRegisters(samplingDelaypH.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    measurementDelaypH = decoder.decode_16bit_uint()
    return measurementDelaypH

def getSamplingDelayTurbi():
    samplingDelayTurbi = client.read_holding_registers(address= 0x00A4,count= 1,unit= turbiditySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(samplingDelayTurbi.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    measurementDelayTurbi = decoder.decode_16bit_uint()
    return measurementDelayTurbi

def configC4E():
    client.write_register(address=0x00A5, value=0x0000, unit= conductivitySensor)
    client.write_register(address=0x00A6, value=0x0000, unit= conductivitySensor)
    client.write_register(address=0x00A7, value=0x0000, unit= conductivitySensor)
    client.write_register(address=0x00A8, value=0x0000, unit= conductivitySensor)
    return None

def configpH():
    client.write_register(address=0x00A6, value=0x0000, unit= phSensor)
    return None

def configTurbi():
    client.write_register(address=0x00A6, value=0x0000, unit= turbiditySensor)
    return None

def startMeasurements():
    client.write_register(address=0x0001, value= 0x001F, unit=  conductivitySensor)
    client.write_register(address=0x0001, value= 0x001F, unit=  phSensor)
    client.write_register(address=0x0001, value= 0x001F, unit=  turbiditySensor)

def getMeasurementStatusC4E():     # Checking measurement status for C4E:
    measureStatusC4E = client.read_holding_registers(address= 0x0052, count= 1, unit= conductivitySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(measureStatusC4E.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    StatusC4E= decoder.decode_8bit_int()
    return StatusC4E

def getMeasurementStatuspH():
    measureStatuspH = client.read_holding_registers(address= 0x0052, count= 1, unit= conductivitySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(measureStatuspH.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    StatuspH= decoder.decode_8bit_int()
    return StatuspH

def getMeasurementStatusTurbi():
    measureStatusTurbi = client.read_holding_registers(address= 0x0052, count= 1, unit= turbiditySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(measureStatusTurbi.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    StatusTurbi= decoder.decode_8bit_int()
    return StatusTurbi

def readC4Ekpi():
    valuesC4E = client.read_holding_registers(address= 0x0053, count= 8, unit= conductivitySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(valuesC4E.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    Temperature = decoder.decode_32bit_float()
    Conductivity = decoder.decode_32bit_float()
    Salinity = decoder.decode_32bit_float()
    TDS = decoder.decode_32bit_float()
    return Temperature, Conductivity, Salinity, TDS

def readpHkpi():
    pH_ = client.read_holding_registers(address= 0x0055, count= 2, unit= phSensor)
    decoder= BinaryPayloadDecoder.fromRegisters(pH_.registers,byteorder= Endian.Big, wordorder=Endian.Big)
    pH = decoder.decode_32bit_float()
    return pH

def readTurbiKpi():
    Turbi = client.read_holding_registers(address= 0x0055, count= 2, unit= turbiditySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(Turbi.registers,byteorder= Endian.Big, wordorder=Endian.Big)
    Turbidity = decoder.decode_32bit_float()
    return Turbidity


client = ModbusSerialClient(method="rtu", 
                            port= "/dev/ttyUSB1", 
                            stopbits = 1, 
                            bytesize = 8, 
                            parity = 'N', 
                            baudrate= 9600,
                            timeout=1)

if client.connect():
    print(timeNow(),"Client connected")
else:
    print(timeNow(),"Unable to connect")

print (timeNow(),"Approx Time needed for C4E : {} ms\n".format(getSamplingDelayC4E()))          #Reading Sampling delay for C4E
print (timeNow(),"Approx Time needed for pH: {} ms\n".format(getSamplingDelaypH()))             #Reading Sampling delay for pH
print (timeNow(),"Approx Time needed for Turbidity: {} ms\n".format(getSamplingDelayTurbi()))  #Reading Sampling delay for Turbidity

configC4E()     #configuring C4E for measurements:
configpH()      #configuring pH for measurements:
configTurbi()   #configuring turbidity for measurements:

gpio.gpioInit()

gpio.gpioLow()

while True:
    print("Float Status : ",gpio.readFloatStatus())
    startMeasurements()                     # Writting measurement command
    time.sleep(1)                           # Waiting sampling delay
    if getMeasurementStatusC4E() == 0:      # Reading measurements C4E
        print(getMeasurementStatusC4E())
        C4Ekpi = readC4Ekpi()              
        print (timeNow(),"Temperature: {} °C".format(C4Ekpi[0]))
        print (timeNow(),"Conductivity: {} µS/cm".format(C4Ekpi[1]))
        print (timeNow(),"Salinity: {} ppt".format(C4Ekpi[2]))
        print (timeNow(),"TDS: {} ppm\n".format(C4Ekpi[3]))
        #print (timeNow(),"Measurement failed:Current Status -> {}".format(getMeasurementStatusC4E()))
    time.sleep(.5)
    if getMeasurementStatuspH() == 0:       # Reading measurements pH
        pHkpi = readpHkpi()
        print (timeNow(),"pH: {}\n".format(pHkpi))
            #else:
    #    print (timeNow(),"Measurement failed:Current Status -> {}".format(getMeasurementStatuspH()))

    time.sleep(.5)
    if getMeasurementStatusTurbi() == 0:       # Reading measurements Turbidity
       print(getMeasurementStatusTurbi())
       turbiKpi = readTurbiKpi()
       print (timeNow(),"Turbidity: {} NTU\n".format(turbiKpi))
    #else:
        #print (timeNow(),"Measurement failed:Current Status -> {}".format(getMeasurementStatusTurbi()))
    
    time.sleep(.5)
    client.close()
    #time.sleep(1)
    
