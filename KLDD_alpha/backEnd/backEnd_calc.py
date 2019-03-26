from backEnd.simulation import StructureFactor, Reflectivity, Yield
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def n_smoothing(x, N):
	return np.convolve(x, np.ones(N)/N, mode = "same")

def slop_adjust(exp_data, tilt):
	pre_max = exp_data.max()
	max_index = (np.where(exp_data == pre_max)[0])
	cal_data = exp_data + (np.linspace(0, tilt, len(exp_data)))* exp_data.max()
	cal_data = cal_data/ cal_data[max_index]* pre_max
	return cal_data

def process(data, adjustment):
	new_data = np.copy(data)
	new_data[0] = data[0] + adjustment[2]
	for i in range(1, len(data)):
		if(adjustment[1] != 0):
			new_data[i] = slop_adjust(data[i], adjustment[1])
		new_data[i] = n_smoothing(new_data[i], adjustment[0])
	return new_data

def cal_layer_distance(h, k, l, lattice):
	dhkl = np.sqrt(1/(4/3*(((h)**2 + h*k + k**2)/(lattice[0]**2)) + (l**2)/(lattice[2]**2)))
	return dhkl

def calc_ref_phase(Brag_reflection, hv, ref_range, Gaussian_boarden, material_infor, ASF_atoms, mode = "Angular"):
	h = Brag_reflection[0]
	k = Brag_reflection[1]
	l = Brag_reflection[2]
	
	range_start = ref_range[0]  
	step_size = ref_range[1] 
	range_end = ref_range[2]

	DWF = Gaussian_boarden[0]
	sigma = Gaussian_boarden[1]
	# update material_infor
	lattice = material_infor[0]
	dhkl = cal_layer_distance(h, k, l, lattice)
	ThetaB = np.arcsin(12400/(hv*2*dhkl))

	material_infor[1] = dhkl
	material_infor[2] = ThetaB
	ref_x_axis, Phase, Ref = Reflectivity(range_start, step_size, range_end, h, k, l, hv, sigma, DWF, material_infor, ASF_atoms, mode = "Angular")
	return ref_x_axis, Phase, Ref

def calc_RCs(Element, aphase, IMFP, angles, No_uc, Brag_reflection, hv, ref_range, Gaussian_boarden, material_infor, ASF_atoms, mode = "Angular"):
	h = Brag_reflection[0]
	k = Brag_reflection[1]
	l = Brag_reflection[2]
	range_start = ref_range[0]  
	step_size = ref_range[1] 
	range_end = ref_range[2]
	DWF = Gaussian_boarden[0]
	sigma = Gaussian_boarden[1]
	# update material_infor
	lattice = material_infor[0]
	dhkl = cal_layer_distance(h, k, l, lattice)
	ThetaB = np.arcsin(12400/(hv*2*dhkl))
	material_infor[1] = dhkl
	material_infor[2] = ThetaB
	theta_p0 = angles[0]
	theta_to = angles[1]
	x_axis, RC_Element, I_nor_Element = Yield(Element, aphase, IMFP, theta_to, theta_p0, No_uc, range_start, step_size, range_end, h, k, l,
             hv, sigma, DWF, material_infor, ASF_atoms, mode = "Angular")
	return x_axis, RC_Element, I_nor_Element

