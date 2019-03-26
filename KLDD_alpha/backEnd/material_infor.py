import csv
import numpy as np
# Bi2Se3_material_info.txt

def create_coordinate(par_dat, start, end):
    coordinate = []
    for i in range(start, end):
        one_atom = []
        for pos in range(1, len(par_dat[i])):
            one_atom = np.append(one_atom, float(par_dat[i][pos]))
        coordinate.append(one_atom)
    coordinate = np.array(coordinate)
    return coordinate


def crystal_infor(filename):      
    input_file = open(filename, "r")
    par_dat = list(csv.reader(input_file, delimiter='\t'))
    ASF_atoms = {}
    coordinates = {}
    atom_name_list = []
    atom_start = -1
    for i, line in enumerate(par_dat):
        if(line[0] == 'a'):
            a = float(line[1])
        elif(line[0] == 'b'):
            b = float(line[1])
        elif(line[0] == 'c'):
            c = float(line[1])
        if(line[0].upper() == "ATOM"):
            ASF_atoms[line[1]] = line[2]
            atom_name_list.append(line[1])
            atom_start = i + 1
            atom_end = atom_start
            while(atom_end < len(par_dat) and par_dat[atom_end][0].upper() != "ATOM" and par_dat[atom_end][1] !=''):
                atom_end += 1
            coordinates[line[1]] = create_coordinate(par_dat, atom_start, atom_end)
            i = atom_end - 1

    Vol = a*b*c*np.sin(2*np.pi/3)
    lattice = [a, b, c, Vol]
    return atom_name_list, ASF_atoms, lattice, coordinates

