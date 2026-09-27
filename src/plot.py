from src.vasp_parser import extract_eigenvals
import matplotlib.pyplot as plt
def plot_energy(eigenval_path, vbm_energy, cbm_energy):
    print(f"VBM set to: {vbm_energy} eV")
    print(f"[PLOT] reading EIGENVAL: {eigenval_path}")
    
    e_up, e_down, occ_up, occ_down = extract_eigenvals(eigenval_path)
    
    e_up_shifted = e_up - vbm_energy
    e_down_shifted = e_down - vbm_energy
    band_gap = cbm_energy - vbm_energy
    
    print(f"[PLOT] detected {len(e_up_shifted)} bands.")
    print(f"[PLOT] calculated band gap: {band_gap:.4f} eV")

    #plotting
    plt.figure(figsize=(6, 8))
    
    plt.fill_between([0, 1], -5, 0, color='cyan', alpha=0.1)
    plt.fill_between([0, 1], band_gap, band_gap + 5, color='gray', alpha=0.1)
    
    plt.axhline(0, color='black', linestyle='--', linewidth=1, label='VBM (0 eV)')
    plt.axhline(band_gap, color='black', linestyle='--', linewidth=1, label=f'CBM ({band_gap:.2f} eV)')
    
    plt.hlines(e_up_shifted, 0.1, 0.4, colors='blue', linewidth=1.5, alpha=0.5)
    plt.hlines(e_down_shifted, 0.6, 0.9, colors='red', linewidth=1.5, alpha=0.5)
    
    occupied_up = e_up_shifted[occ_up > 0.5]
    occupied_down = e_down_shifted[occ_down > 0.5]
    
    plt.scatter([0.25]*len(occupied_up), occupied_up, color='blue', s=40, zorder=3, label='Occupied (up)')
    plt.scatter([0.75]*len(occupied_down), occupied_down, color='red', s=40, zorder=3, label='Occupied (down)')

    plt.ylabel("Energy (eV)", fontsize=12)
    plt.xticks([0.25, 0.75], ['Spin Up', 'Spin Down'], fontsize=12)
    plt.xlim(0, 1)
    
    plt.ylim(-1, band_gap + 1) 
    
    #plt.legend(loc='upper right')
    plt.tight_layout()
    output_filename = "defect_levels.pdf"
    plt.savefig(output_filename, format="pdf", bbox_inches="tight")
    print(f"[PLOT] PDF created: {output_filename}")

    plt.show()