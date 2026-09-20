####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code is intended to run with openEMS
## It generates a 4 element rectangular micrsotrip patch antenn array (ULA)
## Simulates the array and generates results - Directivity, relevant 2D E-Field pattern cuts and 3D heatmqap
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import numpy as np

from CSXCAD import CSXCAD

from openEMS import openEMS

import math

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
centre_frequency = 2.47e9 # Center frequency, frequency of interest
lambda_centre_frequency = round(C0/centre_frequency/unit) # Wavelength of centre frequency in mm
cutoff_frequency = 0.5e9 # 20 dB cut-off frequency
mesh_resolution = 1 # Mesh resolution
patch_width  = 36.4 # patch width in x-direction
patch_length = 28.25 # patch length in y-direction
cut_out_length = 8.28 # Air gap cut out length
cut_out_width = 4.9 # Air gap cut out width
feed_line_length = 18.28 # Feed line length
feed_line_width = 3 # Feed line width
notch_width = 0.95 # Notch between feed line and antenna edge
substrate_epsR   = 4.4 # Substrate permitivity
substrate_kappa  = 15e-3 * 2*np.pi*2.5e9 * EPS0*substrate_epsR # Loss tangent
substrate_width  = 49.2 # Substrate width
substrate_length = 52 # Substrate length
substrate_thickness = 1.6 # Substrate height/thickness
substrate_cells = 4 # Number of Z direction substrate cells where the meshing will be done
feed_R= 50 # Feed impedance
offset = 24 # Offset between edges of 2 successve patches
constant_delay = 1/centre_frequency
phase_delay = -90 # Phase delay between successive elements for directional beams. Keep 0 for boresight, -90 for theta=30, -156 for theta=60
phase_delay_time = abs((phase_delay)/360)*(1/centre_frequency) # Converts phase delay to time delay. No matter what is entered above, this makes sure that the time delay corresponding to the phase delya is positive
simbox_x = lambda_centre_frequency + substrate_width  # Radiation/Simulation box overall X-direction length
simbox_y = lambda_centre_frequency + substrate_length # Radiation/Simulation box overall Y-direction length
simbox_z = lambda_centre_frequency + substrate_thickness  # Radiation/Simulation box overall Z-direction length
simbox = np.array([simbox_x, simbox_y, simbox_z]) # Array for creating simulation box

## Variables are set. Block 3 ends
####################

####################
## Setup a variable called FDTD and assign to it simulation parameters
## Block 4 begins

FDTD = openEMS(NrTS=60000, CoordSystem=0, EndCriteria=1e-6) # Object FDTD is created/instantiated for the class openEMS, set number of time steps to 60000 and set energy decay criteria to be 0.000001. If RAM and CPU are limitation then set the energy decay to 1e-4!
FDTD.SetGaussExcite(centre_frequency, cutoff_frequency) # Use a gaussian excitation, frequency window being centre_frequency +- cutoff_frequency. The .SetGaussExcite is a method within openEMS class
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8']) # Set boundary of the radiation box to be Perfectly matched layer - PML_8 (8-layer) boundary, it is much better at absorbing than MUR. Remember PML_8 will significantly increase simulaiton time compared to MUR!

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
## Generate the microstrip patch array geometry with PEC as material assignment
## Block 6 begins

### Generate leftmost patch

