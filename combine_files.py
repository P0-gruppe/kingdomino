import os
from sys import argv
from PIL import Image

def combine_images(input_dir, output_file):
    # Get all .jpg files in the input directory
    jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')]
    
    if not jpg_files:
        print("No .jpg files found in the specified directory.")
        return

    # Open the first image to get the size
    images = [Image.open(os.path.join(input_dir, jpg_files[0]))]
    width, height = images[0].size

    # Open all other images
    for filename in jpg_files[1:]:
        img = Image.open(os.path.join(input_dir, filename))
        if img.size != (width, height):
            img = img.resize((width, height))
        images.append(img)

    # Create a new image with a height that's the sum of all image heights
    combined_height = height * len(images)
    combined_image = Image.new('RGB', (width, combined_height))

    # Paste all images into the new image
    for i, img in enumerate(images):
        combined_image.paste(img, (0, i * height))

    # Save the combined image
    combined_image.save(output_file)
    print(f"Combined image saved as {output_file}")

# Example usage
input_directory = argv[1]
output_file = 'output.jpg'

combine_images(input_directory, output_file)