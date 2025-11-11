import argparse
import cv2
from plantcv import plantcv as pcv
from os.path import exists, splitext, join, isdir, isfile, basename, normpath
from os import listdir, makedirs

def threshold_image(image: str, outdir=None):
    color_img, imgpath, imgname = pcv.readimage(image)
    grayscale_img = pcv.rgb2gray_lab(color_img, "l")
    thresholded_img = pcv.threshold.otsu(grayscale_img, "light")
    name, ext = splitext(imgname)
    output_path = join(outdir, name + "_Threshold" + ext) if outdir else name + "_Threshold" + ext
    pcv.print_image(thresholded_img, output_path)

def canny_edge_detection(image: str, outdir=None):
    color_img, imgpath, imgname = pcv.readimage(image)
    edges = pcv.canny_edge_detect(color_img,  sigma=1.3)
    name, ext = splitext(imgname)
    output_path = join(outdir, name + "_Edges" + ext) if outdir else name + "_Edges" + ext
    pcv.print_image(edges, output_path)

def analyze_size_and_shape(image: str, outdir=None):
    color_img, imgpath, imgname = pcv.readimage(image)
    pcv.params.line_thickness = 1
    grayscale_img = pcv.rgb2gray_lab(color_img, "l")
    thresholded_img = pcv.threshold.otsu(grayscale_img, "light")
    analyzed_img = pcv.analyze.size(color_img, thresholded_img)
    name, ext = splitext(imgname)
    output_path = join(outdir, name + "_Analyzed" + ext) if outdir else name + "_Analyzed" + ext
    pcv.print_image(analyzed_img, output_path)

def gaussian_blur(image: str, outdir=None):
    color_img, imgpath, imgname = pcv.readimage(image)
    blurred_img = pcv.gaussian_blur(color_img, (7, 7), 0)
    name, ext = splitext(imgname)
    output_path = join(outdir, name + "_Blurred" + ext) if outdir else name + "_Blurred" + ext
    pcv.print_image(blurred_img, output_path)

def isolate_from_bg(image_path, outdir=None):
    img, path, filename = pcv.readimage(image_path)
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    mask = pcv.threshold.otsu(gray_img=s, object_type='light')
    masked = pcv.apply_mask(img=img, mask=mask, mask_color='white')
    name, ext = splitext(filename)
    output_path = join(outdir, name + "_Isolated" + ext) if outdir else name + "_Isolated" + ext
    pcv.print_image(masked, output_path)

def pseudolandmarks(image_path, outdir=None):
    img, path, filename = pcv.readimage(image_path)
    s = pcv.rgb2gray_hsv(img, channel='s')
    mask = pcv.threshold.otsu(s, object_type='light')
    mask = pcv.fill(mask, size=200)
    top, bottom, center_v = pcv.homology.y_axis_pseudolandmarks(img=img, mask=mask)
    left, right, center_h = pcv.homology.x_axis_pseudolandmarks(img=img, mask=mask)
    landmark_img = img.copy()
    landmark_sets = [
        (top, (255, 255, 0), "TOP"),         # cyan - en haut
        (bottom, (255, 0, 255), "BOTTOM"),   # magenta - en bas
        (left, (0, 255, 0), "LEFT"),         # vert - à gauche
        (right, (0, 0, 255), "RIGHT"),       # rouge - à droite
        (center_v, (0, 128, 255), "CENTER_V"), # bleu clair - axe vertical
        (center_h, (255, 128, 0), "CENTER_H")  # orange - axe horizontal
    ]
    for points_array, color, label in landmark_sets:
        if points_array is not None and len(points_array) > 0:
            for pt in points_array:
                x, y = int(pt[0][0]), int(pt[0][1])
                cv2.circle(landmark_img, (x, y), 3, color, -1)
                cv2.circle(landmark_img, (x, y), 4, (255, 255, 255), 1)
    name, ext = splitext(filename)
    output_path = join(outdir, name + '_Pseudolandmarks' + ext) if outdir else name + '_Pseudolandmarks' + ext
    pcv.print_image(landmark_img, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Transformation.py")
    parser.add_argument("-src", required=True, help="Path to an image or directory")
    parser.add_argument("-dst", help="Destination directory for batch processing")
    args = parser.parse_args()
    src = args.src
    if not exists(src):
        print(f"Path {src} does not exist.")
        exit(1)
    if isfile(src) and src.lower().endswith((".jpg", ".jpeg", ".png")):
        threshold_image(src)
        canny_edge_detection(src)
        analyze_size_and_shape(src)
        gaussian_blur(src)
        pseudolandmarks(src)
        isolate_from_bg(src)
    elif isdir(src):
        if not args.dst:
            print("Destination directory (-dst) is required when processing a directory.")
            exit(1)
        source_folder_name = basename(normpath(src))
        output_dir = join(args.dst, source_folder_name)
        makedirs(output_dir, exist_ok=True)
        for filename in listdir(src):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = join(src, filename)
                threshold_image(image_path, output_dir)
                canny_edge_detection(image_path, output_dir)
                analyze_size_and_shape(image_path, output_dir)
                gaussian_blur(image_path, output_dir)
                pseudolandmarks(image_path, output_dir)
                isolate_from_bg(image_path, output_dir)
    else:
        print("Source must be an image file or a directory.")
        exit(1)
