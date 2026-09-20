####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code finds the solution of a quadratic equation using bisection method
## It generates an excel file which can be studied to find the result
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import time

import sys

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## After locating the script, put the location in a variable to later make this directory as simulation directory as well as data saving
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

independentvariable_x = np.linspace(-25,25,51) # Independent variable which is swept in uniform steps from 0.5 to 10 with 20 steps
#print(independentvariable_x) # Debug step
funct_of_x = (independentvariable_x**2) -7.5*(independentvariable_x) -25 # Function of independent varaible x
lower_limit_x = -7 # Lower limit initialization 
upper_limit_x = 17 # Upper limit initialization 
middle_value_x = ((lower_limit_x) + (upper_limit_x))/2 # Middle value initialization 
funct_of_x_at_lower_limit = (lower_limit_x**2) -7.5*(lower_limit_x) -25 # Value of function at lower limit
funct_of_x_at_upper_limit = (upper_limit_x**2) -7.5*(upper_limit_x) -25 # Value of function at upper limit
funct_of_x_middle_value = (middle_value_x**2) -7.5*(middle_value_x) -25 # Value of function at middle value
product_of_funct_lower_upper_limit = (funct_of_x_at_lower_limit)*(funct_of_x_at_upper_limit) # Product of function at lower limit and upper limit
error = -funct_of_x_middle_value # Error initialization

total_iterations = 25 # Total number of iterations for find optimal deltaX

lower_limit_list = [] # Initialize a list to hold lower limit values
upper_limit_list = [] # Initialize a list to hold upper limit values
middle_value_list = [] # Initialize a list to hold middle values
funct_of_x_middle_value_list = [] # Initialize a list to hold the function values at the middle values
error_list = [] # Initialize a list to hold error values

lower_limit_list.append(lower_limit_x) # Append the list
upper_limit_list.append(upper_limit_x)
middle_value_list.append(middle_value_x)
funct_of_x_middle_value_list.append(funct_of_x_middle_value)
error_list.append(error)

## Variables are set. Block 3 ends
####################

####################
## Check the product of intial values, if it is positive then terminate the simulation
## Block 4 begins

if product_of_funct_lower_upper_limit > 0: # If the product of initial function values are > 0 exit the script and display the below message 
    print('The initial value choosen for the bisection method are need to be changed. Revisit the plot!') 
    sys.exit()
    
## Variables are set. Block 4 ends
####################

####################
## Interchange the upper limit with lower limit if the value of function at lower limit is > value of function at upper limit
## Block 5 begins

if funct_of_x_at_lower_limit > funct_of_x_at_upper_limit: # If the value of function at lower limit is greater than the upper limit, then exchange the limit values
    variable_holder = upper_limit_x
    upper_limit_x = lower_limit_x
    lower_limit = variable_holder
    
## Limits are good for processing. Block 5 ends
####################

####################
## Find the solution of quadratic equation and store the important parameters in their respective list
## Block 6 begins

for iterations in range(0, total_iterations+1): # This for loop will increase the iteration upto total iteration set 

    if funct_of_x_middle_value > 0:
        upper_limit_x = middle_value_x

    elif funct_of_x_middle_value < 0:
        lower_limit_x = middle_value_x

    else:
        print('Function is solved. The current middle value is the solution') 
        break

    middle_value_x = ((lower_limit_x) + (upper_limit_x))/2 # Update the middle value
    funct_of_x_middle_value = (middle_value_x**2) -7.5*(middle_value_x) -25 # Update the funciton with new middle value
    error = -funct_of_x_middle_value # Update error
    lower_limit_list.append(lower_limit_x) # Append the list
    upper_limit_list.append(upper_limit_x)
    middle_value_list.append(middle_value_x)
    funct_of_x_middle_value_list.append(funct_of_x_middle_value)
    error_list.append(error)
    
## Root is found, parameters are stored. Block 6 ends
####################

####################
## Convert the generated data into an excel file
## Block 7 begins

dataframe_lower_x = pd.DataFrame(lower_limit_list, columns=['LOWER_LIMIT_X']) # Convert the list to dataframe with specified column name    
dataframe_upper_x = pd.DataFrame(upper_limit_list, columns=['UPPER_LIMIT_X']) 
dataframe_middle_x = pd.DataFrame(middle_value_list, columns=['CENTRAL_X']) 
dataframe_function_value_list = pd.DataFrame(funct_of_x_middle_value_list, columns=['FUNCTION_VALUE']) 
dataframe_error_list = pd.DataFrame(error_list, columns=['ERROR'])

dataframe_combined = pd.concat([dataframe_lower_x, dataframe_upper_x,  dataframe_middle_x, dataframe_function_value_list, dataframe_error_list], axis=1) # Merge the dataframe in a way that columns are side by side
dataframe_combined.to_excel('Bisection_method_quadratic.xlsx', index=False) # Convert the combined dataframe to excel and do not include the index

## Excel file generated. Block 7 ends
####################

####################
## Make an end time stamp and find time taken. Block 8 begins

end_timestamp = time.perf_counter() # Time step at the end
#print(end_timestamp) # Debug step
time_taken = end_timestamp - start_timestamp # Will hold the value in seconds
print('Time taken by code is {:.6f} seconds'.format(time_taken)) # Formatting for time is such that it will have 6 digit precision after decimal and will be in floating point format

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
