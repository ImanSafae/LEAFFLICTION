import argparse
import cv2
from plantcv import plantcv as pcv
from os.path import exists, splitext

def threshold_image(image: str):
    color_img, imgpath, imgname = pcv.readimage(image)
    grayscale_img = pcv.rgb2gray_lab(color_img, "l")
    thresholded_img = pcv.threshold.otsu(grayscale_img, "light")
    name, ext = splitext(imgname)
    pcv.print_image(thresholded_img, name + "_Threshold" + ext)

def canny_edge_detection(image: str):
    color_img, imgpath, imgname = pcv.readimage(image)
    edges = pcv.canny_edge_detect(color_img,  sigma=1.3)
    name, ext = splitext(imgname)
    pcv.print_image(edges, name + "_Edges" + ext)

def analyze_size_and_shape(image: str):
    color_img, imgpath, imgname = pcv.readimage(image)
    pcv.params.line_thickness = 1
    grayscale_img = pcv.rgb2gray_lab(color_img, "l")
    thresholded_img = pcv.threshold.otsu(grayscale_img, "light")
    analyzed_img = pcv.analyze.size(color_img, thresholded_img)
    name, ext = splitext(imgname)
    pcv.print_image(analyzed_img, name + "_Analyzed" + ext)

def gaussian_blur(image: str):
    color_img, imgpath, imgname = pcv.readimage(image)
    blurred_img = pcv.gaussian_blur(color_img, (7, 7), 0)
    name, ext = splitext(imgname)
    pcv.print_image(blurred_img, name + "_Blurred" + ext)

def isolate_from_bg(image_path):
    img, path, filename = pcv.readimage(image_path)
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    mask = pcv.threshold.otsu(gray_img=s, object_type='light')
    masked = pcv.apply_mask(img=img, mask=mask, mask_color='white')
    name, ext = splitext(filename)
    pcv.print_image(masked, name + "_Isolated" + ext)

def pseudolandmarks(image_path):
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
    pcv.print_image(landmark_img, name + '_Pseudolandmarks' + ext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Transformation.py", usage='%(prog)s [path to a picture]')
    parser.add_argument("pic_path")
    args = parser.parse_args()
    pic = args.pic_path
    if (not exists(pic) or not pic.lower().endswith((".jpg", ".jpeg", ".png"))):
        print("Provided argument should be a path to a picture.")
        exit(1)
    threshold_image(pic)
    canny_edge_detection(pic)
    analyze_size_and_shape(pic)
    gaussian_blur(pic)
    pseudolandmarks(pic)
    isolate_from_bg(pic)
