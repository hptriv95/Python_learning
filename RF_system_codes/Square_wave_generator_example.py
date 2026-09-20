####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is designed to generate a Square wave, we can play with number of harmonics
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os # OS library does OS related manipulation tasks

import numpy as np # Used for creating arrays and mathematical computations

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
## Setup necessary variables for simulation
## Block 3 begins

amplitude = 1.0 # Amplitude for the square wave
centre_frequency = 1e6 # Centre frequency of the square wave
number_of_harmonics_wanted = 1 # 0 means only fundamental, you can add the number you want
harmonics = range(0,number_of_harmonics_wanted+1) # 0 means only fundamental, you can add the number you want
total_time_steps = np.linspace(0,5e-6,500)
sin_wave = 0

## Variables are set. Block 3 ends
####################

####################
## Create the Square wave
## Block 4 begins

for n in harmonics:
    sin_wave = sin_wave + (4/(np.pi))*(amplitude/(2*n+1))*np.sin(2*np.pi*centre_frequency*(2*n+1)*total_time_steps) # Square wave generation through adding required number of harmonics of centre frequency 

## Square wave generated. Block 4 ends
####################

####################
## Plot the time domain Square wave
## Block 5 begins

plt.figure(figsize=(8, 4)) # 8 inches wide, 4 inches tall
plt.plot(sin_wave, label='Sin wave')
plt.title('Sine wave')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.show()
## Final block ends.Enjoy!
####################
