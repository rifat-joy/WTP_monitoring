#---------- For Modbus -----------#
from datetime import datetime
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder 
from pymodbus.constants import Endian
import json

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

def readC4Ekpi(tank):
    valuesC4E = client.read_holding_registers(address= 0x0053, count= 8, unit= conductivitySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(valuesC4E.registers, byteorder= Endian.Big, wordorder=Endian.Big)
    TemperatureVal = decoder.decode_32bit_float()
    ConductivityVal = decoder.decode_32bit_float()
    SalinityVal = decoder.decode_32bit_float()
    TDSVal = decoder.decode_32bit_float()
    Temperature = json.dumps({"Temperature" : TemperatureVal,"Tank": tank}, indent= 2)
    Conductivity = json.dumps({"Conductivity" : ConductivityVal,"Tank": tank}, indent= 2)
    Salinity = json.dumps({"Salinity" : SalinityVal, "Tank": tank})
    TDS = json.dumps({"TDS" : TDSVal, "Tank": tank})
    print(Temperature)
    print(Conductivity)
    print(Salinity)
    print(TDS)
    return Temperature,Conductivity, Salinity, TDS

def readpHkpi(tank):
    pH_ = client.read_holding_registers(address= 0x0055, count= 2, unit= phSensor)
    decoder= BinaryPayloadDecoder.fromRegisters(pH_.registers,byteorder= Endian.Big, wordorder=Endian.Big)
    pHReading = decoder.decode_32bit_float()
    pH = json.dumps({"pH": pHReading, "Tank": tank}, indent = 2)
    print(pH)
    return pH

def readTurbiKpi(tank):
    Turbi = client.read_holding_registers(address= 0x0055, count= 2, unit= turbiditySensor)
    decoder= BinaryPayloadDecoder.fromRegisters(Turbi.registers,byteorder= Endian.Big, wordorder=Endian.Big)
    TurbidityReading = decoder.decode_32bit_float()
    Turbidity = json.dumps({"Turbidity": TurbidityReading,"Tank": tank}, indent= 2)
    print(Turbidity)
    return Turbidity

def connectionStatus():
    if client.connect():
        #print(timeNow(),"Modbus Client connected")
        return True
    else:
        print(timeNow(),"Unable to connect")

client = ModbusSerialClient(method="rtu", 
                            port= "/dev/ttyUSB1", 
                            stopbits = 1, 
                            bytesize = 8, 
                            parity = 'N', 
                            baudrate= 9600,
                            timeout=1)