patch = CSX.AddMetal('patch') # Create a perfect electric conductor (PEC)
start = [-(patch_width/2) - 3*((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [(patch_width/2) - 3*((offset/2)+(patch_width/2)), patch_length/2, substrate_thickness]
patch.AddBox(priority=10, start=start, stop=stop) # Add a box-primitive to the metal property 'patch'
FDTD.AddEdges2Grid(dirs='xy', properties=patch, metal_edge_res=mesh_resolution/2)

air = CSX.AddMaterial('air', epsilon=1) # Create air cut-out with higher priority)
start = [-((feed_line_width/2) + notch_width) - 3*((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [((feed_line_width/2) + notch_width) - 3*((offset/2)+(patch_width/2)), -((patch_length/2) - cut_out_length), substrate_thickness]
air.AddBox(priority=11, start=start, stop=stop) # Add a box-primitive to the air property 'air'
FDTD.AddEdges2Grid(dirs='xy', properties=air, metal_edge_res=mesh_resolution/2)

feedline = CSX.AddMetal('feedline') # Create a perfect electric conductor (PEC)
start = [-feed_line_width/2 - 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
stop  = [ feed_line_width/2 - 3*((offset/2)+(patch_width/2)), -(patch_length/2 - cut_out_length), substrate_thickness]
feedline.AddBox(priority=13, start=start, stop=stop) # Add a box-primitive to the metal property 'feedline'
FDTD.AddEdges2Grid(dirs='xy', properties=feedline, metal_edge_res=mesh_resolution/2)

### Generate inner left patch

start = [-(patch_width/2) - ((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [(patch_width/2) - ((offset/2)+(patch_width/2)), patch_length/2, substrate_thickness]
patch.AddBox(priority=10, start=start, stop=stop) # Add a box-primitive to the metal property 'patch'
FDTD.AddEdges2Grid(dirs='xy', properties=patch, metal_edge_res=mesh_resolution/2)

start = [-((feed_line_width/2) + notch_width) - ((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [((feed_line_width/2) + notch_width) - ((offset/2)+(patch_width/2)), -((patch_length/2) - cut_out_length), substrate_thickness]
air.AddBox(priority=11, start=start, stop=stop) # Add a box-primitive to the air property 'air'
FDTD.AddEdges2Grid(dirs='xy', properties=air, metal_edge_res=mesh_resolution/2)

start = [-feed_line_width/2 - ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
stop  = [ feed_line_width/2 - ((offset/2)+(patch_width/2)), -(patch_length/2 - cut_out_length), substrate_thickness]
feedline.AddBox(priority=13, start=start, stop=stop) # Add a box-primitive to the metal property 'feedline'
FDTD.AddEdges2Grid(dirs='xy', properties=feedline, metal_edge_res=mesh_resolution/2)

### Generate inner right patch

start = [-(patch_width/2) + ((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [(patch_width/2) + ((offset/2)+(patch_width/2)), patch_length/2, substrate_thickness]
patch.AddBox(priority=10, start=start, stop=stop) # Add a box-primitive to the metal property 'patch'
FDTD.AddEdges2Grid(dirs='xy', properties=patch, metal_edge_res=mesh_resolution/2)

start = [-((feed_line_width/2) + notch_width) + ((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [((feed_line_width/2) + notch_width) + ((offset/2)+(patch_width/2)), -((patch_length/2) - cut_out_length), substrate_thickness]
air.AddBox(priority=11, start=start, stop=stop) # Add a box-primitive to the air property 'air'
FDTD.AddEdges2Grid(dirs='xy', properties=air, metal_edge_res=mesh_resolution/2)

start = [-feed_line_width/2 + ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
stop  = [ feed_line_width/2 + ((offset/2)+(patch_width/2)), -(patch_length/2 - cut_out_length), substrate_thickness]
feedline.AddBox(priority=13, start=start, stop=stop) # Add a box-primitive to the metal property 'feedline'
FDTD.AddEdges2Grid(dirs='xy', properties=feedline, metal_edge_res=mesh_resolution/2)

### Generate inner rightmost patch

start = [-(patch_width/2) + 3*((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [(patch_width/2) + 3*((offset/2)+(patch_width/2)), patch_length/2, substrate_thickness]
patch.AddBox(priority=10, start=start, stop=stop) # Add a box-primitive to the metal property 'patch'
FDTD.AddEdges2Grid(dirs='xy', properties=patch, metal_edge_res=mesh_resolution/2)

start = [-((feed_line_width/2) + notch_width) + 3*((offset/2)+(patch_width/2)), -patch_length/2, substrate_thickness]
stop  = [((feed_line_width/2) + notch_width) + 3*((offset/2)+(patch_width/2)), -((patch_length/2) - cut_out_length), substrate_thickness]
air.AddBox(priority=11, start=start, stop=stop) # Add a box-primitive to the air property 'air'
FDTD.AddEdges2Grid(dirs='xy', properties=air, metal_edge_res=mesh_resolution/2)

start = [-feed_line_width/2 + 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
stop  = [ feed_line_width/2 + 3*((offset/2)+(patch_width/2)), -(patch_length/2 - cut_out_length), substrate_thickness]
feedline.AddBox(priority=13, start=start, stop=stop) # Add a box-primitive to the metal property 'feedline'
FDTD.AddEdges2Grid(dirs='xy', properties=feedline, metal_edge_res=mesh_resolution/2)

### Microstrip patch array geometry generated. Block 6 ends
####################

####################
## Generate the substrate and ground plane for the microstrip patch
## Block 7 begins

substrate = CSX.AddMaterial('substrate', epsilon=substrate_epsR, kappa=substrate_kappa) # Create a substrate with provided permitivity and loss tangent
start = [-substrate_width/2 - 3*((offset/2)+(patch_width/2)), -substrate_length/2, 0]
stop  = [ substrate_width/2 + 3*((offset/2)+(patch_width/2)),  substrate_length/2, substrate_thickness]
substrate.AddBox( priority=0, start=start, stop=stop )

gnd = CSX.AddMetal('gnd') # Create a perfect electric conductor (PEC)
start[2]=0
stop[2] =0
gnd.AddBox(start, stop, priority=10)
FDTD.AddEdges2Grid(dirs='xy', properties=gnd)

### Substrate and ground plane generated. Block 7 ends
####################

####################
## Generate simulaiton port plane. Observe the delay here!
## Block 8 begins

### Generate the excitation for leftmost patch

start = [0 - 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), 0]
stop  = [0 - 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
port_1 = FDTD.AddLumpedPort(3, feed_R, start, stop, 'z', excite=1, delay=constant_delay - 3*(phase_delay_time/2), priority=14, edges2grid='xy') # A 2 dimension lumped port with voltage excitation is created and assigned the given priority

### Generate the excitation for inner left patch

start = [0 - ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), 0]
stop  = [0 - ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
port_1 = FDTD.AddLumpedPort(1, feed_R, start, stop, 'z', excite=1, delay=constant_delay - (phase_delay_time/2), priority=14, edges2grid='xy') # A 2 dimension lumped port with voltage excitation is created and assigned the given priority

### Generate the excitation for inner right patch

start = [0 + ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), 0]
stop  = [0 + ((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
port_2 = FDTD.AddLumpedPort(2, feed_R, start, stop, 'z', excite=1, delay=constant_delay + (phase_delay_time/2), priority=14, edges2grid='xy') # A 2 dimension lumped port with voltage excitation is created and assigned the given priority

### Generate the excitation for rightmost patch

start = [0 + 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), 0]
stop  = [0 + 3*((offset/2)+(patch_width/2)), -((patch_length/2) + feed_line_length - cut_out_length), substrate_thickness]
port_4 = FDTD.AddLumpedPort(4, feed_R, start, stop, 'z', excite=1, delay=constant_delay + 3*(phase_delay_time/2), priority=14, edges2grid='xy') # A 2 dimension lumped port with voltage excitation is created and assigned the given priority 

### Simulation port plane generated. Block 8 ends
####################

####################
## Generate simulation box
## Block 9 begins

mesh.AddLine('x', [-(simbox[0]/2) - 3*((offset/2)+(patch_width/2)), (simbox[0]/2) + 3*((offset/2)+(patch_width/2))]) # Defines outer boundary of simulation/meshing domain in x direction
mesh.AddLine('y', [-simbox[1]/2, simbox[1]/2])
mesh.AddLine('z', [-simbox[2]/3, simbox[2]*2/3])

### Simulation box generated. Block 9 ends
####################

####################
## Finalize mesh settings and export the geometry, problem setup file to .xml format
## Block 10 begins

mesh.AddLine('z', np.linspace(0,substrate_thickness, substrate_cells+1)) # Substrate gets divided into substrate cell number with +1 as boundary. So here 4 cells and total 5 boundaries (including top and bottom)
mesh.SmoothMeshLines('all', mesh_resolution, 1.4) # Makes the cells size transition gradually, here the ratio of growth is set to 1.4
CSX.Write2XML('Microstrip_patch_uniform_linear_array.xml') # Geometry, problem setup gets dumped in .xml file, which can then be imported to AppCSXCADand verified
nf2ff = FDTD.CreateNF2FFBox() # Creates te near field box. In openEMS the far field characteristics are calculated from nar field. Yet we should keep the radiation box boundary at leas lambda/4 away. For us it is lambda/2 away 

###  Ready for simulation, after proper verification. Block 10 ends
####################

####################
## Run simulation. Block 11 begins

path = os.path.join(simulation_path, 'results') # Go to results subdirectory for storing all the results
FDTD.Run(path, cleanup=True) # Temporary files are stored and then deleted using cleanup

## Simulation is initiated. Block 11 ends
####################

####################
## Find Zin and |S11|. Block 12 begins

frequency_sweep = np.linspace(centre_frequency-cutoff_frequency,centre_frequency+cutoff_frequency,1001) # Creates a frequency vector for sweep, with points between start, stop , number of points
port_1.CalcPort(path, frequency_sweep) # Time domain voltage and curretn signals get converter to frequency domain using fourier transform
Zin = port_1.uf_tot / port_1.if_tot # uf_tot is totla voltage at port, uf_tot is total current at port
s11 = port_1.uf_ref/port_1.uf_inc # port.uf_ref is reflected wave and port.uf_inc is incident wave
s11_dB = 20.0*np.log10(np.abs(s11)) # s11 in dB
plt.figure() # Creates a figure
plt.plot(frequency_sweep/1e9, s11_dB, color ='Blue') # Plots X vs Y
plt.title('|S11| in dB vs Frequency in GHz') # Title for plot
plt.grid(True) # Display major gridlines
plt.ylabel('s11 (dB)') # Y axis label
plt.xlabel('frequency (GHz)') # X-axis label

#P_in = 0.5*np.real(port_1.uf_tot * np.conj(port_1.if_tot)) # Antenna feed power, this is also called the accepted power. It is not the incident power, incident power is accepted power + reflected power. For a well matched antenna they are about the same at resonant frequency
#print(P_in) # Debug step

plt.figure()
plt.plot(frequency_sweep/1e6, np.real(Zin), 'k-', linewidth=2, label=r'$\Re(Z_{in})$')
plt.plot(frequency_sweep/1e6, np.imag(Zin), 'r--', linewidth=2, label=r'$\Im(Z_{in})$') # This would make the figure have both plots, with x-axis being equal and shared
plt.title('Feed point impedance') 
plt.grid(True)
plt.xlabel('frequency (MHz)')
plt.ylabel('impedance ($\Omega$)')
plt.legend()

## Zin and |S11| are calculated and plotted. Block 12 ends
####################

####################
## Calculate radiated power, directivity, efficiency at centre frequency
## Plot 2D and 3D radiation pattern
## Block 13 begins

centre_index = int(len(frequency_sweep)/2) # Find the centre index = 2.5 GHz
theta = np.arange(0,181,1) # Theta angles in degreees
phi = np.arange(0,361,1) # Phi angle in degrees

nf2ff_res = nf2ff.CalcNF2FF(path, centre_frequency, theta, phi) # Calculates the far field characterisitc from near field data recorded during simulation
#power_radiated = nf2ff_res.Prad # Total power radiated with Phi = 0 after conversion to far field from near field
directivity_maximum = nf2ff_res.Dmax # Finds maximum directivity from the data
directivity_dB = 10*np.log10(directivity_maximum) # Converts directivity into dBi
#efficiency = (power_radiated/P_in[centre_index])*100 # It is how efficient the antenna radiates. Efficiency*Directivity = Gain dBi

### 2D radiation pattern generation, for Phi = 0 plane

E_norm = np.squeeze(nf2ff_res.E_norm)
Efield = E_norm[:,0] # Efield which corresponds to Phi = 0
#print(Efield)
#print("Efield shape:", np.shape(Efield))
Efield_normalized = Efield/np.max(Efield) # Normalizes the data with maximum value
Efield_normalized_dB = 20*np.log10(Efield_normalized) # Converts normalized E -feild data into dB
plt.figure()
ax = plt.subplot(111, polar=True) # First row, column and first figure polar plot attached to object ax
theta_radians = np.radians(theta) # For polar plot theta needs to be in radians, so converts it
ax.plot(theta_radians, Efield_normalized_dB, color ='Blue')
ax.set_theta_zero_location("N") # Set 0 degree to North
ax.set_theta_direction(-1) # Makes increasing angle as clockwise
ax.set_xlabel('Theta sweep') # labels the axis
plt.title("Radiation Pattern (Phi = 0°)") # Title for plot
plt.grid(True) # Displays major gridlines

### 2D radiation pattern generation, for Theta = 0 plane

E_norm = np.squeeze(nf2ff_res.E_norm)
Efield = E_norm[90,:] # Efield which corresponds to Theta = 90
Efield_normalized = Efield/np.max(Efield) # Normalizes the data with maximum value
Efield_normalized_dB = 20*np.log10(Efield_normalized) # Converts normalized E -feild data into dB
plt.figure()
ax = plt.subplot(111, polar=True) # First row, column and first figure polar plot attached to object ax
phi_radians = np.radians(phi) # For polar plot theta needs to be in radians, so converts it
ax.plot(phi_radians, Efield_normalized_dB, color ='Blue')
ax.set_xlabel('Phi sweep') # labels the axis
plt.title("Radiation Pattern (Theta = 90°)") # Title for plot
plt.grid(True) # Displays major gridlines

### 3D radiation pattern generation

E_theta = np.squeeze(nf2ff_res.E_theta) # Removes the frequency from the data
E_phi   = np.squeeze(nf2ff_res.E_phi) # Removes the frequency from the data
theta = nf2ff_res.theta # After the .CalcNF2FF method is applied to nf2ff object, the theta goes from 0 to Pi approximately (3.14). This is becasue rectangular co-ordinates get converted to sphrecial 
#print(theta)
phi = nf2ff_res.phi # After the .CalcNF2FF method is applied to nf2ff object, the phi goes from 0 to 2Pi approximately (6.28). This is becasue rectangular co-ordinates get converted to sphrecial
#print(phi)
heatmap, axes = threeD_heatmap(E_theta, E_phi, theta, phi) # Pass the values in the () to function and take the output of function and store it in heatmap, axes

## Parameters calcuated, plots generated. Block 13 ends
####################

####################
## Prints the calculated value and displays the figures
## Final block, block 14 begins

#print( 'Input power: Pin = {} Watt'.format(P_in[centre_index]))# Prints input power
#print( 'Radiated power: Prad = {} Watt'.format(power_radiated)) # Prints radiated power
print( 'Directivity:    Dmax = {} dBi'.format(directivity_dB)) # Prints the directivity
#print( 'Efficiency:     nu_rad = {} %'.format(efficiency)) # Prints efficiency

plt.show() # Displays all the created figures

## Final block ends.Enjoy!
####################
