####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is intended to run with openEMS
## It generates a halfwave folded dipole made with aluminium metal and then simulates it
## Intended frequency of operation is 0.5 GHz
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import numpy as np

from CSXCAD import CSXCAD

from openEMS import openEMS

from openEMS.physical_constants import *

import matplotlib.pyplot as plt
from matplotlib import cm

from Function_3D_heatmap import threeD_heatmap

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

unit = 1e-3 # All length in mm
mesh_resolution = 2.5 # Mesh cube single side length
centre_frequency = 5e8 # Center frequency, frequency of interest
lambda_centre_frequency = round(C0/centre_frequency/unit) # Wavelength of centre frequency in mm
cutoff_frequency = 4e8 # 20 dB cut-off frequency
dipole_radius = 1.6 # Antenna cylinder wire radius
dipole_length = 105 # Length of antenna cylinder wire section
feed_height = 2.5 #  Feed rectangle height
feed_impedance = 300 # Feed impedance/System impedance
number_points_frequency_sweep = int(2*(cutoff_frequency/1e6) + 1) # Number of points to be swept
curve_radius = 20
number_segments = 200
curve_theta = np.linspace(0, np.pi, number_segments)
simbox = np.array([lambda_centre_frequency + 2*dipole_radius, lambda_centre_frequency + 4*dipole_radius + 4*curve_radius, 2*feed_height + 2*dipole_length + lambda_centre_frequency]) # Radiation box dimensions

#print(len(curve_theta)) # Debug step
#print(curve_theta[99]) # Debug step
# print(number_points_frequency_sweep) # Debug step
## Variables are set. Block 3 ends
####################

####################
## Setup a variable called FDTD and assign to it simulation parameters
## Block 4 begins

FDTD = openEMS(NrTS=30000, CoordSystem=0, EndCriteria=1e-4) # Object FDTD is created/instantiated for the class openEMS, set number of time steps to 30000 and set energy decay criteria to be 0.0001
FDTD.SetGaussExcite(centre_frequency, cutoff_frequency) # Use a gaussian excitation, frequency window being centre_frequency +- cutoff_frequency. The .SetGaussExcite is a method within openEMS class
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8']) # Set boundary of the radiation box to be Perfectly matched layer - PML_8 (8-layer) boundary, it is much better at absorbing than MUR

## FDTD simulation parameters are initialized. Block 4 ends
####################

####################
## Initialize CSXCAD for constructing geometry
## Block 5 begins

CSX = CSXCAD.ContinuousStructure(CoordSystem=0) # Object CSX is created/instantiated and passed on CSXCAD.continousStructures method. It helps to generate geometries
FDTD.SetCSX(CSX) # Links the object FDTD with method setCSX to the CSX object created above
mesh = CSX.GetGrid() # Holds the grid related data
mesh.SetDeltaUnit(unit) # Sets the unit of the grid

## CSXCAD.continuousStrucutre is initialized and set. Block 5 ends
####################

####################
## Generate metal  named aluminium and assign conductivity to it
## Block 6 begins

aluminium = CSX.AddMaterial('aluminium') # Create a metal called aluminium
aluminium.SetMaterialProperty(epsilon=1.0, mue=1.0, kappa=3.6e7) # Set the material properties for ressitve loss

## Generated aluminium metal and assigned property to it. Block 6 ends
####################


####################
## Generate the dipole antenna geometry with aluminium as material assignment
## Block 7 begins

### Cylinder 1 design begins

start_point = [0, 0, feed_height] # start point in 3D for geometry creation
stop_point = [0, 0, feed_height + dipole_length] # stop point in 3D for geometry creation
aluminium.AddCylinder(start_point, stop_point, dipole_radius) # a cylinder is created with aluminium metal which has the given starting and ending points with a defined radius

### Cylinder 1 design ends
### Cylinder 2 design begins

start_point = [0, 0, -feed_height]
stop_point = [0, 0, -feed_height - dipole_length]
aluminium.AddCylinder(start_point, stop_point, dipole_radius)# a cylinder is created with aluminium metal which has the given starting and ending points with a defined radius

### Cylinder 2 design ends
### Upper curved metal design begins
#print(range(len(curve_theta))) # Debug step

curvature_coordinates = [] # Initialize an array
for t in range(len(curve_theta)): # Loop for t values from 0 to 99
    coordinate_point = [0, curve_radius - curve_radius*np.cos(curve_theta[t]), feed_height + dipole_length + curve_radius*np.sin(curve_theta[t])] # Co-ordinates of the curve
    curvature_coordinates.append(coordinate_point) # Append the list
    #print(curvature_coordinates) # Debug step

