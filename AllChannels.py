import sys
import time
import traceback
from PhidgetHelperFunctions import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

def onAttachHandler(self):
    ph = self
    try:
        print("\n\tSetting DataInterval to 8ms")
        ph.setDataInterval(8)

        print("\tSetting Voltage Ratio ChangeTrigger to 0.0000132")
        ph.setVoltageRatioChangeTrigger(0.0000050)

        if(ph.getchannelsubclass() == channelsubclass.phidchsubclass_voltageratioinput_sensor_port):
            print("\tSetting VoltageRatio SensorType")
            ph.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO)

        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()

    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

def onDetachHandler(self):
    ph = self
    try:
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()

    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

def onErrorHandler(self, errorCode, errorString):
    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" +      str(errorCode) + ")\n")

def raw(ch0, ch1, ch2, ch3):
    print("Channel 0: " , ch0.getVoltageRatio() , "    Channel 1: "  ,  ch1.getVoltageRatio() , "    Channel 2: " +  ch2.getVoltageRatio() , "    Channel 3 : " , -ch3.getVoltageRatio())

def conv(ch0, ch1, ch2, ch3, cal0, cal1, cal2, cal3):

    raw0 = -ch0.getVoltageRatio()
    raw1 = -ch1.getVoltageRatio()
    raw2 = -ch2.getVoltageRatio()
    raw3 = -ch3.getVoltageRatio()

    out0 = (raw0 - cal0)*52742
    out1 = (raw1 - cal1)*49407
    out2 = (raw2 - cal2)*54889
    out3 = (raw3 - cal3)*54664

    f = lambda x,t: 0 if x < t  else x
    d0 = f(out0, 0.15 )
    d1 = f(out1, 0.15 )
    d2 = f(out2, 0.15 )
    d3 = f(out3, 0.15 )

    print("\n")
    print("Channel 0: cal = {} raw = {} out = {} kg".format(cal0, raw0, d0))
    print("#"*int((d0*10)//1)+"\n")

    print("Channel 1: cal = {} raw = {} out = {} kg".format(cal1, raw1, d1))
    print("#"*int((d1*10)//1)+"\n")

    print("Channel 2: cal = {} raw = {} out = {} kg".format(cal2, raw2, d2))
    print("#"*int((d2*10)//1)+"\n")

    print("Channel 3: cal = {} raw = {} out = {} kg".format(cal3, raw3, d3))
    print("#"*int((d3*10)//1)+"\n")

def convo(d):
    n = int(d*10)
    t = " "
    for x in range (0, n):
        t+="#"
    return t

def main():
    try:
        try:
            ch0 = VoltageRatioInput()
            ch1 = VoltageRatioInput()
            ch2 = VoltageRatioInput()
            ch3 = VoltageRatioInput()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t" + e)
            raise


        " Set matching parameters to specify which channel to open"
        ch0.setDeviceSerialNumber(494011)
        ch0.setChannel(0)
        ch1.setDeviceSerialNumber(494011)
        ch1.setChannel(1)
        ch2.setDeviceSerialNumber(494011)
        ch2.setChannel(2)
        ch3.setDeviceSerialNumber(494011)
        ch3.setChannel(3)

        " event handlers before calling open so that no events are missed. "
        print("\n--------------------------------------")

        print("\nSetting OnAttachHandler...")
        ch0.setOnAttachHandler(onAttachHandler)
        ch1.setOnAttachHandler(onAttachHandler)
        ch2.setOnAttachHandler(onAttachHandler)
        ch3.setOnAttachHandler(onAttachHandler)

        print("Setting OnDetachHandler...")
        ch0.setOnDetachHandler(onDetachHandler)
        ch1.setOnDetachHandler(onDetachHandler)
        ch2.setOnDetachHandler(onDetachHandler)
        ch3.setOnDetachHandler(onDetachHandler)

        print("Setting OnErrorHandler...")
        ch0.setOnErrorHandler(onErrorHandler)
        ch1.setOnErrorHandler(onErrorHandler)
        ch2.setOnErrorHandler(onErrorHandler)
        ch3.setOnErrorHandler(onErrorHandler)

        print("\nSetting onVoltageRatioChangeHandler...")
        #ch0.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
        #ch1.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
        #ch2.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
        #ch3.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)

        " Open the channel with a timeout "
        print("\nOpening and Waiting for Attachment...")
        try:
            ch0.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch0)
            raise EndProgramSignal("Program Terminated: Open Failed")
        try:
            ch1.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch1)
            raise EndProgramSignal("Program Terminated: Open Failed")
        try:
            ch2.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch2)
            raise EndProgramSignal("Program Terminated: Open Failed")
        try:
            ch3.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch3)
            raise EndProgramSignal("Program Terminated: Open Failed")

        for  n in range (100):
            cal0 = -ch0.getVoltageRatio()
            cal1 = -ch1.getVoltageRatio()
            cal2 = -ch2.getVoltageRatio()
            cal3 = -ch3.getVoltageRatio()
            time.sleep(0.008)

        while True:
            conv(ch0, ch1, ch2, ch3, cal0, cal1, cal2, cal3)
            time.sleep(0.008)

        #Print(ch0.getVoltageRatio())
        print(" Press enter to exit ")
        readin = sys.stdin.readline()
        " Perform clean up and exit "

        print("\nDone Sampling...")
        print("Cleaning up...")
        ch0.close()
        ch1.close()
        ch2.close()
        ch3.close()
        print("\nExiting...")
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        ch0.close()
        ch1.close()
        ch2.close()
        ch3.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        ch0.close()
        ch1.close()
        ch2.close()
        ch3.close()
        return 1
main()

