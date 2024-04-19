import itertools
import logging
import os
import subprocess
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from numpy import random

logging.basicConfig(filename="imageSwapper.log", level=logging.DEBUG, filemode="w")


def get_files(directory, extensions):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split(".")[-1].lower() in extensions:
                files_list.append(os.path.join(root, file))
    return files_list


def match_template(template_files):
    template_path = np.random.choice(template_files)
    try:
        result = subprocess.run(
            ["magick", "identify", "-format", "%wx%h", template_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        size_str = result.stdout.strip()
        # Strip non-printable characters before logging
        clean_size_str = "".join(filter(str.isprintable, size_str))
        if clean_size_str.count("x") == 1:
            width, height = map(int, clean_size_str.split("x"))
            logging.debug(
                f"Attempting to use template: {template_path} with size: {width}x{height}"
            )
            return {"path": template_path, "size": (width, height), "format": "DDS"}
        else:
            logging.error(
                f"Unexpected size format for template {template_path}: {clean_size_str}"
            )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing template {template_path}: {e}")
    return None


def process_images(
    input_folder, template_folder, output_folder, do_not_duplicate=False
):
    extensions = ["jpg", "jpeg", "png", "webp", "bmp"]
    input_files = get_files(input_folder, extensions)
    logging.info(f"Total input files found: {len(input_files)}")
    template_files = get_files(template_folder, ["dds"])
    processed_files_count = 0

    with ProcessPoolExecutor() as executor:
        future_to_file = {}

        if do_not_duplicate:
            random.shuffle(input_files)  # Shuffle the list for random processing order
            input_files_iterator = iter(input_files)
        else:
            input_files_iterator = itertools.cycle(
                input_files
            )  # Prepare for potentially infinite cycling

        try:
            while template_files:
                # If not duplicating, shuffle the input_files list each time it's fully iterated
                if (
                    do_not_duplicate
                    and future_to_file
                    and all(future.done() for future in future_to_file)
                ):
                    random.shuffle(input_files)
                    input_files_iterator = iter(input_files)  # Reset the iterator

                input_file = next(input_files_iterator)
                if not template_files:
                    break  # Stop if there are no template files left

                template_info = match_template(template_files)
                if template_info is None:
                    logging.warning(
                        f"No compatible template found for {input_file}. Skipping."
                    )
                    continue

                output_path_dds = construct_output_path(
                    template_info, output_folder, template_folder
                )
                template_files.remove(
                    template_info["path"]
                )  # Remove the used template from the list

                future = executor.submit(
                    resize_and_convert_image,
                    input_file,
                    output_path_dds,
                    template_info["size"],
                )
                future_to_file[future] = input_file

        except StopIteration:
            # This exception should only occur if do_not_duplicate is True and we've exhausted input_files
            logging.info("Exhausted all input files.")

        # Wait for all futures to complete
        for future in as_completed(future_to_file):
            input_file = future_to_file[future]
            if future.result():
                processed_files_count += 1
                logging.info(f"Successfully processed {input_file}")
            else:
                logging.error(f"Failed to process {input_file}")

    logging.info(f"Processing complete. Processed: {processed_files_count} files.")


def resize_and_convert_image(input_file, output_path_dds, size):
    try:
        subprocess.run(
            [
                "magick",
                "convert",
                input_file,
                "-resize",
                f"{size[0]}x{size[1]}!",
                output_path_dds,
            ],
            check=True,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Exception occurred while processing {input_file}: {e}")
        return False


def construct_output_path(template_info, output_folder, template_folder):
    relative_path = os.path.relpath(template_info["path"], template_folder)
    output_path = os.path.join(output_folder, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path.rsplit(".", 1)[0] + ".dds"


if __name__ == "__main__":
    import sys

    if not (4 <= len(sys.argv) <= 5):
        print(
            "Usage: python script.py <input_folder> <template_folder> <output_folder> [do_not_duplicate]"
        )
        sys.exit(1)
    input_folder, template_folder, output_folder = sys.argv[1:4]
    do_not_duplicate = len(sys.argv) == 5 and sys.argv[4].lower() in [
        "true",
        "yes",
        "1",
    ]
    process_images(input_folder, template_folder, output_folder, do_not_duplicate)
