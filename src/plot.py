from src.vasp_parser import extract_eigenvals
import matplotlib.pyplot as plt
def plot_energy(eigenval_path, vbm_energy):
    print(f"VBM set to: {vbm_energy} eV")
    print(f"[PLOT] reading EIGENVAL: {eigenval_path}")
    
    e_up, e_down = extract_eigenvals(eigenval_path)
    
    e_up_shifted = e_up - vbm_energy
    e_down_shifted = e_down - vbm_energy
    
    print(f"[PLOT] detected {len(e_up_shifted)} bands.")
    #plotting
    print("[PLOT] generating figure...")
    plt.figure(figsize=(6, 8))
    
    plt.hlines(e_up_shifted, 0.1, 0.4, colors='blue', linewidth=1.5)
    
    plt.hlines(e_down_shifted, 0.6, 0.9, colors='red', linewidth=1.5)
    
    plt.axhline(0, color='black', linestyle='--', linewidth=1.5, label='VBM (0 eV)')
    
    plt.ylabel("Energy (eV)", fontsize=12)
    plt.title("Energy levels", fontsize=14)
    
    plt.xticks([0.25, 0.75], ['Spin Fel', 'Spin Le'], fontsize=12)
    plt.xlim(0, 1)
    
    plt.ylim(-1, 4) 
    
    plt.legend()
    plt.tight_layout()
    plt.show()