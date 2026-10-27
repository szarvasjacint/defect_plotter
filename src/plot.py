from src.vasp_parser import extract_eigenvals, extract_dos, extract_bandstructure
import matplotlib.pyplot as plt
import numpy as np
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
    
    plt.tight_layout()
    pdf_filename = "defect_levels.pdf"
    png_filename = "defect_levels.png"
    
    plt.savefig(pdf_filename, format="pdf", bbox_inches="tight")
    
    plt.savefig(png_filename, format="png", dpi=300, bbox_inches="tight")
    print(f"[PLOT] PDF and PNG created")

    plt.show()


def plot_dos(dos_files, vbm_energy, bandgap, labels=None):
    print(f"[DOS] VBM set to: {vbm_energy} eV | Band gap: {bandgap} eV")
    
    plt.figure(figsize=(10, 6))
    colors = ['#7f7f7f', '#0026ca', '#d60000', '#2ca02c', '#9467bd']
    
    for i, file_path in enumerate(dos_files):
        print(f"[DOS] reading file: {file_path}")
        energies, dos_up, dos_down = extract_dos(file_path)
        energies_shifted = energies - vbm_energy
        
        label = labels[i] if (labels and i < len(labels)) else file_path.split('/')[-1]
        color = colors[i % len(colors)]
        
        plt.plot(energies_shifted, dos_up, color=color, linewidth=1.8, label=label)
        if i == 0:
            plt.fill_between(energies_shifted, 0, dos_up, color='#e5e5e5', alpha=0.7, zorder=1)
            
        if np.any(dos_down != 0):
            plt.plot(energies_shifted, dos_down, color=color, linewidth=1.8)
            if i == 0:
                plt.fill_between(energies_shifted, 0, dos_down, color='#e5e5e5', alpha=0.7, zorder=1)
                
    plt.axvspan(0, bandgap, color='#e2f0d9', alpha=0.6, zorder=0, label='Band Gap')
    
    plt.axvline(0, color='black', linestyle='--', linewidth=1.0, zorder=2)
    plt.axvline(bandgap, color='black', linestyle='--', linewidth=1.0, zorder=2)
    
    #plt.title("2D SiC - Density of States", fontsize=14, fontweight='normal', pad=12)
    plt.xlabel("Energy [eV]", fontsize=12)
    plt.ylabel("DOS", fontsize=12)
    
    plt.xlim(-4, 6)
    plt.ylim(0, 4.0)
    
    plt.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()
    
    pdf_filename = "pdos_plot.pdf"
    png_filename = "pdos_plot.png"
    plt.savefig(pdf_filename, format="pdf", bbox_inches="tight")
    plt.savefig(png_filename, format="png", dpi=300, bbox_inches="tight")
    
    print(f"[DOS] Saved files: {pdf_filename} and {png_filename}")
    plt.show()


def plot_bandstructure(band_file, klabels_file, vbm_energy):
    print(f"[BAND] VBM set to: {vbm_energy} eV")
    print(f"[BAND] Reading files: {band_file} and {klabels_file}")
    
    k_path, bands, k_coords, k_labels = extract_bandstructure(band_file, klabels_file)
    
    bands_shifted = bands - vbm_energy
    
    # MÓDOSÍTÁS: Szélesebb képarány (pl. 10x6 vagy 8x6)
    plt.figure(figsize=(8, 6)) 
    
    for i in range(bands_shifted.shape[1]):
        plt.plot(k_path, bands_shifted[:, i], color='#0026ca', linewidth=1.5, zorder=1)
        
    plt.axhline(0, color='black', linestyle='--', linewidth=1.5, zorder=2)
    
    for coord in k_coords:
        plt.axvline(coord, color='black', linestyle='-', linewidth=0.8, alpha=0.5, zorder=0)
        
    plt.xticks(k_coords, k_labels, fontsize=14)
    plt.xlim(k_coords[0], k_coords[-1])
    
    plt.ylim(-5, 5)
    
    plt.ylabel("Energy [eV]", fontsize=14)
    
    plt.tight_layout()
    
    pdf_filename = "bandstructure_plot.pdf"
    png_filename = "bandstructure_plot.png"
    plt.savefig(pdf_filename, format="pdf", bbox_inches="tight")
    plt.savefig(png_filename, format="png", dpi=300, bbox_inches="tight")
    
    print(f"[BAND] Saved files: {pdf_filename} and {png_filename}")
    plt.show()