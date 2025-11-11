import argparse
from os import listdir
from os.path import join, isdir, isfile
import subprocess
import random

def count_images(directory):
    """Count images in a directory"""
    return len([f for f in listdir(directory) 
                if isfile(join(directory, f)) and f.lower().endswith((".jpg", ".jpeg", ".png"))])

def get_images(directory):
    """Get list of image paths in a directory"""
    return [join(directory, f) for f in listdir(directory) 
            if isfile(join(directory, f)) and f.lower().endswith((".jpg", ".jpeg", ".png"))]

def balance_dataset(root_directory):
    """Balance the number of images across all subdirectories"""
    subdirs = {}
    
    for subdir_name in listdir(root_directory):
        subdir_path = join(root_directory, subdir_name)
        if isdir(subdir_path):
            image_count = count_images(subdir_path)
            subdirs[subdir_path] = image_count
            print(f"{subdir_name}: {image_count} images")
    
    if not subdirs:
        print("No subdirectories found.")
        return
    
    max_count = max(subdirs.values())
    print(f"\nTarget count: {max_count} images per subdirectory")
    
    for subdir_path, current_count in subdirs.items():
        needed = max_count - current_count
        if needed > 0:
            print(f"\n{subdir_path}: need {needed} more images")
            images = get_images(subdir_path)
            
            if not images:
                print(f"  No images to augment in {subdir_path}, skipping...")
                continue
            
            augmentations_per_image = needed // len(images)
            remainder = needed % len(images)
            
            for i, image_path in enumerate(images):
                num_augmentations = augmentations_per_image
                if i < remainder:
                    num_augmentations += 1
                
                if num_augmentations > 0:
                    # print(f"  Creating {num_augmentations} augmentations for {image_path}")
                    try:
                        subprocess.run(
                            ["python", "Augmentation.py", image_path, "-n", str(num_augmentations)],
                            check=True,
                            capture_output=True,
                            text=True
                        )
                    except subprocess.CalledProcessError as e:
                        print(f"  Error augmenting {image_path}: {e}")
                        print(f"  stdout: {e.stdout}")
                        print(f"  stderr: {e.stderr}")
        else:
            print(f"\n{subdir_path}: already balanced ({current_count} images)")
    
    print("\n=== Final counts ===")
    for subdir_name in listdir(root_directory):
        subdir_path = join(root_directory, subdir_name)
        if isdir(subdir_path):
            image_count = count_images(subdir_path)
            print(f"{subdir_name}: {image_count} images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Balance_Dataset.py',
        description='Balance the number of images across subdirectories by creating augmented versions.'
    )
    parser.add_argument("directory", help="Root directory containing subdirectories with images")
    args = parser.parse_args()
    
    balance_dataset(args.directory)
