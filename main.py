import argparse
import sys
from src.vasp_parser import extract_tot_energy
from src.plot import plot_energy, plot_dos, plot_bandstructure

def main():
    parser = argparse.ArgumentParser(description="VASP Defect Energy Plotter")
    
    subparsers = parser.add_subparsers(dest="command", help="Functions")
    
    # 1. TOTEN
    parser_energy = subparsers.add_parser("energy", help="TOTEN from OUTCAR")
    parser_energy.add_argument("--TOTEN", required=True, help="OUTCAR file path")
    
    # 2. Plotting
    parser_plot = subparsers.add_parser("plot", help="Energy level plotting")
    parser_plot.add_argument("--vbm", type=float, required=True, help="Energy of VBM (eV)")
    parser_plot.add_argument("--cbm", type=float, required=True, help="Energy of CBM (eV)")
    parser_plot.add_argument("--EIGENVAL", required=True, help="EIGENVAL file path")

    #3. Dos plotting
    parser_dos = subparsers.add_parser("dos", help="Density of States plotting")
    parser_dos.add_argument("--files", nargs='+', required=True, help="List of DOSCAR or VASPKIT .dat files")
    parser_dos.add_argument("--labels", nargs='+', help="Labels for the legend (e.g. Total Si C)")
    parser_dos.add_argument("--vbm", type=float, required=True, help="Energy of VBM (eV) for shifting")
    parser_dos.add_argument("--bandgap", type=float, required=True, help="Band gap energy in eV")

    #4. BS
    parser_band = subparsers.add_parser("band", help="Band structure plotting")
    parser_band.add_argument("--band", required=True, help="REFORMATTED_BAND.dat file path")
    parser_band.add_argument("--klabels", required=True, help="KLABELS file path")
    parser_band.add_argument("--vbm", type=float, required=True, help="Energy of VBM (eV) for shifting")

    if len(sys.argv) == 1:
        print("="*50)
        print("   VASP Defect Analyzer")
        print("="*50)
        print("Choose a function to run:\n")
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    if args.command == "energy":
        total_energy = extract_tot_energy(args.TOTEN)
        print(f"[RESULT] Total energy: {total_energy} eV\n")
        
    elif args.command == "plot":
        print(f"[PLOT] Starting plotting...")
        plot_energy(args.EIGENVAL, args.vbm, args.cbm)

    elif args.command == "dos":
        print(f"[DOS] Starting DOS plotting...")
        plot_dos(args.files, args.vbm, args.bandgap, args.labels)

    elif args.command == "band":
        print(f"[BAND] Starting band structure plotting...")
        plot_bandstructure(args.band, args.klabels, args.vbm)

if __name__ == "__main__":
    main()