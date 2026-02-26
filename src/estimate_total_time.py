import os

# Atomic numbers dictionary
ATOMIC_NUMBERS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18,
    'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
    'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36,
}

def get_molecule_stats(file_path):
    electrons = 0
    atoms = 0
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if not lines:
                return 0, 0
            atoms = int(lines[0].strip())
            for line in lines[2:]:
                parts = line.split()
                if not parts:
                    continue
                symbol = parts[0].capitalize()
                electrons += ATOMIC_NUMBERS.get(symbol, 0)
    except Exception as e:
        pass
    return electrons, atoms

def analyze_all(directory):
    total_electrons = 0
    total_atoms = 0
    molecule_data = []
    
    files = [f for f in os.listdir(directory) if f.endswith('.xyz')]
    
    for filename in files:
        path = os.path.join(directory, filename)
        e, a = get_molecule_stats(path)
        total_electrons += e
        total_atoms += a
        molecule_data.append({'e': e, 'a': a})
        
    return total_electrons, total_atoms, len(files), molecule_data

if __name__ == "__main__":
    dir_path = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries"
    t_e, t_a, count, data = analyze_all(dir_path)
    
    print(f"Total molecules: {count}")
    print(f"Total electrons across all: {t_e}")
    print(f"Total atoms across all: {t_a}")
    
    # Estimate complexity
    # Complexity of DFT roughly scales as O(N^3) where N proportional to electrons
    # We'll use a relative scale based on the largest molecule found previously (222 electrons -> ~10 hours)
    # Largest molecule complexity = 222^3
    largest_e = 222
    ref_time_hours = 10 
    
    total_estimated_hours = 0
    for mol in data:
        # Scale time: (current_e / largest_e)^3 * ref_time
        if mol['e'] > 0:
            rel_complexity = (mol['e'] / largest_e)**3
            total_estimated_hours += rel_complexity * ref_time_hours
            
    print(f"Total Estimated Computing Time: {total_estimated_hours:.2f} hours")
    print(f"In days: {total_estimated_hours/24:.2f} days")
