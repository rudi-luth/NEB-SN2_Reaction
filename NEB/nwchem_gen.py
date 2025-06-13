#!/usr/bin/env python3

# Script to generate neb calculations using nwchem
# coded by rudi
# 13-Jun 2025

import numpy as np
import argparse

# read xyz file
def read_xyz(fname):
    atoms = []
    coords = []

    with open(fname, 'r') as file:
        # Read the first line (number of atoms)
        fline = int(file.readline().strip())
        
        # Read the second line (blank or comment)
        sline = file.readline().strip()
        
        # Read the atom data
        for _ in range(num_atoms):
            line = file.readline().strip().split()
            element = line[0]  # Element symbol (e.g., 'O', 'H')
            x, y, z = map(float, line[1:])  # Coordinates in 3D space
            
            atoms.append(element)
            coords.append([x, y, z])

    return atoms, np.array(coords)

# generate nwchem script
def nwchem_gen(ifiles, ofile):

    geometry_tags = [" ", "endgeom"]

    with open(ofile, 'w') as file:
        file.write('# nwchem input script\n# made by Rudi\n#\n\n')
        file.write('# Init assegment\nstart SN2_path\n')
        # file.write('# Memory allocation (adjust as needed)\nmemory total 1 gb\n\n') If you need you can use it
        file.write(f'# XYZ coordinates in Angstrom units\n')
        
        # Write XYZ blocks with specific geometry tags
        for idx, (input_file, tag) in enumerate(zip(ifiles, geometry_tags), start=1):
            # Read data from each input file
            atoms, coords = read_xyz(ifile)

            # Write geometry block with the specific tag
            file.write(f'geometry {tag} nocenter noautosym noautoz \n')
            file.write(f'# Input File {idx}: {ifile}\n')
            
            # Write the atom and coordinate data
            for atom, coord in zip(atoms, coords):
                file.write(f'  {atom:<2}  {coord[0]:.6f}  {coord[1]:.6f}  {coord[2]:.6f}\n')
            file.write('end\n\n')  # Close the geometry block

        file.write('# Specify the basis set\nbasis\n  * library 3-21G\nend\n\n')
        file.write('# Set up DFT options\ndft\n  xc b3lyp\n  maxiter 5001\n  cgmin\n  mult 1\nend\n\n')    # change the mult for spin multiplicity
        file.write('# Set up NEB options\nneb\n  nbeads 10\n  kbeads 1.0\n  maxiter 10\n  stepsize 0.10\n  print_shift 1\nend\nn')
        file.write('task dft neb ignore\n\n')
        file.write('# NEB options for increase the number of images \nneb\n  nbeads 20\n  kbeads 1.0\n  maxiter 30\n  stepsize 1.0\n  loose\nend\nn')
        file.write('task dft neb ignore')
