from argparse import ArgumentParser
from glob import glob
from os import path

from PIL import Image


def get_bool(prompt):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter True or False!")


def get_file_info(swap_folder: str, input_images: str, output_dir: bool, loop_images: bool):
    glob_pattern = path.join(input_images, '*.*')
    input_files = sorted(glob(glob_pattern, recursive=True), key=path.getctime)

    glob_pattern = path.join(swap_folder, '*.*')
    swap_folder = sorted(glob(glob_pattern, recursive=True), key=path.getctime)
    base_files = {}
    for file in input_files:
        image = Image.open(file)
        base_files[file] = image.size
    if len(input_images) > len(swap_folder) and not loop_images:
        if not get_bool("You have more source images than you have swap images, loop?\n>"):
            exit()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_images', type=str, help="Images you are hoping to replace.")
    parser.add_argument('-s', '--swap_folder', type=str,
                        help="Your folder of images you want to use to swap with the ones in input.")
    parser.add_argument('-o', '--output_dir', default="", type=str, help="Output directory, optional.")
    parser.add_argument('-l', '--loop_images', default=False, type=bool,
                        help="Should we loop images if you don't have enough?\nTrue or False?")
    args = parser.parse_args()
    get_file_info(swap_folder=args.swap_folder, input_images=args.input_images, output_dir=args.output_dir,
                  loop_images=args.loop_images)
