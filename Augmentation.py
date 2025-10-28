import argparse
from os.path import isfile, join, exists, isdir, splitext
from PIL import Image, ImageFilter

def rotate_image(image: Image):
    img_rotated = image.rotate(60)
    name, ext = splitext(image.filename)
    img_rotated.save(name + "_Rotate" + ext)

def blur_image(image: Image):
    img_blurred = image.filter(filter=ImageFilter.BoxBlur(15))
    name, ext = splitext(image.filename)
    img_blurred.save(name + "_Blur" + ext)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Augmentation.py',
                                     usage='%(prog)s [path to a picture]',
                                     description='Displays and creates 6 new augmented versions of the provided picture.')
    parser.add_argument("pic_path")
    args = parser.parse_args()
    pic = args.pic_path
    print("Pic:", pic)
    if (not exists(pic) or not pic.lower().endswith((".jpg", ".jpeg", ".png"))):
        print("Provided argument should be a path to a picture.")
        exit(1)
    with Image.open(pic) as img:
        rotate_image(img)
        blur_image(img)
    
    
