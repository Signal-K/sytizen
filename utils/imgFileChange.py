import os
from PIL import Image

def convert_jpeg_to_png():
    """
    Convert all .jpeg and .jpg files to .png in the current directory and its subdirectories.
    """
    current_directory = os.getcwd()  # Get the directory where the script is located
    print(f"Scanning for .jpeg and .jpg files in: {current_directory}")

    for root, _, files in os.walk(current_directory):  # Walk through all directories
        for file in files:
            if file.lower().endswith(('.jpeg', '.jpg')):  # Check for .jpeg or .jpg
                jpeg_path = os.path.join(root, file)  # Full path to the file
                png_path = os.path.splitext(jpeg_path)[0] + ".png"  # Replace extension with .png

                try:
                    # Open and convert the image
                    with Image.open(jpeg_path) as img:
                        img.convert("RGBA").save(png_path, "PNG")
                    print(f"Converted: {jpeg_path} -> {png_path}")

                    # Optionally delete the original file
                    # os.remove(jpeg_path)
                except Exception as e:
                    print(f"Error converting {jpeg_path}: {e}")

if __name__ == "__main__":
    print("Starting conversion of .jpeg and .jpg files to .png...")
    convert_jpeg_to_png()
    print("Conversion completed.")