curvature_coordinates = np.array(curvature_coordinates) # Convert list into array

#print(len(curvature_coordinates)) # Debug step        

for i in range(len(curvature_coordinates) - 1): 
    start_point = curvature_coordinates[i] 
    stop_point = curvature_coordinates[i+1]
    aluminium.AddCylinder(start_point, stop_point, dipole_radius) # Design small arched cylinders in loop to make a semi-circular curved metal

### Upper curved metal design ends
### Cylinder 3 design begins

start_point = [0, 40, -feed_height - dipole_length]
stop_point = [0, 40, feed_height + dipole_length]
aluminium.AddCylinder(start_point, stop_point, dipole_radius)# a cylinder is created with aluminium metal which has the given starting and ending points with a defined radius

### Cylinder 3 design ends
### Lower curved metal design begins

curvature_coordinates = [] # Initialize an array
for t in range(len(curve_theta)): # Loop for t values from 0 to 99
    coordinate_point = [0, curve_radius - curve_radius*np.cos(curve_theta[t]), -feed_height - dipole_length - curve_radius*np.sin(curve_theta[t])] # Co-ordinates of the curve
    curvature_coordinates.append(coordinate_point) # Append the list
    #print(curvature_coordinates) # Debug step

curvature_coordinates = np.array(curvature_coordinates) # Convert list into array

#print(len(curvature_coordinates)) # Debug step        

for i in range(len(curvature_coordinates) - 1): 
    start_point = curvature_coordinates[i] 
    stop_point = curvature_coordinates[i+1]
    aluminium.AddCylinder(start_point, stop_point, dipole_radius) # Design small arched cylinders in loop to make a semi-circular curved metal


## Both arms of dipole antenna are created. Block 7 ends
####################

####################
## Generate the simulation port plane
## Block 8 begins

start_point = [0, -dipole_radius, -feed_height]
stop_point = [0, dipole_radius, feed_height]
port = FDTD.AddLumpedPort(1, feed_impedance, start_point, stop_point, 'z', port_type='voltage', excite=1, priority=10, edges2grid='xy') # A 2 dimension lumped port with voltage excitation is created touching the bottom of 2 arms of dipole antenna

## Simulation port plane generated. Block 8 ends
####################

####################
## Generate simulation box
## Block 9 begins

mesh.AddLine('x', [-simbox[0]/2, simbox[0]/2]) # Defines outer boundary of simulation/meshing domain in x direction
mesh.AddLine('y', [-simbox[1]/2, simbox[1]/2])
mesh.AddLine('z', [-simbox[2]/2, simbox[2]/2])

## Simulation box/Radiation box is generated. Block 9 ends
####################

####################
## Finalize mesh settings and export the geometry, problem setup file to .xml format
## Block 10 begins

mesh.SmoothMeshLines('all', mesh_resolution, 1.4) # Makes the cells size transition gradually, here the ratio of growth is set to 1.4
CSX.Write2XML('Folded_dipole_antenna.xml') # Geometry, problem setup gets dumped in .xml file, which can then be imported to AppCSXCADand verified

nf2ff = FDTD.CreateNF2FFBox() # Creates te near field box. In openEMS the far field characteristics are calculated from nar field. Yet we should keep the radiation box boundary at leas lambda/4 away. For us it is lambda/2 away 

## Ready for simulation, after proper verification. Block 10 ends
####################

####################
## Run simulation. Block 11 begins

path = os.path.join(simulation_path, 'results') # Go to results subdirectory for storing all the results
FDTD.Run(path, cleanup=True) # Temporary files are stored and then deleted using cleanup

## Simulation is initiated. Block 11 ends
####################

####################
## Find Zin and |S11|. Block 12 begins

frequency_sweep = np.linspace(max(1e8,centre_frequency-cutoff_frequency),centre_frequency+cutoff_frequency,number_points_frequency_sweep) # Creates a frequency vector for sweep, with points between start, stop , number of points
port.CalcPort(path, frequency_sweep) # Time domain voltage and curretn signals get converter to frequency domain using fourier transform
Zin = port.uf_tot / port.if_tot # uf_tot is totla voltage at port, uf_tot is total current at port
s11 = port.uf_ref/port.uf_inc # port.uf_ref is reflected wave and port.uf_inc is incident wave
s11_dB = 20.0*np.log10(np.abs(s11)) # s11 in dB

