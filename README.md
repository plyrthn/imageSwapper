# Image Swapper

## Introduction
Image Swapper is a Python script that automates the process of swapping images from an input directory with templates from a template directory, processing them accordingly, and outputting the results to a specified directory. It leverages ImageMagick for complex image processing tasks, including resizing and converting image formats.

## Requirements
- Python 3.6 or higher
- Poetry for dependency management
- ImageMagick installed and accessible from the command line

## Installation

### Install ImageMagick
Ensure ImageMagick is installed on your system and that the `magick` command is accessible from the command line. Visit [ImageMagick's official website](https://imagemagick.org) for installation instructions.

### Setup with Poetry
After cloning the project, navigate to the project directory and run the following command to install Python dependencies via Poetry:

```bash
poetry install
```

This command sets up a virtual environment and installs the necessary dependencies defined in `pyproject.toml`.

## Usage
To use the script, you can run it through Poetry to ensure it executes in the correct virtual environment. Use the following command format:

```bash
poetry run python imageSwapper.py <input_folder> <template_folder> <output_folder> [--do_not_duplicate]
```

### Arguments
- `<input_folder>`: Directory containing the images to process. For example, a folder containing memes or other images you want resized.
- `<template_folder>`: Directory containing the template images. These are the images to match for size and output format.
- `<output_folder>`: Directory where processed images will be saved.
- `--do_not_duplicate` (optional): Flag to prevent template reuse across multiple images. If omitted, templates may be reused.

### Example Command
```bash
poetry run python imageSwapper.py "M:/Pictures/memes" "C:/Users/James/AppData/Local/FortniteGame/Saved/PersistentDownloadDir/CMS/Files/C28FF1DE0C661DAF01E118A30B3F21B897A7A6E2bak" "C:/Users/James/AppData/Local/FortniteGame/Saved/PersistentDownloadDir/CMS/Files/C28FF1DE0C661DAF01E118A30B3F21B897A7A6E2" --do_not_duplicate
```

This processes images from `"M:/Pictures/memes"`, matches them with templates from `"C:/Users/James/AppData/Local/FortniteGame/Saved/PersistentDownloadDir/CMS/Files/C28FF1DE0C661DAF01E118A30B3F21B897A7A6E2bak"`, and outputs processed images to `"C:/Users/James/AppData/Local/FortniteGame/Saved/PersistentDownloadDir/CMS/Files/C28FF1DE0C661DAF01E118A30B3F21B897A7A6E2"`. The `--do_not_duplicate` flag ensures templates are used only once.

## Features
1. **Input File Handling**: Accepts various image formats like JPG, PNG, WEBP, and BMP from the input directory.
2. **Template Matching**: Uses DDS template files to determine the output image size and format.
3. **Flexible Processing**: Optionally prevents duplication of templates using the `--do_not_duplicate` flag.
4. **Parallel Processing**: Leverages multi-threading to speed up the resizing and conversion of images.
5. **Detailed Logging**: Logs operations and errors to `imageSwapper.log` for debugging purposes.

## Troubleshooting
### Common Issues
1. **ImageMagick Not Found**: Ensure that ImageMagick is installed and the `magick` command is in your system's PATH.
2. **Invalid Directories**: Verify that the paths for `input_folder`, `template_folder`, and `output_folder` are correct.
3. **Permission Errors**: Ensure that you have read and write permissions for the specified directories.

### Debugging Logs
Check the `imageSwapper.log` file in the script's directory for detailed logs of the script's execution.

## Support
For questions or issues, please open an issue on the project's GitHub repository page.
