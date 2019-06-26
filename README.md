Kuo-Lin-Dynamical-Diffrration (KLDD) is a GUI program that simulates the x-ray standing wave effects of a single crystal based on dynamical x-ray diffraction. The program can carry out the simulations of the standing wave phase, reflectivity and photoemission rocking curves. The authors are Cheng-Tai Kuo, Shih-Chieh Lin, and Charles S. Fadley.

Inputs:
This program needs two types of input to implement the simulation:
1.	Material Information: This file includes the lattice constant of the desired material, the atomic scattering factor and atomic position of each element. This information needs to be placed in a specific ordered. Please find the sample file 'material_info.txt' for more details.
2.	Simulation parameters: Type in the simulation parameters in the user interface. Note that all of the parameters, such as the Bragg reflection, photon energy, simulation angle/energy range, polar angle, take-off angle, and Gaussian broadening factor, are mandatory to be filled to carry out the simulations.
Note that the above two kinds of input need to be entered correctly to produce simulation. Fail to do so will lead to an error message.

Features:
1.	Simulate reflectivity, phase, and photoemission rocking curve 
2.	Save and export the simulation data
3.	Load experimental reflectivity and rocking curves for comparison and analysis
4.	Support the background subtraction or angle calibration on the experimental data
5.	Built-in toolbar, which is above the simulation window, allow adjusting the layout and/or saving the figures 
6.	Enable adjustment on the initial phase of the photoemission rocking curve

Author contributions:
Dr. Cheng-Tai Kuo has developed the dynamical diffraction theory on single crystals and implemented the scientific simulation codes which are used as backend of this program. Mr. Shih-Chieh Lin has implemented the graphic user interface and integrated it with backend. Prof. Charles S. Fadley is the principal investigator of this project.
