# Kuo-Lin-Dynamic-Diffraction
The is a GUI program to simulate the phase, reflectivity and photoemission rocking curves of single crystal.
Authors: Cheng-Tai Kuo, Shih-Chieh Lin, Charles S. Fadley

Inputs:

This program needs two types of input to implement the simulation:
1. Material Information
This file includes the lattice constant, atomic scattering factors and atomic position of each element.
This information needs to be placed in a specific ordered. Please find the sample file 'material_info.txt' for more details.
2. Simulation parameter
Type in the simulation parameters in the user interface.
Noted that all of the Bragg reflection, photon energy, simulation range, polar angle, take-off angle, and Gaussian broaden needed to be filled to produce simulation.

Noted that the above two kinds of input need to be entered correctly to produce simulation. Fail to do so will lead to an error message.

Features:
1. Simulate reflectivity, phase, and rocking curve 
2. Loading experimental reflectivity and rocking curves for comparison
3. One could adjust the layout or save the figures by using the toolbar above the simulation window.  
4. Save the simulation data 
5. Support the background subtraction or angle calibration on the experimental data
6. Enable adjustment on the initial phase of the rocking curve 


Authors' contribution:

Dr. Cheng-tai Kuo has develped dynamic diffraction theory on single crystal and implement the scientific simulation code which is used as backend of this program.
Shih-Chieh Lin has implemented the graphic user interface and integrated it with backend.
Prof. Chuck Fadley is the principal investigator of this project.
