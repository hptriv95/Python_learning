####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code finds the integral of xln(x) between x=3 and x=6
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
funct_of_x = independentvariable_x*np.log(independentvariable_x) # Function of independent varaible x
integration_lower_limit = 3 # Lower limit for integration
integration_upper_limit = 6 # Upper limit for integration
funct_of_x_at_lower_limit = integration_lower_limit*np.log(integration_lower_limit) # Value of function at lower limit
funct_of_x_at_upper_limit = integration_upper_limit*np.log(integration_upper_limit) # Value of function at upper limit
summation_of_halved_upper_lower_limit_terms = (funct_of_x_at_lower_limit + funct_of_x_at_upper_limit)/2 # Halved summation terms
summation_of_middle_terms = 0 # Initialized to a value of 0
delta_x = integration_upper_limit - integration_lower_limit # Initialize bin size
intervals = 1 # Initialize a value of 1 for intervals 
delta_x_list = [] # Initialize a list to hold division bin
total_iterations = 25 # Total number of iterations for find optimal deltaX
analytical_integral_value = 20.557915147098496 # Analytical value from calculator rounded off after 10 decimals
integral_list = [] # Initialize a list to hold integral values
error_list = [] # Initialize a list to hold error values
integral_list = [] # Initialize a list to hold integral values

## Variables are set. Block 3 ends
####################

####################
## Setup the trapezoidal integration and find value the integral of xln(x) between x=3 and x=6
## Store important parameters. Block 4 begins

for iterations in range(0, total_iterations+1): # This for loop will increase the iteration upto total iteration set 
    delta_x_list.append(delta_x) # Append the list
    summation_of_middle_terms = 0 # For each increment in iteration, initialize this to 0

    for index in range(1, intervals): # Iterate for the times required
        middle_term = (integration_lower_limit + ((index)*delta_x))*np.log(integration_lower_limit+((index)*delta_x)) # Function formula with increment
        #print(middle_term) # Debug step
        summation_of_middle_terms = summation_of_middle_terms + middle_term # As name suggests
        #print(summation_of_middle_terms) # Debug step

    summation_of_funct_x = summation_of_halved_upper_lower_limit_terms + summation_of_middle_terms # As name suggests
    #print(summation_of_funct_x) # Debug step
    integral_value = delta_x*summation_of_funct_x
    #print(integral_value) # Debug step
    integral_list.append(integral_value) # Append the list 
    error = analytical_integral_value - integral_value # Error from the absolute value
    error_list.append(error) # Append the value of error to the error list
    delta_x = (delta_x)/2 # Divide the value of deltaX by 2
    intervals=intervals*2 # Multiply the intervals by 2 to scale up to match the decreasing bin size


## Integral value is found and parametes are stored. Block 4 ends
####################

####################
## Convert the generated data into an excel file
## Block 5 begins
    
dataframe_delta_x = pd.DataFrame(delta_x_list, columns=['DELTA_X']) # Convert the list to dataframe with specified column name
dataframe_derivative_list = pd.DataFrame(integral_list, columns=['INTEGRAL_VALUE']) # 
dataframe_error_list = pd.DataFrame(error_list, columns=['ERROR'])

dataframe_combined = pd.concat([dataframe_delta_x, dataframe_derivative_list, dataframe_error_list], axis=1) # Merge the dataframe in a way that columns are side by side
dataframe_combined.to_excel('Trapezodial_integration_xlnx.xlsx', index=False) # Convert the combined dataframe to excel and do not include the index

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
