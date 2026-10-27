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
        lines = [line.strip() for line in file if line.strip()]

    #VASPKIT
    if lines[0].startswith("#") or "Energy" in lines[0]:
        for line in lines:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            
            try:
                energy_val = float(parts[0])
                dos_val = float(parts[-1])
            except ValueError:
                continue
                
            energies.append(energy_val)
            dos_up.append(dos_val)
            dos_down.append(0.0)

    #VASP
    else:
        header_line = lines[5].split()
        nedos = int(header_line[2])
        
        for i in range(6, 6 + nedos):
            if i >= len(lines):
                break
            parts = lines[i].split()
            if len(parts) < 3:
                continue
            
            try:
                energy_val = float(parts[0])
                dos_up_val = float(parts[1])
                dos_down_val = float(parts[2]) if len(parts) >= 5 else 0.0
            except ValueError:
                continue
                
            energies.append(energy_val)
            dos_up.append(dos_up_val)
            dos_down.append(dos_down_val)

    return np.array(energies), np.array(dos_up), np.array(dos_down)


def extract_bandstructure(band_path, klabels_path):
    #KLABELS
    k_coords = []
    k_labels = []
    with open(klabels_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    coord = float(parts[1])
                    label = parts[0]
                    if label == "GAMMA":
                        label = r"$\Gamma$"
                    k_labels.append(label)
                    k_coords.append(coord)
                except ValueError:
                    continue
                    
    #REFORMATTED_BAND
    k_path = []
    bands = []
    with open(band_path, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) > 1:
                k_path.append(float(parts[0]))
                bands.append([float(x) for x in parts[1:]])
                
    return np.array(k_path), np.array(bands), k_coords, k_labels