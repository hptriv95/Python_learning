####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code simulates a Sine wave propagating in 1D space with and without boundary condition
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import numpy as np

import matplotlib.pyplot as plt

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## After locating the script, put the location in a variable to later make this directory as simulation directory as well as data saving
## Block 2 begins

simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup necessary variables for simulation
## Block 3 begins

sim_spatial_size = 100 # Let the grid have 100 points
sim_time_steps = 500 # Let the total time steps be 500
speed_of_light = 1 # Normalized speed of light as hav not considered unit of time and distance. They are just points
spatial_step_size = 1 # Size of unit spatial step
time_step = spatial_step_size/(speed_of_light) # Value of unit time step. Taken from stability criteria
electric_field_y = np.zeros(sim_spatial_size) # Initialize a 1D vector for electric field of required size
magnetic_field_x = np.zeros(sim_spatial_size) # Initialize a 1D vector for magnetic field of required size
frequency = 0.025 # Normalized frequency

## Variables are set. Block 3 ends 
####################

####################
## Setup necessary variables for simulation
## Block 4 begins

plt.ion() # Turn on animated plots/continous ploting
fig, ax = plt.subplots(figsize=(8, 4)) 
line, = ax.plot(electric_field_y, 'b-', label='Electric field') # the "," is used to return the line always as ax.plot()[0]. Extracting first element from the list 
ax.set_xlim(0, sim_spatial_size)
ax.set_ylim(-5, 5)
ax.set_xlabel('Spatial Grid Points')
ax.set_ylabel('Amplitude')
ax.set_title('1D FDTD')
ax.grid(True) # Make grids visible

for n in range(sim_time_steps):

    #electric_field_y_previous_run = electric_field_y.copy()# Enable this for first order simple ABC. This command creates a copied version of vector which does not update when the original vactor updates
    electric_field_y[0] = np.sin(2*np.pi*n*frequency*time_step) # First element in vector is given a sin wave source
    for index in range(sim_spatial_size - 1):
        magnetic_field_x[index] = magnetic_field_x[index] + (electric_field_y[index+1] - electric_field_y[index])*(time_step/spatial_step_size) # Add previously held magnetic field value of this grid point to the properly scaled difference of electric field for next grid point and this grid point

    for index in range(1, sim_spatial_size):
        electric_field_y[index] = electric_field_y[index] + (magnetic_field_x[index] - magnetic_field_x[index-1])*(time_step/spatial_step_size) # Add previously held electric field value of this grid point to the properly scaled difference of magnetic field for this grid point and one grid point back

    #electric_field_y[sim_spatial_size - 1] = electric_field_y_previous_run[sim_spatial_size - 2] # Enable this for first order simple ABC. Previous second last grid-point stored value is assigned to the last element 
    
    if n % 2 == 0: # If the remainder when n gets divided by 2 is 0 then go into the defined structure below
        line.set_ydata(electric_field_y) # Update the data on line object every other time step
        fig.canvas.draw() # Draw the figure again
        fig.canvas.flush_events() # Update immediately 

plt.ioff() # Continous plotting turn off
plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################

