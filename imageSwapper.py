import argparse
import itertools
import logging
import os
import platform
import subprocess
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from numpy import random

# Setup logging
logging.basicConfig(filename="imageSwapper.log", level=logging.DEBUG, filemode="w")


def validate_directory(path, create_if_missing=False):
    """
    Validate that a directory exists, and optionally create it if missing.

    :param path: Path to validate.
    :param create_if_missing: Whether to create the directory if it doesn't exist.
    :return: The absolute path of the directory if valid.
    """
    absolute_path = os.path.abspath(path)
    if not os.path.exists(absolute_path):
        if create_if_missing:
            os.makedirs(absolute_path, exist_ok=True)
            logging.info(f"Created missing directory: {absolute_path}")
        else:
            logging.error(f"Directory does not exist: {absolute_path}")
            raise FileNotFoundError(f"Directory does not exist: {absolute_path}")
    elif not os.path.isdir(absolute_path):
        logging.error(f"Path is not a directory: {absolute_path}")
        raise NotADirectoryError(f"Path is not a directory: {absolute_path}")
    return absolute_path


def get_files(directory, extensions):
    """Recursively find all files in a directory with specified extensions."""
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split(".")[-1].lower() in extensions:
                files_list.append(os.path.join(root, file))
    return files_list


def match_template(template_files):
    """Select and validate a random template file."""
    template_path = np.random.choice(template_files)
    try:
        # Determine the command prefix based on the operating system
        if platform.system() == "Linux":
            command = [
                "identify",  # On Linux, use "identify"
                "-format",
                "%wx%h",
                template_path,
            ]
        else:
            command = [
                "magick",  # On Windows or other OS, use "magick identify"
                "identify",
                "-format",
                "%wx%h",
                template_path,
            ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )

        size_str = result.stdout.strip()
        clean_size_str = "".join(filter(str.isprintable, size_str))

        if clean_size_str.count("x") == 1:
            width, height = map(int, clean_size_str.split("x"))
            logging.debug(
                f"Attempting to use template: {template_path} with size: {width}x{height}"
            )
            return {"path": template_path, "size": (width, height)}
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
    """Process images using templates to resize and convert them."""
    extensions = ["jpg", "jpeg", "png", "webp", "bmp", "dds"]
    input_files = get_files(input_folder, extensions)
    logging.info(f"Total input files found: {len(input_files)}")
    template_files = get_files(template_folder, extensions)
    processed_files_count = 0

    with ProcessPoolExecutor() as executor:
        future_to_file = {}

        if do_not_duplicate:
            random.shuffle(input_files)
            input_files_iterator = iter(input_files)
        else:
            input_files_iterator = itertools.cycle(input_files)

        try:
            while template_files:
                input_file = next(input_files_iterator)
                if not template_files:
                    break

                template_info = match_template(template_files)
                if template_info is None:
                    logging.warning(
                        f"No compatible template found for {input_file}. Skipping."
                    )
                    continue

                output_path = construct_output_path(template_info, output_folder)
                template_files.remove(template_info["path"])

                future = executor.submit(
                    resize_and_convert_image,
                    input_file,
                    output_path,
                    template_info["size"],
                )
                future_to_file[future] = input_file

        except StopIteration:
            logging.info("Exhausted all input files.")

        for future in as_completed(future_to_file):
            input_file = future_to_file[future]
            if future.result():
                processed_files_count += 1
                logging.info(f"Successfully processed {input_file}")
            else:
                logging.error(f"Failed to process {input_file}")

    logging.info(f"Processing complete. Processed: {processed_files_count} files.")


def resize_and_convert_image(input_file, output_path, size):
    """Resize and convert an image to the appropriate format using ImageMagick."""
    try:
        # Determine the command prefix based on the operating system
        if platform.system() == "Linux":
            command = [
                "convert",
                input_file,
                "-resize",
                f"{size[0]}x{size[1]}!",
                output_path,
            ]
        else:
            command = [
                "magick",
                "convert",
                input_file,
                "-resize",
                f"{size[0]}x{size[1]}!",
                output_path,
            ]

        subprocess.run(
            command,
            check=True,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Exception occurred while processing {input_file}: {e}")
        return False


def construct_output_path(template_info, output_folder):
    """Construct output file path based on template file name and extension."""
    template_filename = os.path.basename(
        template_info["path"]
    )  # Use template's filename
    output_path = os.path.join(output_folder, template_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path


def main():
    """Parse arguments and initiate processing."""
    parser = argparse.ArgumentParser(
        description="Image Swapper: Resizes and replaces images using templates."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Path to the folder containing the images to resize and process.",
    )
    parser.add_argument(
        "template_folder",
        type=str,
        help="Path to the folder containing template images.",
    )
    parser.add_argument(
        "output_folder",
        type=str,
        help="Path to the folder where processed images will be saved.",
    )
    parser.add_argument(
        "--do_not_duplicate",
        action="store_true",
        help="Prevent template reuse. Each template will be used only once.",
    )

    args = parser.parse_args()

    # Validate directories
    input_folder = validate_directory(args.input_folder)
    template_folder = validate_directory(args.template_folder)
    output_folder = validate_directory(args.output_folder, create_if_missing=True)

    # Process images
    process_images(input_folder, template_folder, output_folder, args.do_not_duplicate)

    logging.info("Script execution completed.")


if __name__ == "__main__":
    main()
