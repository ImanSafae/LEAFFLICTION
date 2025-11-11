import argparse
from os.path import exists, splitext
from PIL import Image, ImageFilter, ImageEnhance
import math

def rotate_image(image: Image):
    img_rotated = image.rotate(60)
    name, ext = splitext(image.filename)
    img_rotated.save(name + "_Rotate" + ext)

def blur_image(image: Image):
    img_blurred = image.filter(filter=ImageFilter.BoxBlur(15))
    name, ext = splitext(image.filename)
    img_blurred.save(name + "_Blur" + ext)

def zoom_into_image(image: Image):
    initial_width, initial_heigth = image.size
    width_offset = (initial_width * 0.5) / 2
    heigth_offset = (initial_heigth * 0.5) / 2
    new_left = width_offset
    new_right = initial_width - width_offset
    new_top = heigth_offset
    new_bottom = initial_heigth - heigth_offset
    # new_size = (math.floor(initial_width * 0.7), math.floor(initial_heigth * 0.7))
    img_zoomed = image.crop((new_left, new_top, new_right, new_bottom))
    # img_zoomed = img_zoomed.resize(new_size)
    name, ext = splitext(image.filename)
    img_zoomed.save(name + "_Zoom" + ext)

def flip_image(image: Image):
    img_flipped = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    name, ext = splitext(image.filename)
    img_flipped.save(name + "_Flip" + ext)

def illuminate_image(image: Image):
    enhancer = ImageEnhance.Brightness(image)
    img_illuminated = enhancer.enhance(1.5)
    name, ext = splitext(image.filename)
    img_illuminated.save(name + "_Illuminate" + ext)

def contrast_image(image):
    enhancer = ImageEnhance.Contrast(image)
    img_contrasted = enhancer.enhance(2)
    name, ext = splitext(image.filename)
    img_contrasted.save(name + "_Contrast" + ext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Augmentation.py',
                                     usage='%(prog)s [path to a picture] [-n COUNT]',
                                     description='Displays and creates augmented versions of the provided picture.')
    parser.add_argument("pic_path")
    parser.add_argument("-n", type=int, default=6, help="Number of augmentations to create (default: 6)")
    args = parser.parse_args()
    pic = args.pic_path
    print("Pic:", pic)
    if (not exists(pic) or not pic.lower().endswith((".jpg", ".jpeg", ".png"))):
        print("Provided argument should be a path to a picture.")
        exit(1)
    
    augmentations = [rotate_image, blur_image, zoom_into_image, flip_image, illuminate_image, contrast_image]
    num_to_create = min(args.n, len(augmentations))
    
    with Image.open(pic) as img:
        for i in range(num_to_create):
            augmentations[i](img)
    
    
