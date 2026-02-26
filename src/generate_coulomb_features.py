import os
import glob
import numpy as np
import pandas as pd

# Propiedades atómicas para el número atómico (Z) y electrones de valencia (ve)
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
        # Corrección por si el átomo tiene formato con números (ej. C1)
        atom_symbol = ''.join([c for c in atom if c.isalpha()])
        if atom_symbol not in ATOMIC_PROPS:
            atom_symbol = atom_symbol.capitalize() # Por si acaso
        x, y, z = map(float, parts[1:4])
        atoms.append(atom_symbol)
        coords.append([x, y, z])
        
    return molecule_name, atoms, np.array(coords)

def build_coulomb_matrix(atoms, coords):
    N = len(atoms)
    M = np.zeros((N, N))
    Z = np.array([ATOMIC_PROPS[a]['Z'] for a in atoms])
    
    for i in range(N):
        M[i, i] = 0.5 * (Z[i] ** 2.4)
        for j in range(i + 1, N):
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist == 0:
                dist = 1e-6 # evitar división por cero si dos átomos están en el mismo lugar
            val = (Z[i] * Z[j]) / dist
            M[i, j] = val
            M[j, i] = val
            
    return M

def get_valence_electrons(atoms):
    return sum(ATOMIC_PROPS[a]['ve'] for a in atoms)

def extract_features(filepath):
    molecule_name, atoms, coords = parse_xyz(filepath)
    filename = os.path.basename(filepath)
    
    M = build_coulomb_matrix(atoms, coords)
    
    # Extraer autovalores y ordenar de forma descendente
    eigvals = np.linalg.eigvalsh(M)
    eigvals = np.sort(eigvals)[::-1]
    
    # Vectorización y padding hasta MAX_ATOMS
    padded_eigvals = np.zeros(MAX_ATOMS)
    padded_eigvals[:len(eigvals)] = eigvals
    
    # Feature de Control (N_ve)
    N_ve = get_valence_electrons(atoms)
    
    return [filename] + list(padded_eigvals) + [N_ve]

def main():
    directory = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries'
    files = glob.glob(os.path.join(directory, '*.xyz'))
    
    # Ordenar por el número inicial del archivo
    files = sorted(files, key=lambda x: int(os.path.basename(x).split('_')[0]) if os.path.basename(x).split('_')[0].isdigit() else x)
    
    data = []
    total = len(files)
    print(f"Procesando {total} archivos XYZ...")
    
    for i, f in enumerate(files):
        try:
            data.append(extract_features(f))
        except Exception as e:
            print(f"Error procesando {f}: {e}")
            
        if (i + 1) % 200 == 0:
            print(f"Progreso: {i + 1}/{total}")
            
    col_names = ['filename'] + [f'eig_{i}' for i in range(MAX_ATOMS)] + ['N_ve']
    df = pd.DataFrame(data, columns=col_names)
    
    output_path = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/coulomb_features.csv'
    df.to_csv(output_path, index=False)
    print(f"\nProceso completado.")
    print(f"Forma de la matriz de features: {df.shape}")
    print(f"Guardado en: {output_path}")

if __name__ == '__main__':
    main()
