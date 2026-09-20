####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code alters the voltage and current of the intended instrument
## It is done by passing values to the necessary register
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
## Pass the values to the correct registers
## Block 3 begins

pps3005s = ModbusSerialClient(port='COM4', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1) # Create an object and provide necessary values. (serial port, baudrate, parity check=N means No check, One stop bit for end of frame, as names suggests)
pps3005s.connect() # Establish connection with the provided parameters
output_voltage = pps3005s.write_register(address=48, value=158, device_id=1) # Set the register 48 (voltage set) with the provided value to the ID of intended instrument. Value of 1 represents 10 mV, so 158 is 1.58 V
output_current = pps3005s.write_register(address=49, value=2026, device_id=1) # Set the register 49 (current set) with the provided value to the ID of intended instrument. Value of 1 represents 1 mA, so 2026 is 2.026 A
print(output_voltage)
print(output_current)
pps3005s.close() # Close the connection

## Final block ends.Enjoy!
####################
