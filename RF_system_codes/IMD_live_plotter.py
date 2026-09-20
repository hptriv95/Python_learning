####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code plots tunable output response of a third order weakly non-linear system when given 2 sinusoidal inputs
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider # To get the tunable slider

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

frequency_1 = 1.5e9 # Frequency of first input cosine wave
frequency_2 = 2e9 # Let the total time steps be 500
amplitude_1_linear = 0.2 # Amplitude of first tone
amplitude_2_linear = 3 # Amplitude of second tone = Amplitude of second tone
system_coeff_a0 = 0.5 # System co-efficient A0 = DC level
system_coeff_a1 = 10 # System co-efficient A1 = Linear gain
system_coeff_a2 = 0.5 # System co-efficient A2
system_coeff_a3 = 0.1 # System co-efficient A3
number_of_time_steps = 5000000 # Number of time steps in simulation
sim_time = 20e-6 # Total time of simulation
time_steps = np.linspace(0,sim_time,number_of_time_steps) # Sweep time from 0 to 20 us with 5000000 points
delta_time_step = time_steps[1] - time_steps[0] # Value of each time step
span_negative = 0 # X-axis lower limit
span_positive = 5e9 # X-axis upper limit

## Variables are set. Block 3 ends 
####################

####################
## Create the slider for tuning amplitude of the tones and the first, second, third order coefficient and span. I want the slider and spectrum plot in different figures
## Block 4 begins

ax_amplitude_1_linear = plt.axes([0.25, 0.8, 0.6, 0.05]) # [left start place, height, right end place, thickness]
ax_amplitude_2_linear = plt.axes([0.25, 0.7, 0.6, 0.05]) #
ax_system_coeff_a1 = plt.axes([0.25, 0.6, 0.6, 0.05]) #
ax_system_coeff_a2 = plt.axes([0.25, 0.5, 0.6, 0.05]) #
ax_system_coeff_a3 = plt.axes([0.25, 0.4, 0.6, 0.05]) #
ax_span_negative = plt.axes([0.25, 0.3, 0.6, 0.05]) # If RAM is a concern then comment this line
ax_span_positive = plt.axes([0.25, 0.2, 0.6, 0.05]) # If RAM is a concern thenb comment this line

slider_amplitude_1_linear = Slider(ax=ax_amplitude_1_linear, label='Amplitude tone 1', valmin=0.5, valmax=5, valinit=amplitude_1_linear) #
slider_amplitude_2_linear = Slider(ax=ax_amplitude_2_linear, label='Amplitude tone 2', valmin=0.5, valmax=5, valinit=amplitude_2_linear) #
slider_system_coeff_a1 = Slider(ax=ax_system_coeff_a1, label='Coefficient A1', valmin=1, valmax=20, valinit=system_coeff_a1) #
slider_system_coeff_a2 = Slider(ax=ax_system_coeff_a2, label='Coefficient A2', valmin=0.1, valmax=0.5, valinit=system_coeff_a2) #
slider_system_coeff_a3 = Slider(ax=ax_system_coeff_a3, label='Coefficient A3', valmin=0.01, valmax=0.25, valinit=system_coeff_a3) #
slider_span_negative = Slider(ax=ax_span_negative, label='Lower span limit', valmin=-9e9, valmax=9e9, valinit=span_negative) # If RAM is a concern then comment this line
slider_span_positive = Slider(ax=ax_span_positive, label='Upper span limit', valmin=-9e9, valmax=9e9, valinit=span_positive) # If RAM is a concern then comment this line

## Slider generated. Block 4 ends 
####################

####################
## Create the input, output and spectrum for the default settings
## Block 5 begins

x_t = amplitude_1_linear*(np.cos(2*(np.pi)*frequency_1*time_steps)) + amplitude_2_linear*(np.cos(2*(np.pi)*frequency_2*time_steps)) # Input signal - sum of 2 sinusoids
y_t = system_coeff_a0 + system_coeff_a1*(x_t) + system_coeff_a2*(x_t**2) - system_coeff_a3*(x_t**3) # Output of the third order non-linear system

fft_value_x = np.fft.fft(x_t) # Calculates the DFT using FFT algorithm
fft_value_x = np.fft.fftshift(fft_value_x)  # When DFT gets calculated, it is not centred around 0 frequency, this is to centre it

