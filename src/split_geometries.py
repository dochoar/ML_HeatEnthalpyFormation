import os
import re

def sanitize_filename(name):
    # Remove leading/trailing whitespace and replace internal spaces/special chars with underscores
    name = name.strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name

def split_xyz(input_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    with open(input_path, 'r') as f:
        lines = f.readlines()

    total_lines = len(lines)
    current_line = 0
    geom_count = 0

    while current_line < total_lines:
        line = lines[current_line].strip()
        if not line:
            current_line += 1
            continue
        
        try:
            num_atoms = int(line)
        except ValueError:
            print(f"Warning: Expected integer at line {current_line + 1}, found '{line}'. Skipping.")
            current_line += 1
            continue

        # Next line is the name/comment line
        name_line = lines[current_line + 1].strip() if current_line + 1 < total_lines else "unnamed"
        sanitized_name = sanitize_filename(name_line)
        
        # N atoms lines
        atom_lines = lines[current_line + 2 : current_line + 2 + num_atoms]
        
        # Construct filename
        filename = f"{geom_count:04d}_{sanitized_name}.xyz"
        output_path = os.path.join(output_dir, filename)
        
        # Write individual file
        with open(output_path, 'w') as out_f:
            out_f.write(f"{num_atoms}\n")
            out_f.write(f"{name_line}\n")
            for atom_line in atom_lines:
                out_f.write(atom_line)
                if not atom_line.endswith('\n'):
                    out_f.write('\n')
        
        # Move to next block
        current_line += 2 + num_atoms
        geom_count += 1

    print(f"Successfully split {geom_count} geometries into {output_dir}")

if __name__ == "__main__":
    input_file = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/1694prunedHOF_geom_01 (1).xyz"
    output_directory = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries"
    split_xyz(input_file, output_directory)
