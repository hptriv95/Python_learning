####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code plots normalized |array factor| and radiation pattern for Hertzian dipole array
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
## After locating the script, put the location in a variable. This is sanity check
## Make a start timestamp.Block 2 begins

start_timestamp = time.perf_counter()
#print(start_timestamp) # Debug step
simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable named simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup necessary variables for simulation
## Block 3 begins

centre_frequency = 2.47e9 # Centre frequency
speed_of_light = 3e8 # Speed of light
lambda_centre_frequency = (speed_of_light)/(centre_frequency) # Wavelength of centre frequency
number_of_antennas = 4 # Number of antennas
antenna_spacing = lambda_centre_frequency/2 # Spacing between elements
beta_phase_constant = (2*np.pi)/(lambda_centre_frequency) # Phase constant
theta = np.arange(0,181,1) # Theta sweep
phi = np.arange(0,361,1) # Phi sweep
theta_radians = np.radians(theta) # Convert the theta in degrees to radians
phi_radians = np.radians(phi) 
phase_difference = -90 # Phase difference between succcessive elements. For thirty degrees beam steering keep this -90 and for 60 degrees keep it -156
phase_difference_radians = np.radians(phase_difference) # Convert phase difference in degree to radians
psi = (beta_phase_constant)*(antenna_spacing)*(np.sin(theta_radians))*(np.sin(phi_radians[91]))+(phase_difference_radians) # psi function from array factor derivation

## Variables are set. Block 3 ends
####################

####################
## Genreate normalized array factor and radiation pattern for the required setup
## Block 4 begins

array_factor = np.sin(number_of_antennas*psi/2)/((number_of_antennas)*(np.sin(psi/2))) # Normalized array factor
pattern = np.sin(theta_radians)*array_factor # Overall radiation pattern
    
## Normalized array factor and radiation pattern are generated. Block 4 ends
####################

####################
## Plot the result. Make an end time stamp and find time taken
## Block 5 begins

plt.figure()
ax = plt.subplot(111, polar=True) # First row, column and first figure polar plot attached to object ax
theta_radians = np.radians(theta) # For polar plot theta needs to be in radians, so converts it
ax.plot(theta_radians, abs(array_factor), color ='Red', label='Array_factor')
ax.plot(theta_radians, pattern, color ='Blue', label='Radiation_pattern')
ax.set_theta_zero_location("N") # Set 0 degree to North
ax.set_theta_direction(-1) # Makes increasing angle as clockwise
ax.set_xlabel('Theta sweep') # Labels the axis
plt.title("Normalized |array factor| and radiation pattern (Phi = 90°)") # Title for plot
plt.grid(True) # Displays major gridlines
plt.legend() # Display legend
end_timestamp = time.perf_counter() # Time step at the end
#print(end_timestamp) # Debug step
time_taken = end_timestamp - start_timestamp # Will hold the value in seconds
print('Time taken by code is {:.6f} seconds'.format(time_taken)) # Formatting for time is such that it will have 6 digit precision after decimal and will be in floating point format

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
