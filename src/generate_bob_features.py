import os
import glob
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement

# Propiedades atómicas
ATOMIC_PROPS = {
    'H':  {'Z': 1,  've': 1},
    'Li': {'Z': 3,  've': 1},
    'Be': {'Z': 4,  've': 2},
    'B':  {'Z': 5,  've': 3},
    'C':  {'Z': 6,  've': 4},
    'N':  {'Z': 7,  've': 5},
    'O':  {'Z': 8,  've': 6},
    'F':  {'Z': 9,  've': 7},
    'Na': {'Z': 11, 've': 1},
    'Mg': {'Z': 12, 've': 2},
    'Al': {'Z': 13, 've': 3},
    'Si': {'Z': 14, 've': 4},
    'P':  {'Z': 15, 've': 5},
    'S':  {'Z': 16, 've': 6},
    'Cl': {'Z': 17, 've': 7},
    'K':  {'Z': 19, 've': 1},
    'Ca': {'Z': 20, 've': 2},
    'Ga': {'Z': 31, 've': 3},
    'Ge': {'Z': 32, 've': 4},
    'As': {'Z': 33, 've': 5},
    'Se': {'Z': 34, 've': 6},
    'Br': {'Z': 35, 've': 7},
    'I':  {'Z': 53, 've': 7}
}

MAX_ATOMS = 56

def parse_xyz(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    num_atoms = int(lines[0].strip())
    molecule_name = lines[1].strip()
    
    atoms = []
    coords = []
    
    for line in lines[2:2+num_atoms]:
        parts = line.strip().split()
        if not parts:
            continue
        atom = parts[0]
        atom_symbol = ''.join([c for c in atom if c.isalpha()])
        if atom_symbol not in ATOMIC_PROPS:
            atom_symbol = atom_symbol.capitalize()
        x, y, z = map(float, parts[1:4])
        atoms.append(atom_symbol)
        coords.append([x, y, z])
        
    return molecule_name, atoms, np.array(coords)

def analyze_dataset(files):
    unique_atoms = set()
    max_atoms_count = {}
    max_pairs_count = {}
    
    for f in files:
        _, atoms, _ = parse_xyz(f)
        unique_atoms.update(atoms)
        
    unique_atoms = sorted(list(unique_atoms))
    
    for atom in unique_atoms:
        max_atoms_count[atom] = 0
        
    all_pairs = list(combinations_with_replacement(unique_atoms, 2))
    for tuple_pair in all_pairs:
        max_pairs_count[tuple_pair] = 0
        
    for f in files:
        _, atoms, _ = parse_xyz(f)
        N = len(atoms)
        
        atom_counts = {a: 0 for a in unique_atoms}
        for a in atoms:
            atom_counts[a] += 1
            
        for a in unique_atoms:
            if atom_counts[a] > max_atoms_count[a]:
                max_atoms_count[a] = atom_counts[a]
                
        for pair in all_pairs:
            a1, a2 = pair
            if a1 == a2:
                count = (atom_counts[a1] * (atom_counts[a1] - 1)) // 2
            else:
                count = atom_counts[a1] * atom_counts[a2]
            if count > max_pairs_count[pair]:
                max_pairs_count[pair] = count
                
    max_atoms_count = {k: v for k, v in max_atoms_count.items() if v > 0}
    max_pairs_count = {k: v for k, v in max_pairs_count.items() if v > 0}
    
    return unique_atoms, max_atoms_count, max_pairs_count

def calculate_bob(atoms, coords, max_atoms_count, max_pairs_count):
    N = len(atoms)
    Z = [ATOMIC_PROPS[a]['Z'] for a in atoms]
    
    atom_bags = {k: [] for k in max_atoms_count.keys()}
    pair_bags = {k: [] for k in max_pairs_count.keys()}
    
    for i in range(N):
        atom_bags[atoms[i]].append(0.5 * (Z[i] ** 2.4))
        for j in range(i + 1, N):
            pair = tuple(sorted([atoms[i], atoms[j]]))
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist == 0: dist = 1e-6
            val = (Z[i] * Z[j]) / dist
            pair_bags[pair].append(val)
            
    bob_vector = []
    vector_names = []
    
    for atom, max_size in sorted(max_atoms_count.items()):
        values = sorted(atom_bags[atom], reverse=True)
        padded = values + [0.0] * (max_size - len(values))
        bob_vector.extend(padded)
        vector_names.extend([f"{atom}_{i}" for i in range(max_size)])
        
    for pair, max_size in sorted(max_pairs_count.items()):
        values = sorted(pair_bags[pair], reverse=True)
        padded = values + [0.0] * (max_size - len(values))
        bob_vector.extend(padded)
        pair_str = f"{pair[0]}_{pair[1]}"
        vector_names.extend([f"{pair_str}_{i}" for i in range(max_size)])
        
    N_ve = sum(ATOMIC_PROPS[a]['ve'] for a in atoms)
    bob_vector.append(N_ve)
    vector_names.append("N_ve")
    
    return bob_vector, vector_names

def main():
    directory = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries'
    files = glob.glob(os.path.join(directory, '*.xyz'))
    files = sorted(files, key=lambda x: int(os.path.basename(x).split('_')[0]) if os.path.basename(x).split('_')[0].isdigit() else x)
    
    print("Analizando el dataset para determinar tamaños de bolsas (Bag of Bonds)...")
    unique_atoms, max_atoms_count, max_pairs_count = analyze_dataset(files)
    
    total_features = sum(max_atoms_count.values()) + sum(max_pairs_count.values())
    print(f"Átomos únicos: {unique_atoms}")
    print(f"Max átomos: {max_atoms_count}")
    print(f"Número total de features en BoB: {total_features} + 1 (N_ve) = {total_features + 1}")
    
    data = []
    total = len(files)
    print(f"Procesando {total} archivos XYZ...")
    
    vector_names = None
    for i, f in enumerate(files):
        try:
            filename = os.path.basename(f)
            _, atoms, coords = parse_xyz(f)
            bob_v, v_names = calculate_bob(atoms, coords, max_atoms_count, max_pairs_count)
            if vector_names is None:
                vector_names = ['filename'] + v_names
            data.append([filename] + bob_v)
        except Exception as e:
            print(f"Error procesando {f}: {e}")
            
        if (i + 1) % 200 == 0:
            print(f"Progreso: {i + 1}/{total}")
            
    df = pd.DataFrame(data, columns=vector_names)
    
    output_path = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/bob_features.csv'
    df.to_csv(output_path, index=False)
    print(f"\nProceso completado.")
    print(f"Forma de la matriz BoB: {df.shape}")
    print(f"Guardado en: {output_path}")

if __name__ == '__main__':
    main()
