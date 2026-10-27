import numpy as np

def extract_tot_energy(path):
    last_energy = None
    with open(path, "r") as file:
        for line in file:
            if "TOTEN" in line:
                parts = line.split()
                last_energy = float(parts[4])
    return(last_energy)

def extract_eigenvals(path):
    e_up = []
    e_down = []
    occ_up, occ_down = [], []
    with open(path, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) == 5 and parts[0].isdigit():
                e_up.append(float(parts[1]))
                e_down.append(float(parts[2]))
                occ_up.append(float(parts[3]))
                occ_down.append(float(parts[4]))
    return np.array(e_up), np.array(e_down), np.array(occ_up), np.array(occ_down)

def extract_dos(path):
    energies, dos_up, dos_down = [], [], []

    with open(path, "r") as file:
        lines = file.readlines()

    #VASPKIT
    if lines[0].startswith("#") or "Energy" in lines[0]:
        for line in lines:
            if line.startswith("#"):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                energies.append(float(parts[0]))
                dos_up.append(float(parts[1]))
                dos_down.append(0.0)

    #original VASP
    else:
        header_line = lines[5].split()
        nedos = int(header_line[2])
        
        for i in range(6, 6 + nedos):
            parts = lines[i].split()
            energies.append(float(parts[0]))
            
            if len(parts) == 5:
                dos_up.append(float(parts[1]))
                dos_down.append(float(parts[2]))
            elif len(parts) == 3:
                dos_up.append(float(parts[1]))
                dos_down.append(0.0)

    return np.array(energies), np.array(dos_up), np.array(dos_down)