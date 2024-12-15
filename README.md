
# Image Swapper

## Introduction
Image Swapper is a Python script that resizes and converts images from an input directory using templates from a template directory. The processed images are saved to an output directory. This tool is useful for batch processing large numbers of images, ensuring they match specific templates in size and format. It uses ImageMagick for the heavy lifting of image processing and logs all actions for easy troubleshooting.

## Features
- **Batch Image Processing**: Automatically processes multiple images at once.
- **Template Matching**: Uses images from the template directory to determine the output size and format.
- **Format Support**: Works with common image formats like JPG, PNG, BMP, WEBP, and DDS.
- **Parallel Execution**: Uses multiple processes to speed up processing.
- **Error Logging**: Logs detailed information about successes, errors, and unexpected events to `imageSwapper.log`.

## Prerequisites
- **Python 3.6 or higher**
- **ImageMagick**: Ensure that ImageMagick is installed and the `magick` command is available in your system's PATH. Visit [ImageMagick's official website](https://imagemagick.org) for installation instructions.

## Installation

1. **Install ImageMagick**
   - Download and install ImageMagick from [imagemagick.org](https://imagemagick.org/).
   - Make sure the `magick` command works in your terminal.

2. **Clone the repository**
   ```bash
   git clone https://github.com/username/image-swapper.git
   cd image-swapper
   ```

3. **Install dependencies** (optional)
   - If you use **Poetry**:
     ```bash
     poetry install
     ```
   - Otherwise, manually install Python packages:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

Run the following command to start swapping images:
```bash
python imageSwapper.py <input_folder> <template_folder> <output_folder> [--do_not_duplicate]
```

### Required Arguments
- **input_folder**: Path to the folder containing images to be processed.
- **template_folder**: Path to the folder containing template images.
- **output_folder**: Path to the folder where processed images will be saved.

### Optional Arguments
- **--do_not_duplicate**: If set, each template will only be used once. Without this flag, templates may be reused for multiple input images.

### Example Command
```bash
python imageSwapper.py "./input_images" "./templates" "./output_images" --do_not_duplicate
```
**Explanation:**
- Images from `./input_images` are processed to match templates from `./templates`.
- The processed images are saved in `./output_images`.
- The `--do_not_duplicate` flag ensures that each template is only used once.

## How It Works
1. **Input and Template Collection**: The script scans the input and template directories to collect supported image files.
2. **Template Matching**: Randomly selects a template image and determines its dimensions.
3. **Image Processing**: Uses ImageMagick to resize the input image to match the template size and saves it to the output directory.
4. **Parallel Execution**: Multiple images are processed concurrently for faster execution.

## Detailed Example
Assume the following directory structure:
```
project/
├── input_images/
│     └── image1.jpg
│     └── image2.png
├── templates/
│     └── template1.jpg
│     └── template2.png
├── output_images/  (This folder is created automatically)
```
Run the following command:
```bash
python imageSwapper.py ./input_images ./templates ./output_images --do_not_duplicate
```
After execution, `output_images` will contain the resized versions of `image1.jpg` and `image2.png` matching the sizes of `template1.jpg` and `template2.png`.

## Troubleshooting

**Problem:** ImageMagick `magick` command not found
- **Solution**: Ensure ImageMagick is installed and added to your system's PATH.

**Problem:** Input or template directory not found
- **Solution**: Double-check the paths provided in the command. Ensure they exist and are accessible.

**Problem:** No images are processed
- **Solution**: Make sure there are images in the input and template directories. Supported formats are JPG, PNG, BMP, WEBP, and DDS.

**Problem:** Logs indicate 'Error processing template'
- **Solution**: Verify that the template images are valid images and that ImageMagick can process them. Check the `imageSwapper.log` file for more details.

## Log File
All events, errors, and debugging information are saved in `imageSwapper.log`. This file is created in the same directory where the script runs.

## Support
If you encounter issues, review the `imageSwapper.log` file. It contains detailed information about the script's execution. For further help, open an issue on the project's GitHub repository.

## License
This project is licensed under the MIT License.