fft_value_y = np.fft.fft(y_t) # Calculates the DFT using FFT algorithm
fft_value_y = np.fft.fftshift(fft_value_y)  # When DFT gets calculated, it is not centred around 0 frequency, this is to centre it

frequency_samples = np.fft.fftfreq(number_of_time_steps, d=delta_time_step) # Creates frequency samples corresponding to the FFT values
frequency_samples = np.fft.fftshift(frequency_samples) # Arranges the frequency samples in order to match the properly arranged FFT values

fig, ax = plt.subplots(figsize=(8, 4))
spectrum = 2*(np.abs(fft_value_y)/(number_of_time_steps)) # Create amplitude accurate single sided/folded spectrum
headroom = (np.max(spectrum) - np.min(spectrum))/10 # Headroom for the y-axis limits
line, = ax.plot(frequency_samples, spectrum, color='red', label='Spectrum of input')
ax.set_xlim(span_negative, span_positive)
ax.set_ylim(np.min(spectrum)-headroom, np.max(spectrum)+headroom)
ax.set_xlabel('Frequency in Hz')
ax.set_ylabel('Amplitude')
ax.set_title('IMD plot')
ax.grid(True) # Make grids visible

## Default input, output and spectrum  generated. Block 5 ends 
####################

####################
## Create a function where the tuned values get passed on to the input, output and reflect changes in spectrum on the same figure as defined before
## Block 6 begins

def tuneable(val): # Function makes the plot real time tuneable

    amplitude_1_linear= slider_amplitude_1_linear.val # Update the value with the current value of the slider
    amplitude_2_linear= slider_amplitude_2_linear.val
    system_coeff_a1 = slider_system_coeff_a1.val
    system_coeff_a2 = slider_system_coeff_a2.val
    system_coeff_a3 = slider_system_coeff_a3.val 
    span_negative = slider_span_negative.val # If RAM is a concern then comment this line
    span_positive = slider_span_positive.val # If RAM is a concern then comment this line
    
    x_t = amplitude_1_linear*(np.cos(2*(np.pi)*frequency_1*time_steps)) + amplitude_2_linear*(np.cos(2*(np.pi)*frequency_2*time_steps)) # Input signal - sum of 2 sinusoids
    y_t = system_coeff_a0 + system_coeff_a1*(x_t) + system_coeff_a2*(x_t**2) - system_coeff_a3*(x_t**3) # Output of the third order non-linear system

    fft_value_x = np.fft.fft(x_t) # Calculates the DFT using FFT algorithm
    fft_value_x = np.fft.fftshift(fft_value_x)  # When DFT gets calculated, it is not centred around 0 frequency, this is to centre it

    fft_value_y = np.fft.fft(y_t) # Calculates the DFT using FFT algorithm
    fft_value_y = np.fft.fftshift(fft_value_y)  # When DFT gets calculated, it is not centred around 0 frequency, this is to centre it

    frequency_samples = np.fft.fftfreq(number_of_time_steps, d=delta_time_step) # Creates frequency samples corresponding to the FFT values
    frequency_samples = np.fft.fftshift(frequency_samples) # Arranges the frequency samples in order to match the properly arranged FFT values

    spectrum = 2*(np.abs(fft_value_y)/(number_of_time_steps))
    ax.set_ylim(np.min(spectrum)-headroom, np.max(spectrum)+headroom) # Scaling the Y-axis as per the scaling of spectrum
    ax.set_xlim(span_negative, span_positive)
    line.set_ydata(spectrum) # Update the spectrum trace
    fig.canvas.draw_idle() # Draw the figure again
    fig.canvas.flush_events() # Update immediately

## Tuneable function created. Block 6 ends 
####################

####################
## Tune the values as required and pass the values to the tuneable function
## Block 7 begins

slider_amplitude_1_linear.on_changed(tuneable)# .on_changed expects a function. Val is attribute within the .on_changed method. When the slider is tuned, the value gets passed to the created tuneable function
slider_amplitude_2_linear.on_changed(tuneable)
slider_system_coeff_a1.on_changed(tuneable)
slider_system_coeff_a2.on_changed(tuneable) 
slider_system_coeff_a3.on_changed(tuneable) 
slider_span_negative.on_changed(tuneable) # If RAM is a concern then comment this line
slider_span_positive.on_changed(tuneable) # If RAM is a concern then comment this line
plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################

