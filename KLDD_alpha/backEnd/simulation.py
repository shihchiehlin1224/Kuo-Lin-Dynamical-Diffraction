import numpy as np
import matplotlib.pyplot as plt
def StructureFactor(h1, k1, l1, hv, Material_inf, ASF_atoms):
    H = np.array([h1, k1, l1])
    # read in the coordinates of each atom
    coordinates = Material_inf[3]
    FAtoms = {}
    FH_Atoms = 0
    FH_sum = 0
    
    # iterate through all elements, key is the chemical formula of element
    for key, value in ASF_atoms.items():
        ASF_temp = np.loadtxt(value, skiprows = 1, unpack = True)
        real = np.interp(hv, ASF_temp[0], ASF_temp[1])
        imag = np.interp(hv, ASF_temp[0], ASF_temp[2])
        FAtoms[key] = real + imag* 1j
        for j in range(len(coordinates[key])):
            FH_cur = FAtoms[key]* np.exp(2* np.pi* 1j* np.dot(H, coordinates[key][j]))
            FH_Atoms += FH_cur
        FH_sum += FH_Atoms
        FH_Atoms = 0
    return 2*FH_sum


def Yield(Element, aphase, IMFP, theta_to, theta_p0, No_uc, x_lower, x_step, x_upper, h1, k1, l1,
             hv, sigma, DWF, Material_inf, ASF_atoms, mode = "Angular"):
   
    Aphase = aphase* np.pi
    H = np.array([h1, k1, l1])
    ThetaB = Material_inf[2]
    # all x_axis, phase and Ref are real 1D array
    x_axis, Phase, Ref = Reflectivity(x_lower, x_step, x_upper, h1, k1, l1, hv, sigma,
                                      DWF, Material_inf, ASF_atoms, mode);
    if(mode == "Angular"):
        Angle_e = (x_axis + theta_to)
        theta_pH = 2* x_axis + theta_to - 90;
    elif(mode == "Photonic"):
        Angle_e = ThetaB + theta_to
        theta_pH = 2* ThetaB + theta_to - 90;
    else:
        return ;

    S_I_AI = np.cos(2*ThetaB)
    Lamda_e = IMFP* np.sin(np.radians(Angle_e))
    
    # read in material information
    coordinates = Material_inf[3][Element]
    lattice = Material_inf[0]
    m1 = len(coordinates)
    
    # initialize the size of variable used later
    Coh_Pos_Element = np.zeros(m1)
    Yield_A = np.zeros([len(Ref) ,m1* No_uc])
    I_Element = np.zeros([len(Ref) ,m1* No_uc])
    RC_Element = np.zeros(len(Ref))
    I_nor_Element = np.zeros(len(Ref))
    
    for i in range(0, m1):
        Coh_Pos_Element[i] = np.dot(H, coordinates[i])%1
        for k in range(0, No_uc):
            Coh_Fra_Element = 1
            Yield_A[:,i + k*m1] = (np.exp(-lattice[2]* (k + 1 - coordinates[i][2])/ Lamda_e)*
            (1 + Ref + 2* S_I_AI* np.sqrt(Ref)* Coh_Fra_Element* np.cos(Phase* np.pi - 2* np.pi* Coh_Pos_Element[i] + np.pi*Aphase)))
            I_Element[:,i + k*m1] = np.exp(-lattice[2]* (k + 1 - coordinates[i][2])/ Lamda_e)

    RC_Element = Yield_A.sum(axis=1)
    I_nor_Element = I_Element.sum(axis=1) 
    return x_axis, RC_Element, I_nor_Element

# the default mode is angular

def Reflectivity(x_lower, x_step, x_upper, h1, k1, l1, hv, sigma, DWF, Material_inf, ASF_atoms, mode = "Angular"):
   
    ThetaB = Material_inf[2]
    dhkl = Material_inf[1]
    Vol = Material_inf[0][3]
    
    x_axis = np.arange(x_lower, x_upper + x_step, x_step)
    # claim the x_axis_real, Yeta, RC, Phase are 1D numpy array has the same size as x_axis 
    #x_axis_real = Yeta = zeros(len(x_axis))
    Rc = np.zeros(len(x_axis), dtype = complex)
    Phase = np.zeros(len(x_axis))
    
    FH = StructureFactor(h1, k1, l1, hv, Material_inf, ASF_atoms)
    FHB = StructureFactor(-h1, -k1, -l1, hv, Material_inf , ASF_atoms)
    F0 = StructureFactor(0, 0, 0, hv, Material_inf, ASF_atoms);
    
    G = 2.818* 10**(-5)* (12400/hv)**2 /(np.pi* Vol);
    
    # Calculations for different modes, return null while mode is not choosen properly
    if(mode == "Angular"):
        x_axis_real = x_axis + np.degrees(ThetaB)
        Yeta = (- np.radians(x_axis)* np.sin(2*ThetaB) + G*F0)/(G* np.sqrt(FH* FHB))
    elif(mode == "Photonic"):
        x_axis_real = x_axis + 12400/(2* dhkl* np.sin(ThetaB))
        Yeta=  (-2* x_axis* (np.sin(ThetaB))**2 /hv + G*F0)/(G* np.sqrt(FH* FHB));
    else:
        return ;
    
    for i in range(len(Yeta)):        
        if (np.real(Yeta[i]) < 0):
            Rc[i] = (Yeta[i] + np.sqrt(Yeta[i]**2 -1))**2 *(FH/FHB)
        else: 
            Rc[i] = (Yeta[i] - np.sqrt(Yeta[i]**2 -1))**2 *(FH/FHB)

    Ref_ideal = np.absolute(Rc)
    
    Rc_mag = np.absolute(np.sqrt(Rc/Ref_ideal))
    Rc_theta = np.angle(np.sqrt(Rc/Ref_ideal))
    
    max_index = (np.where(Rc_theta == Rc_theta.max())[0])
    for i in range(len(Rc)):
        if i < max_index:
            Phase[i] = (Rc_theta[i] + np.pi)/np.pi
        else:
            Phase[i] = (Rc_theta[i])/np.pi 
    
    Phase = Phase #- Phase.min();
    
    
    if(sigma == 0):
        Gaussian_i = 1
        Gaussian = 1
    else:
        sigma_square = sigma**2
        n_Ref = (np.where(Ref_ideal == Ref_ideal.max())[0])
        Gaussian_i = (1/(np.sqrt(2* np.pi* sigma_square)))* np.exp(-(x_axis - x_axis[n_Ref])**2/ (2*(sigma_square)))
        Gaussian = Gaussian_i/Gaussian_i.max()
        # Gaussian = 1 
                     
    Ref = Gaussian* Ref_ideal* np.exp(-DWF); 
    return x_axis_real, Phase, Ref
