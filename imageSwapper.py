import random
from argparse import ArgumentParser
from os import path, listdir, makedirs

from PIL import Image


def get_bool(prompt):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter True or False!")


def get_list_of_files(dir_name):
    list_of_file = listdir(dir_name)
    all_files = list()
    for entry in list_of_file:
        full_path = path.join(dir_name, entry)
        if path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def get_file_info(input_images: str, swap_folder: str, output_dir: bool):
    input_files = get_list_of_files(input_images)
    swap_files = get_list_of_files(swap_folder)
    base_files = {}
    for file in input_files:
        image = Image.open(file)
        base_files[file] = image.size
    if len(base_files.keys()) > len(swap_files):
        if get_bool(
                f"You have more source images ({len(base_files.keys())}) than you have swap images({len(swap_files)}).\nShould we loop? True or False.\n>"):
            randomized_list = random.choices(swap_files, k=len(base_files.keys()))
        else:
            exit()
    else:
        randomized_list = random.sample(swap_files, len(input_images))
    iter_num = 0
    for key, value in base_files.items():
        print(f"{key} was replaced with: {randomized_list[iter_num]}")
        image = Image.open(randomized_list[iter_num])
        image = image.convert('RGB')
        image = image.resize(value)
        if output_dir:
            if not path.isdir(f'{output_dir}/{key.replace(input_images, "").replace(path.basename(key), "")}'):
                makedirs(f'{output_dir}/{key.replace(input_images, "").replace(path.basename(key), "")}')
            image.save(f'{output_dir}/{key.replace(input_images, "")}')
        else:
            image.save(key, 'JPEG')
        iter_num += 1


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_images', type=str, help="Images you are hoping to replace.")
    parser.add_argument('-s', '--swap_folder', type=str,
                        help="Your folder of images you want to use to swap with the ones in input.")
    parser.add_argument('-o', '--output_dir', default=None, type=str, help="Output directory, optional.")
    args = parser.parse_args()
    get_file_info(swap_folder=args.swap_folder, input_images=args.input_images, output_dir=args.output_dir)
