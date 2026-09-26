import argparse
import sys
from src.vasp_parser import extract_tot_energy

def main():
    parser = argparse.ArgumentParser(description="VASP Defect Energy Plotter")
    
    subparsers = parser.add_subparsers(dest="command", help="Functions")
    
    # 1. TOTEN
    parser_energy = subparsers.add_parser("energy", help="TOTEN from OUTCAR")
    parser_energy.add_argument("--TOTEN", required=True, help="OUTCAR file path")
    
    # 2. Plotting
    parser_plot = subparsers.add_parser("plot", help="Energy level plotting")
    parser_plot.add_argument("--vbm", type=float, required=True, help="Energy of VBM (eV)")

    # Ha nincs megadva parancs, kiírjuk a súgót
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
        print(f"[PLOT] VBM set to: {args.vbm} eV\n")

if __name__ == "__main__":
    main()