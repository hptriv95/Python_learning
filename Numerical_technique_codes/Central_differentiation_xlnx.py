####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code finds the derivative of xln(x) at x=3
## It generates an excel file which can be studied to find the optimum value of deltaX
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
## Setup necessary variables for simulation
## Block 3 begins

independentvariable_x = np.linspace(0.5,10,20) # Independent variable which is swept in uniform steps from 0.5 to 10 with 20 steps
#print(independentvariable_x) # Debug step
fixed_x = independentvariable_x[5] # Independent variable with fixed value for finding derivative at this point
#print(fixed_x) # Debug step
funct_of_x = independentvariable_x*np.log(independentvariable_x) # Function of independent varaible x
delta_x = 0.1 # Division bin first element
delta_x_list = [] # Initialize a list to hold division bin
total_iterations = 20 # Total number of iterations for find optimal deltaX
derivative_list = [] # Initialize a list to hold derivative values
absolute_derivative_value = 2.0986122887 # Analytical value from calculator rounded off after 10 decimals
error_list = [] # Initialize a list to hold error values 

## Variables are set. Block 3 ends
####################

####################
## Setup the central difference and run itertively for optimum deltaX at x=3
## Block 4 begins

for index in range(0, total_iterations): # Iterate for the times required
    funct_of_x_plus = (fixed_x + delta_x)*(np.log(fixed_x + delta_x)) # f(x+deltaX)
    funct_of_x_minus = (fixed_x - delta_x)*(np.log(fixed_x - delta_x)) # f(x-deltaX)
    derivative_of_funct_of_x = (funct_of_x_plus - funct_of_x_minus)/(2*delta_x) # df(x)/dx
    #print(derivative_of_funct_of_x) # Debug step
    #print(delta_x) # Debug step
    delta_x_list.append(delta_x) # Append the value of deltaX to the list
    derivative_list.append(derivative_of_funct_of_x) # Append the value of derivative to the list
    error = absolute_derivative_value - derivative_of_funct_of_x # Error from the absolute value
    error_list.append(error) # Append the value of error to the error list
    delta_x = (delta_x)/2 # Divide the value of deltaX by 2

## Derivative ad error for the deltaX vlaue are generated. Block 4 ends
####################

####################
## Convert the generated data into an excel file
## Block 5 begins
    
dataframe_delta_x = pd.DataFrame(delta_x_list, columns=['DELTA_X']) # Convert the list to dataframe with specified column name
dataframe_derivative_list = pd.DataFrame(derivative_list, columns=['DERIVATIVE_X']) # 
dataframe_error_list = pd.DataFrame(error_list, columns=['ERROR'])

dataframe_combined = pd.concat([dataframe_delta_x, dataframe_derivative_list, dataframe_error_list], axis=1) # Merge the dataframe in a way that columns are side by side
dataframe_combined.to_excel('Central_derivative_xlnx.xlsx', index=False) # Convert the combined dataframe to excel and do not include the index

## Excel file generated. Block 5 ends
####################

####################
## Generate plot for xln(x). Block 6 begins
## Make an end time stamp and find time taken

plt.figure() # Creates a figure
plt.plot(independentvariable_x, funct_of_x, color='Blue')
plt.title('Plot of F(x) = xlnx vs x') 
plt.grid(True)
plt.xlabel('x')
plt.ylabel('F(x)')

end_timestamp = time.perf_counter() # Time step at the end
#print(end_timestamp) # Debug step
time_taken = end_timestamp - start_timestamp # Will hold the value in seconds
print('Time taken by code is {:.6f} seconds'.format(time_taken)) # Formatting for time is such that it will have 6 digit precision after decimal and will be in floating point format

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
