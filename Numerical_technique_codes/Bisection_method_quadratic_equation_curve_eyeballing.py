####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code plots the equation in the provided range
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import time

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## After locating the script, put the location in a variable. This is sanity check
## Make a start timestamp
## Block 2 begins

start_timestamp = time.perf_counter()
#print(start_timestamp) # Debug step
simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup independent variable and define the function
## Block 3 begins

independentvariable_x = np.linspace(-25,25,51) # Independent variable which is swept in uniform steps from -25 to 25 with 51 steps
#print(independentvariable_x) # Debug step
funct_of_x = (independentvariable_x**2) -7.5*(independentvariable_x) -25 # Function of independent varaible x

## Independent variable and function are defined. Block 3 ends 
####################

####################
## Generate plot for the provided function. Block 4 begins
## Make an end time stamp and find time taken

plt.figure() # Creates a figure
plt.plot(independentvariable_x, funct_of_x, color='Blue')
plt.title('Plot of F(x) = (x^2) - 7.5x - 25 vs x') 
plt.grid(True)
plt.xlabel('x')
plt.ylabel('F(x)')

end_timestamp = time.perf_counter() # Time step at the end
#print(end_timestamp) # Debug step
time_taken = end_timestamp - start_timestamp # Will hold the value in seconds
print('Time taken by code is {:.6f} seconds'.format(time_taken))

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
