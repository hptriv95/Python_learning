####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is intended to run with openEMS
## It generates a 3D heatmap from input as E-field data
## Output is the 3D heatmap and axes
## If this code helps you then, cheers!
####################
#################### FUNCTION CODE - NOT TO BE EXECUTED BY ITSELF
####################

## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm # Provides access to colour-map module - jet for our case

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## I have put the script in C:\EM_simulation\Simulation_directory\Dipole_antenna
## After locating the script, put the location in a variable to later make this directory as simulation directory as well as data saving
## Block 2 begins

simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Function is defined
## Block 3 begins

def threeD_heatmap(E_theta, E_phi, theta, phi): 

    E_total = np.sqrt(np.abs(E_theta)**2 + np.abs(E_phi)**2) # Find out the magnitude of E-field
    E_total = E_total/np.max(E_total) # Normalize the E-field with maximum value 
    #print(E_total) # Debug step
    E_total = np.maximum(E_total, 1e-12) # If there is any value less than 1e-12 than replace that with 1e-12. Idea is to avoid 0 
    E_dB = 20 * np.log10(E_total)  # Convert to dB
    #print(20 * np.log10(E_total)) # Debug step
    print("theta min/max (rad):", theta.min(), theta.max()) # Confirmation for full sweep of theta: 0 to Pi
    print("sin(theta) range:", np.min(np.sin(theta)), np.max(np.sin(theta))) # Same as above
    PHI, THETA = np.meshgrid(phi,theta) # Creates a 2D array from 1D array of phi and theta
    R = E_total # Assign magnitude
    X = R * np.sin(THETA) * np.cos(PHI) # Convert spherical co-ordinates to rectangular co-ordinates
    Y = R * np.sin(THETA) * np.sin(PHI) # Convert spherical co-ordinates to rectangular co-ordinates
    Z = R * np.cos(THETA) # Convert spherical co-ordinates to rectangular co-ordinates
    fig = plt.figure(figsize=(8, 4)) # Create an object called fig for plotting the figure
    ax = fig.add_subplot(111, projection='3d') # Create an object called ax ti add axes to the figure
    norm = plt.Normalize(-10, 0) # Strongest value to plot of normalized E-field is 0 dB (1) and weakest value to be plotted is -10 dB.This way colour gradients can be viewed with ease
    colors = cm.jet(norm(E_dB)) # Maps high values to red, than in descending order yellow, green and blue
    print(X.shape, Y.shape, Z.shape) # Debug step. Find out shape of X, Y, Z to confirm
    surface = ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False) # Creates a surface plot, from X, Y, Z grid with colours defined by what we set, makes grid lines invisible and other parts are to smoothen the plot
    heatmap = cm.ScalarMappable(cmap=cm.jet, norm=norm) # Creates a colour bar for the heatmap.Mappable is used to map data to colour
    heatmap.set_array(E_dB) # Use the E_dB data for the colour bar created to make the heatmap 
    fig.colorbar(heatmap, ax=ax, shrink=0.6, label='dB') # Makes the figure, shrinks the colour bar to 0.6*height   
    ax.set_title("3D Radiation Pattern (Heatmap)")
    ax.set_box_aspect([1,1,1])
    return fig, ax # This is the output or the return value of the function

## Final block ends.Enjoy!
####################
