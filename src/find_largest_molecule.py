import os

# Atomic numbers dictionary
ATOMIC_NUMBERS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18,
    'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
    'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36,
    # Add more if needed based on the dataset, but these are common
}

def count_electrons(file_path):
    electrons = 0
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) < 3:
                return 0
            
            # Skip first two lines (atom count and comment)
            for line in lines[2:]:
                parts = line.split()
                if not parts:
                    continue
                symbol = parts[0].capitalize()
                electrons += ATOMIC_NUMBERS.get(symbol, 0)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return electrons

def find_largest(directory):
    max_electrons = -1
    largest_molecule = ""
    atom_count = 0
    
    files = [f for f in os.listdir(directory) if f.endswith('.xyz')]
    
    for filename in files:
        path = os.path.join(directory, filename)
        current_electrons = count_electrons(path)
        
        if current_electrons > max_electrons:
            max_electrons = current_electrons
            largest_molecule = filename
            # Get atom count for time estimation
            with open(path, 'r') as f:
                try:
                    atom_count = int(f.readline().strip())
                except:
                    atom_count = 0
                    
    return largest_molecule, max_electrons, atom_count

if __name__ == "__main__":
    dir_path = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries"
    molecule, electrons, atoms = find_largest(dir_path)
    print(f"Largest molecule: {molecule}")
    print(f"Number of electrons: {electrons}")
    print(f"Number of atoms: {atoms}")
