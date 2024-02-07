import os
import subprocess

import numpy as np
from PIL import Image


def get_files(directory, extensions):
    """
    Retrieve files with specific extensions from a directory.
    """
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1].lower() in extensions:
                files_list.append(os.path.join(root, file))
    return files_list


def match_template(input_image_path, template_files):
    """
    Select a random template and return its path and properties using ImageMagick.
    """
    while template_files:  # Keep trying until a compatible file is found or the list is exhausted
        template_path = np.random.choice(template_files, replace=False)
        try:
            # Use ImageMagick's identify command to get image size
            result = subprocess.run(['magick', 'identify', '-format', '%wx%h', template_path],
                                    capture_output=True, text=True, check=True)
            size_str = result.stdout.strip()
            width, height = map(int, size_str.split('x'))
            template_info = {'path': template_path, 'size': (width, height), 'format': 'DDS'}
            template_files.remove(template_path)  # Remove selected template to avoid repetition
            return template_info
        except subprocess.CalledProcessError as e:
            print(f"Skipping unsupported template {template_path}: {e}")
            template_files.remove(template_path)  # Remove unsupported template from consideration

    return None  # Return None if no compatible template is found


def process_images(input_folder, template_folder, output_folder):
    extensions = ['jpg', 'jpeg', 'png', 'webp', 'bmp']
    input_files = get_files(input_folder, extensions)
    template_files = get_files(template_folder, ['dds'])  # Assuming DDS is the desired format

    # Ensure the list of templates is reused once all have been selected
    original_template_files = template_files.copy()

    for input_file in input_files:
        if not template_files:  # Replenish the list if empty
            template_files = original_template_files.copy()

        template_info = match_template(input_file, template_files)
        if template_info is None:
            print(f"No compatible template found for {input_file}. Skipping.")
            continue  # Skip to the next input file if no compatible template was found

        # Construct output path
        relative_path = os.path.relpath(template_info['path'], template_folder)
        output_path = os.path.join(output_folder, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Update the output path's extension to .dds
        output_path_dds = output_path.rsplit('.', 1)[0] + '.dds'

        # Use ImageMagick to resize and convert the input image to match the template, ignoring aspect ratio
        try:
            subprocess.run([
                'magick', 'convert', input_file,
                '-resize', f"{template_info['size'][0]}x{template_info['size'][1]}!",
                output_path_dds
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {input_file}: {e}")
            continue

    print("Processing complete.")



if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python script.py <input_folder> <template_folder> <output_folder>")
    else:
        input_folder, template_folder, output_folder = sys.argv[1:]
        process_images(input_folder, template_folder, output_folder)
