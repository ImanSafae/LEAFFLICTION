from sys import argv
from os import listdir
from os.path import isfile, join, exists, isdir
import matplotlib
matplotlib.use('TkAgg')  # Configurer le backend
import matplotlib.pyplot as plt


def analyze_subdirectories(directory):
    subdirectories = {}
    for subdir in listdir(directory):
        subpath = (join(directory, subdir))
        if isdir(subpath):
            contained_pics = [
                pic
                for pic in listdir(subpath)
                if isfile(join(subpath, pic))
                and pic.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            subdirectories[subdir] = len(contained_pics)
    return subdirectories


def plot_distribution(subdirectories, directory):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # 1 ligne, 2 colonnes
    values = list(subdirectories.values()) # number of pics in the folder
    labels = list(subdirectories.keys()) # name of the folder
    if not values:
        print("No subdirectories to plot")
    else:
        if sum(values) == 0:
            print("Found subdirectories but no images to plot")
        else:
            axes[0].pie(values, labels=labels, autopct='%1.1f%%')
            # axes[0].set_title(directory)
            
            axes[1].bar(labels, values)
            # axes[1].set_title(directory)
            axes[1].set_xlabel('Folders')
            axes[1].set_ylabel('Number of Images')
            
            plt.title(directory)
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Please call with one argument which should be a directory.")
        exit(1)
    directory = argv[1]
    if not exists(directory):
        print(f"The directory {directory} does not exist.")
        exit(1)
    subdirectories = analyze_subdirectories(directory)
    plot_distribution(subdirectories, directory)
