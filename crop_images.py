from PIL import Image
import sys


def crop_to_banner(image_path, output_path, banner_width, banner_height):
    # Open the image
    img = Image.open(image_path)

    # Get original dimensions
    img_width, img_height = img.size

    # Calculate cropping box (centered)
    left = (img_width - banner_width) / 2
    top = (img_height - banner_height) / 2
    right = (img_width + banner_width) / 2
    bottom = (img_height + banner_height) / 2

    # Crop the image
    banner = img.crop((left, top, right, bottom))
    
    print("Image new size: ", banner.size)

    # Save the banner image
    banner.save(output_path)


# Example usage
image = sys.argv[1]
crop_to_banner(
    f"images/{image}.png",
    f"images/{image}-Banner.png",
    banner_width=1000,
    banner_height=350,
)
