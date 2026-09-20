####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is intended to run with the provided excel file
## It generates Nyquist plot considering Magnitude in linear and phase in radians
## This is for the loop gain shown for the OTA circuit
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os # OS library does OS related manipulation tasks

import numpy as np # Used for creating arrays and mathematical computations

import pandas as pd # Pandas is the library for data handling

import matplotlib.pyplot as plt # Used for plotting


## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located for verification
## Block 2 begins

current_directory = os.getcwd()
print(current_directory) # For debug

## Found the directory. Block 2 ends
####################

####################
## Create variables
## Block 3 begins

critical_point_phase = np.pi # Phase of critical point is 180
critical_point_magnitude = 1 # Magnitude of critical point is 1 
maximum_value_limit = 10 # Maximum limit for the magnitude of the polar plot. Set 10 for zoomed in version and 5000 for zoomed out version

## Variables created. Block 3 ends
####################

####################
## Bring in the data from excel file
## Store specific columns into variables
## Block 4 begins

excel_data = pd.read_excel("Nyquist_plot_data.xlsx") # This command reads the named excel file from the location of the script as well as stores it in excel_data
print (excel_data) # This command prints the dataframe read from the above command


magnitude = excel_data[['Magnitude']] # This command takes the data from column called "Magnitude" and stores it in variable/list called magnitude
print (magnitude)

phase_radians = excel_data[['Phase_Radians']]
print (phase_radians)

## Read the file and created necessary variables for plotting Nyquist plot. Block 4 ends
####################

####################
## Plot the data
## Block 5 starts

ax = plt.subplot(111, projection='polar') # Generate a polar plot and give it object ax
ax.plot(phase_radians, magnitude)# Plot(x,y)
ax.plot(-phase_radians, magnitude)# Plot mirror image
ax.set_xlabel('Phase in degrees')
ax.scatter(critical_point_phase, critical_point_magnitude, color='red', marker='o', s=100) # Create marker for the critical point
ax.set_rmax(maximum_value_limit) # Set the maximum limit for the magnitude of polar plot
plt.title("Transfer function magnitude and phase plot") # Title for plot
plt.grid(True) # Displays major gridlines
plt.show()

## Plots are generated. Block 5 ends. Enjoy!
####################



