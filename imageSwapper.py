import logging
import os
import subprocess
import numpy as np

logging.basicConfig(filename='imageSwapper.log', level=logging.DEBUG, filemode='w')

def get_files(directory, extensions):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1].lower() in extensions:
                files_list.append(os.path.join(root, file))
    return files_list

def match_template(template_files):
    template_path = np.random.choice(template_files)
    logging.debug(f"Attempting to use template: {template_path}")
    try:
        result = subprocess.run(['magick', 'identify', '-format', '%wx%h', template_path],
                                capture_output=True, text=True, check=True)
        size_str = result.stdout.strip()
        if size_str.count('x') == 1:
            width, height = map(int, size_str.split('x'))
            return {'path': template_path, 'size': (width, height), 'format': 'DDS'}
        else:
            logging.error(f"Unexpected size format for template {template_path}: {size_str}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing template {template_path}: {e}")
    return None

def process_images(input_folder, template_folder, output_folder, do_not_duplicate=False):
    extensions = ['jpg', 'jpeg', 'png', 'webp', 'bmp']
    input_files = get_files(input_folder, extensions)
    logging.info(f"Total input files found: {len(input_files)}")
    template_files = get_files(template_folder, ['dds'])
    processed_files_count = 0

    while template_files and input_files:
        for input_file in list(input_files): # Operate on a shallow copy to modify the original list
            logging.debug(f"Processing file: {input_file}")

            template_info = match_template(template_files)
            if template_info is None:
                logging.warning(f"No compatible template found for {input_file}. Skipping.")
                continue

            try:
                output_path_dds = construct_output_path(template_info, output_folder, template_folder)
                subprocess.run(['magick', 'convert', input_file, '-resize', f"{template_info['size'][0]}x{template_info['size'][1]}!", output_path_dds], check=True)
                processed_files_count += 1

                if do_not_duplicate:
                    input_files.remove(input_file) # Remove the processed input file if do_not_duplicate is True
                template_files.remove(template_info['path']) # Remove the used template from the list
            except subprocess.CalledProcessError as e:
                logging.error(f"Exception occurred while processing {input_file}: {e}")

    logging.info(f"Processing complete. Processed: {processed_files_count}")

def construct_output_path(template_info, output_folder, template_folder):
    relative_path = os.path.relpath(template_info['path'], template_folder)
    output_path = os.path.join(output_folder, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path.rsplit('.', 1)[0] + '.dds'

if __name__ == "__main__":
    import sys
    if not (4 <= len(sys.argv) <= 5):
        print("Usage: python script.py <input_folder> <template_folder> <output_folder> [do_not_duplicate]")
        sys.exit(1)
    input_folder, template_folder, output_folder = sys.argv[1:4]
    do_not_duplicate = len(sys.argv) == 5 and sys.argv[4].lower() in ['true', 'yes', '1']
    process_images(input_folder, template_folder, output_folder, do_not_duplicate)