import os
import re

def sanitize_filename(name):
    """Sanitize the molecule name to be used as a filename."""
    # Remove characters that are generally invalid in filenames
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Replace spaces with underscores
    name = name.replace(" ", "_").replace("(", "").replace(")", "")
    return name.strip()

def split_xyz(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r') as f:
        lines = f.readlines()

    molecule_count = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        try:
            num_atoms = int(line)
            # XYZ format: line 0 is atom count, line 1 is comment/name, then 'num_atoms' lines follow
            comment = lines[i+1].strip()
            
            molecule_lines = lines[i : i + 2 + num_atoms]
            
            # Use sanitized comment as filename, or a default if empty
            base_name = sanitize_filename(comment) if comment else f"molecule_{molecule_count:04d}"
            
            # Ensure unique filename by appending index if needed
            file_name = f"{molecule_count:04d}_{base_name}.txt"
            output_path = os.path.join(output_dir, file_name)
            
            with open(output_path, 'w') as out_f:
                out_f.writelines(molecule_lines)
            
            molecule_count += 1
            i += 2 + num_atoms
        except (ValueError, IndexError):
            # If line is not an integer or not enough lines left, skip
            i += 1

    print(f"Extraction complete. {molecule_count} molecules extracted to {output_dir}")

if __name__ == "__main__":
    src_file = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/1694prunedHOF_geom_01 (1).xyz"
    out_directory = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/structure/individual_geometries"
    split_xyz(src_file, out_directory)
