####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code lists connected ports, instruments and establishes connection
## with the required test-equipment by finding their device IDs
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import sys # Python interpreter can be communicated with

import serial.tools.list_ports # Scans and lists serial ports

from pymodbus.client import ModbusSerialClient # Establishes connection with instruments

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## This is for sanity check
## Block 2 begins

simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup necessary variables for simulation
## Block 3 begins

ports_list = serial.tools.list_ports.comports()
#print(len(ports_list)) # Debug step
devices = [] # Creates an empty list called devices. This will indicate number of instruments in total
required_port = None # No fixed port is assigned

## Variables are set or initialized. Block 3 ends
####################

####################
## Find out on if equipment is connected and on which port. If it open for communicated
## Then find out the device ID to talk to them
## Block 4 begins

for ports in ports_list: # for number of elements in the ports_list
    print(f'{ports.device} - {ports.description}') # Fetches the name of the HW on serial port and its description
    if 'CH340' in ports.description: # If 'CH340' is detected in the name of the hardware then store it in a variable called required_port. This is to check detection
        required_port = ports.device

if required_port is None: # If no value is asdsigned to required_port
    print('CH340 is not detected')
    sys.exit() # Exit the script
    
pps3005s = ModbusSerialClient( port=required_port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5 ) # Create an object and provide necessary values. (serial port, baudrate, parity check=N means No check, One stop bit for end of frame, as names suggests)

if pps3005s.connect() == 0: # If the commmunication cannot be started. Checking the connection also opens the connection by default
    print('no devices...no connection...')
    sys.exit() # Exit the script


for instrument in range(1,4): # Since I have only one programmable power supply and lot of equipments have their instrument IDs in single digit. Sweep the variable to confirm the ID
    try: # If the code can cause an error or crash, then use this with the except
        read_register = pps3005s.read_holding_registers(address=0, count=1, device_id=instrument) # Read the register for (start value of memory location to be read, how many 16 bit register need to be read, from the provided device ID)

        if read_register.isError() == 0: # If no error is there in reading the register 
            print(f'Detected instrument {instrument}')
            devices.append(instrument) # Add the device_id to list
        else:
            print(f'instrument {instrument}: not detected')

    except Exception as crash: # Catches errors or crashes and stores them in crash
        print(f'Instrument {instrument}: {crash}')
        
pps3005s.close()# Close the connection
print('Detected devices:', devices)

## Final block ends.Enjoy!
####################
