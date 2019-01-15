# -*- coding: utf-8 -*-
"""
Created on Thu Oct 04 16:29:40 2018

Test Opal Kelly XEM6001 or XEM7010 pipe API

Just run this script while either of the boards is connected and powered
The pipeTest example bitfile will be flashed to the FPGA
And then we try to write and read to the FPGAs memory using the pipe API

@author: ctw24
"""

############# Check the python version to lead the correct version of the API
import sys
import numpy as np

if sys.version_info[0] == 2:
    import OpalKellyAPIPython2_7.ok as ok  #import the Opal Kelly API
elif sys.version_info[0] == 3:
    import OpalKellyAPIPython3_6.ok as ok  #import the Opal Kelly API



############# Setup the FPGA (and the test the FrontPanel Interface a bit) #############
# https://opalkelly.com/examples/test-the-frontpanel-interface/#tab-python

device = ok.okCFrontPanel()

# Enumerating Devices
# https://opalkelly.com/examples/enumerating-devices/#tab-cpp
deviceCount = device.GetDeviceCount() #The number of devices attached.

for i in range(deviceCount):
    print( 'Device[{0}] Model: {1}'.format( i, device.GetDeviceListModel(i)) )
    print( 'Device[{0}] Serial: {1}'.format(i, device.GetDeviceListSerial(i)) )


# Open the first device available
# https://opalkelly.com/examples/open-the-first-device-available/#tab-python

device.OpenBySerial("")

if not device.IsOpen(): # Returns true if a device is currently open
    sys.exit("No open device found")


# acquire device info
devInfo = ok.okTDeviceInfo()
device.GetDeviceInfo(devInfo)

# print some device information
print("         Product: {}".format(devInfo.productName))
print("Firmware version: {}.{}".format(devInfo.deviceMajorVersion, devInfo.deviceMinorVersion))
print("   Serial Number: {}".format(devInfo.serialNumber))
print("       Device ID: {}".format(devInfo.deviceID.split('\0')[0]))

# identify the FPGA that is connected and choose the appropriate bitfile name
if devInfo.productName == 'XEM6001':
    config_file_name = 'pipetest-xem6001.bit'
elif devInfo.productName == 'XEM7010-A50':
    config_file_name = 'pipetest-xem7010.bit'
else: config_file_name = 'pipetest.bit'

# Download the configuration file onto the FPGA
# https://opalkelly.com/examples/configure-the-fpga/#tab-python
if (device.NoError != device.ConfigureFPGA(config_file_name)):
    sys.exit("FPGA configuration failed.")
                            
                            
                            
                            

#datain = np.empty(16, dtype=int)
#dataout = bytearray(b'11111111111111111111111111')
#datain = bytearray(b'00000000000000000000000000')
## load the bit-file onto the FPGA
#
## 0 seems to indicate no error: 
## https://library.opalkelly.com/library/FrontPanelAPI/classokCFrontPanel.html#a8ba687692ea69eb5d033136b91586d14
#                            
#device.SetWireInValue(0x10, 0xff, 0x01);
#device.UpdateWireIns();
#device.SetWireInValue(0x10, 0x00, 0x01);
#device.UpdateWireIns();
#
#data = device.WriteToPipeIn(0x80, dataout)
#print(datain)
#data = device.ReadFromPipeOut(0xA0, datain)
#print(datain)
#        