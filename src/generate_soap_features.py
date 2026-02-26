import os
import glob
import numpy as np
import pandas as pd
from dscribe.descriptors import SOAP
from ase import Atoms

ATOMIC_PROPS = {
    'H':  {'ve': 1}, 'Li': {'ve': 1}, 'Be': {'ve': 2}, 'B':  {'ve': 3},
    'C':  {'ve': 4}, 'N':  {'ve': 5}, 'O':  {'ve': 6}, 'F':  {'ve': 7},
    'Na': {'ve': 1}, 'Mg': {'ve': 2}, 'Al': {'ve': 3}, 'Si': {'ve': 4},
    'P':  {'ve': 5}, 'S':  {'ve': 6}, 'Cl': {'ve': 7}, 'K':  {'ve': 1},
    'Ca': {'ve': 2}, 'Ga': {'ve': 3}, 'Ge': {'ve': 4}, 'As': {'ve': 5},
    'Se': {'ve': 6}, 'Br': {'ve': 7}, 'I':  {'ve': 7}
}

def parse_xyz_to_ase(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    num_atoms = int(lines[0].strip())
    
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
        
    ase_atoms = Atoms(symbols=atoms, positions=coords)
    return ase_atoms, atoms

def get_unique_elements(files):
    unique_elements = set()
    for f in files:
        _, atoms = parse_xyz_to_ase(f)
        unique_elements.update(atoms)
    return sorted(list(unique_elements))

def main():
    directory = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries'
    files = glob.glob(os.path.join(directory, '*.xyz'))
    files = sorted(files, key=lambda x: int(os.path.basename(x).split('_')[0]) if os.path.basename(x).split('_')[0].isdigit() else x)
    
    print("Analizando elementos únicos en el dataset...")
    unique_elements = get_unique_elements(files)
    print(f"Elementos únicos encontrados: {unique_elements}")
    
    # Configuración de SOAP según requerimientos
    soap = SOAP(
        species=unique_elements,
        periodic=False,
        r_cut=6.0,          # Radio de corte de 6.0 Å
        n_max=8,            # Expansión radial de bases
        l_max=6,            # Armónicos esféricos
        average="inner",    # Calcular promedio sobre todos los átomos (para tener vector de tamaño fijo)
        sparse=False
    )
    
    data = []
    total = len(files)
    print(f"\nProcesando {total} archivos XYZ usando SOAP...")
    
    # Obtener el tamaño de features
    n_features = soap.get_number_of_features()
    
    print(f"Radio (r_cut): {soap._r_cut}")
    print(f"Bases radiales (n_max): {soap._n_max}")
    print(f"Armónicos esféricos (l_max): {soap._l_max}")
    print(f"Vector size per molecule: {n_features} + 1 (N_ve)")
    
    for i, f in enumerate(files):
        try:
            filename = os.path.basename(f)
            ase_atoms, atom_symbols = parse_xyz_to_ase(f)
            
            # Generar features de SOAP promediadas para la molécula
            features = soap.create(ase_atoms)
            
            # Manejar el caso donde average="inner" retorna un array 1D envuelto o directo
            if len(features.shape) > 1:
                features = features.mean(axis=0)
            else:
                features = features.flatten()
            
            # Control Feature N_ve
            N_ve = sum(ATOMIC_PROPS[a]['ve'] for a in atom_symbols)
            
            # Guardamos los features y el N_ve al final
            row = [filename] + list(features) + [N_ve]
            data.append(row)
            
        except Exception as e:
            print(f"Error procesando {f}: {e}")
            
        if (i + 1) % 50 == 0:
            print(f"Progreso: {i + 1}/{total}")
            
    # Crear los encabezados
    columns = ['filename'] + [f'soap_{j}' for j in range(n_features)] + ['N_ve']
    
    df = pd.DataFrame(data, columns=columns)
    output_path = '/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/soap_features.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nProceso completado exitosamente.")
    print(f"Forma de la matriz SOAP: {df.shape}")
    print(f"Guardado en: {output_path}")

if __name__ == '__main__':
    main()
