
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
poetry run python imageSwapper.py <input_folder> <template_folder> <output_folder> [do_not_duplicate]
```

Arguments:
- `<input_folder>`: Directory containing the images to process.
- `<template_folder>`: Directory containing the template images.
- `<output_folder>`: Directory where processed images will be saved.
- `[do_not_duplicate]` (optional): Flag to control template reuse across multiple images. Use `true`, `yes`, or `1` to allow template reuse. If omitted, the script defaults to not reusing templates.

### Example Command
```bash
poetry run python imageSwapper.py "C:/images/input" "C:/images/templates" "C:/images/output" true
```
This processes images from `"C:/images/input"`, matches them with templates from `"C:/images/templates"`, outputs to `"C:/images/output"`, and allows template reuse.

## Support
For questions or issues, please open an issue on the project's GitHub repository page.
