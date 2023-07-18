#import sensors
#from datetime import datetime
from time import sleep
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder 
from pymodbus.constants import Endian
import MQTT
import json
from time import sleep

flowMeterIn = 1
flowMeterOut = 10

def readInstanteniousFlowIn():
    instanteniousFlowIn = client.read_input_registers(address = 0x1010, count = 2, unit = flowMeterIn)
    decoder = BinaryPayloadDecoder.fromRegisters(instanteniousFlowIn.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    instanteniousFlowInVal = decoder.decode_32bit_float()
    FlowIn = json.dumps({"FlowIn": instanteniousFlowInVal}, indent= 2)
    return FlowIn

def readInstanteniousFlowOut():
    instanteniousFlowOut = client.read_input_registers(address = 0x1010, count = 2, unit = flowMeterOut)
    decoder = BinaryPayloadDecoder.fromRegisters(instanteniousFlowOut.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    instanteniousFlowOutVal = decoder.decode_32bit_float()
    FlowOut = json.dumps({"FlowOut": instanteniousFlowOutVal}, indent= 2)
    return FlowOut

def readCumulativeVal_In():
    readCumulativeInt_In = client.read_input_registers(address = 0x1018, count = 2, unit = flowMeterIn)
    decoder = BinaryPayloadDecoder.fromRegisters(readCumulativeInt_In.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    cumIntVal_In = decoder.decode_32bit_int()
    cumulativeDec_In = client.read_input_registers(address = 0x101A, count = 2, unit = flowMeterIn)
    decoder = BinaryPayloadDecoder.fromRegisters(cumulativeDec_In.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    cumDecVal_In = decoder.decode_32bit_float()
    cumValIn = json.dumps({"TotalFlow_In": (cumIntVal_In+cumDecVal_In)}, indent= 2)
    return cumValIn

def readCumulativeVal_Out():
    cumulativeInt_Out = client.read_input_registers(address = 0x1018, count = 2, unit = flowMeterOut)
    decoder = BinaryPayloadDecoder.fromRegisters(cumulativeInt_Out.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    cumIntVal_Out = decoder.decode_32bit_int()
    cumulativeDec_Out = client.read_input_registers(address = 0x101A, count = 2, unit = flowMeterOut)
    decoder = BinaryPayloadDecoder.fromRegisters(cumulativeDec_Out.registers,byteorder= Endian.Big, wordorder= Endian.Big)
    cumDecVal_Out = decoder.decode_32bit_float()
    cumValOut = json.dumps({"TotalFlow_Out": (cumIntVal_Out+cumDecVal_Out)}, indent=2)
    return cumValOut

def connectionStatus():
    if client.connect():
        return True
    else:
        print("Unable to connect")

client = ModbusSerialClient(method="rtu", 
                            port= "/dev/ttyUSB0", 
                            stopbits = 1, 
                            bytesize = 8, 
                            parity = 'N', 
                            baudrate= 9600,
                            timeout=1)


e_code01 = json.dumps({"code" : "101"})
e_code02 = json.dumps({"code" : "102"})

sleep(30)

while connectionStatus():
    print("Flowmeter Client connected")
    try:
        MQTT.clientPing.publish("newvisiontopic/flow_In",readInstanteniousFlowIn())
        MQTT.clientPing.publish("newvisiontopic/totalFlow_In",readCumulativeVal_In())
    except AttributeError:
        print("Error code Published")
        MQTT.clientPing.publish("Error_code", e_code01)

    try:
        MQTT.clientPing.publish("newvisiontopic/flow_Out", readInstanteniousFlowOut())
        MQTT.clientPing.publish("newvisiontopic/totalFlow_Out", readCumulativeVal_Out())
    except AttributeError:
        print("Error code Published")
        MQTT.clientPing.publish("Error_code", e_code02)
    print("Flowmeter data published")
    sleep(1)