####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code sweeps registers for finding their value
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

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
## Find out register for passing values of voltage and current
## Block 3 begins

pps3005s = ModbusSerialClient(port='COM4', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1) # Create an object and provide necessary values. (serial port, baudrate, parity check=N means No check, One stop bit for end of frame, as names suggests)
pps3005s.connect() # Establish connection

for register_index in range(0, 500): # Sweep the register and check which registers have the value which is in proportion to the value already set in the instrument
    try: # If the code can cause an error or crash, then use this with the except
        read_register = pps3005s.read_holding_registers(address=register_index, count=1, device_id=1)
        if read_register.isError():
            print(f'Register {register_index:02d}: {read_register}') # :02d is the for formatting 0 is padding character, 2 is width of string, d is for decimal
        else:
            print(f'Register {register_index:02d} = {read_register.registers[0]}')
    except Exception as crash: # Catches errors or crashes and stores them in crash
        print(f'Register {register_index:02d}: {crash}')

pps3005s.close() # Close the connection


## Final block ends.Enjoy!
####################
