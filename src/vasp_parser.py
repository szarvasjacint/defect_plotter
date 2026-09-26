def extract_tot_energy(path):
    last_energy = None
    with open(path, "r") as file:
        for line in file:
            if "TOTEN" in line:
                parts = line.split()
                last_energy = float(parts[4])
    return(last_energy)