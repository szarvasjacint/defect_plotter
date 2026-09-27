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
    with open(path, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) == 5 and parts[0].isdigit():
                e_up.append(float(parts[1]))
                e_down.append(float(parts[2]))
    return np.array(e_up), np.array(e_down)
                            