plt.figure() # Creates a figure
plt.plot(frequency_sweep/1e9, Zin.real, label ='Real part of Zin', color ='Blue') # Plots X vs Y
plt.plot(frequency_sweep/1e9, Zin.imag, label ='Imaginary part of Zin', color ='Red') # This would make the figure have both plots, with x-axis being equal and shared
plt.grid(True) # Disp[lay major gridlines
plt.ylabel('Zin real and imaginary (Ohms)') # Y axis label
plt.xlabel('Frequency (GHz)') # X-axis label
plt.ylim(-500,500) # Limit the Y for the plot
plt.title("Zin in Ohms vs Frequency in GHz") # Titile for plot
plt.legend() # Show legend

plt.figure() # Creates a figure
plt.plot(frequency_sweep/1e9, s11_dB, color ='Blue') # Plots X vs Y
plt.grid(True)
plt.ylabel('S|11| (dB)')
plt.xlabel('Frequency (GHz)')
plt.title("|S11| in dB vs Frequency in GHz") # Titile for plot

## Zin and |S11| are calculated and plotted. Block 12 ends
####################

####################
## Calculate toal input power, radiated power, directivity, efficiency at centre frequency
## Plot 2D radiation pattern for theta sweep at phi = 0
## Block 13 begins

centre_index = int(len(frequency_sweep)/2) # Find the centre index = 2.5 GHz
power_input = 0.5*np.real(port.uf_tot[centre_index]*np.conj(port.if_tot[centre_index])) # Power_in is (0.5)real(V*conjugate(I))

### For getting field characteristics

theta = np.arange(0,181,1) # Theta angles in degreees
#phi = [0] # Phi angle for E field cut
phi = np.arange(0,361,1) # Phi angle in degrees

nf2ff_res = nf2ff.CalcNF2FF(path, centre_frequency, theta, phi) # Calculates the far field characterisitc from near field data recorded during simulation
print("E_theta shape:", np.shape(nf2ff_res.E_theta)) 
print("E_phi shape:", np.shape(nf2ff_res.E_phi))
### directivity, efficiency calcualtion

power_radiated = nf2ff_res.Prad
directivity_maximum = nf2ff_res.Dmax # Finds maximum directivity from the data
directivity_dB = 10*np.log10(directivity_maximum) # Converts directivity into dBi
efficiency = (power_radiated/power_input)*100 # It is how efficient the antenna radiates. Efficiency*Directivity = Gain dBi

### 2D radiation pattern generation

Efield = nf2ff_res.E_norm[0] # Pulls in the F-field data for Phi = 0 and all theta and gives it to variable Efield
Efield_normalized = Efield/np.max(Efield) # Normalizes the data with maximum value
Efield_normalized_dB = 20*np.log10(Efield_normalized) # Converts normalized E -feild data into dB
print(Efield_normalized_dB)
plt.figure()
ax = plt.subplot(111, polar=True) # First row, column and first figure polar plot attached to object ax
theta_radians = np.radians(theta)
print(theta_radians)# For polar plot theta needs to be in radians, so converts it
ax.plot(theta_radians, Efield_normalized_dB, color ='Blue')
ax.set_theta_zero_location("N") # Set 0 degree to North
ax.set_theta_direction(-1) # Makes increasing angle as clockwise
ax.set_xlabel('Theta sweep') # labels the axis
plt.title("Radiation Pattern (Phi = 0°)") # Title for plot
plt.grid(True) # Displays major gridlines

### 3D radiation pattern generation

E_theta = np.squeeze(nf2ff_res.E_theta) # Removes the frequency from the data
E_phi   = np.squeeze(nf2ff_res.E_phi) # Removes the frequency from the data
theta = nf2ff_res.theta # After the .CalcNF2FF method is applied to nf2ff object, the theta goes from 0 to Pi approximately (3.14). This is becasue rectangular co-ordinates get converted to sphrecial 
#print(theta)
phi = nf2ff_res.phi # After the .CalcNF2FF method is applied to nf2ff object, the phi goes from 0 to 2Pi approximately (6.28). This is becasue rectangular co-ordinates get converted to sphrecial
#print(phi)
heatmap, axes = threeD_heatmap(E_theta, E_phi, theta, phi) # Pass the values in the () to function and take the output of function and store it in heatmap, axes

## Required parameters are calculated and radiation pattern is plotted. Block 13 ends
####################

####################
## Prints the calculated value and displays the figures
## Final block, block 14 begins

print( 'Input power: Pin = {} Watt'.format(power_input))# Prints input power
print( 'Radiated power: Prad = {} Watt'.format(power_radiated)) # Prints radiated power
print( 'Directivity:    Dmax = {} dBi'.format(directivity_dB)) # Prints the directivity
print( 'Efficiency:     nu_rad = {} %'.format(efficiency)) # Prints efficiency

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
