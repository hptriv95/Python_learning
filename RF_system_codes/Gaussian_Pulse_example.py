####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is designed to generate a Gaussian pulse, its derivate and their spectrum
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

amplitude = 1.0 # Amplitude for the Gaussian pulse
mean = 1 # Mean for Gaussian pulse
standard_deviation = 0.25  # Standard deviation for the Gaussian pulse
sampling_frequency = 4001 # Sampling frequency
time_steps = np.linspace(-2, 2, sampling_frequency) # Time start, stop and number of steps for computation 
dt = time_steps[1] - time_steps[0] # Value of 1 time step value (spacing between samples)
number_of_time_steps = len(time_steps) # Finds and stores the number of elements in time_steps list

## Variables are set. Block 3 ends
####################

####################
## Create the Gaussian pulse
## Block 4 begins

gaussian_pulse = amplitude * np.exp(-(time_steps - mean)**2 / (2 * standard_deviation**2)) # Generic Gaussian pulse. If this line is enabled, comment the bottom line
#gaussian_pulse = np.gradient(gaussian_pulse, time_steps) # Differentiated Gaussian pulse, enable this line if using differentiated Gaussian pulse

## Gaussian pulse generated. Block 4 ends
####################

####################
## Plot the time domain pulse
## Block 5 begins

plt.figure(figsize=(8, 4)) # 8 inches wide, 4 inches tall
plt.plot(time_steps, gaussian_pulse, label=fr'Gaussian pulse ($\sigma$={standard_deviation})')
plt.title('Generic Gaussian pulse') # If using generic Gaussian pulse, then comment the line below
#plt.title('Shifted and differentiated Gaussian pulse') # If using differentiated Gaussian pulse, then comment the upper line
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

## Gaussian pulse plotted. Block 5 ends
####################

####################
## Generate spectrum for the Gaussian pulse
## Block 6 begins

fft_value = np.fft.fft(gaussian_pulse) # Calculates the DFT using FFT algorithm
fft_value = np.fft.fftshift(fft_value)  # When DFT gets calculated, it is not centred around 0 frequency, this is to centre it
frequency_samples = np.fft.fftfreq(number_of_time_steps, d=dt) # Creates frequency samples corresponding to the FFT values
frequency_samples = np.fft.fftshift(frequency_samples) # Arranges the frequency samples in order to match the properly arranged FFT values 

## Spectrum for the Gaussian pulse is generated . Block 6 ends
####################

####################
## Generate spectrum for the Gaussian pulse
## Block 7 begins

plt.figure(figsize=(8, 4))
spectrum = np.abs(fft_value) * dt # Calculate the magnitude and scales the discrete sum to approximate a continous integral. I f you want to look at the average then instead of multiplying by dt divide by sampling_frequency - 1
plt.plot(frequency_samples, spectrum,color='red', label=fr'Gaussian pulse ($\sigma$={standard_deviation})')
plt.title('Spectrum of Gaussian pulse') # If using generic Gaussian pulse, then comment the line below
#plt.title('Spectrum of shifted and differentiated Gaussian pulse') # If using differentiated Gaussian pulse, then comment the above line
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.legend()
plt.xlim(-10, 10) # This limit is suitable for the pulse made by me to view only the necessary part
plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
