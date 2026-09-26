import argparse
import sys
from src.vasp_parser import extract_tot_energy

def main():
    parser = argparse.ArgumentParser(
        description="VASP Defect Energy Plotter"
    )
    parser.add_argument("--TOTEN", required=True, help="OUTCAR file path")

    if len(sys.argv) == 1:
        print("="*50)
        print("   VASP Defect Energy Analyzer v1.0")
        print("="*50)
        print("A futtatáshoz meg kell adnod a paramétereket. Íme a használati útmutató:")
        parser.print_help()
        sys.exit(1)


    args = parser.parse_args()
    
    total_energy = extract_tot_energy(args.TOTEN)
    print(f"[RESULT] Total energy: {total_energy} eV\n")

if __name__ == "__main__":
    main()