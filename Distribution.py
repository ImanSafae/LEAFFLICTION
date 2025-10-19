from sys import argv
from os import listdir
from os.path import isfile, join, exists, isdir
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


def plot_distribution(subdirectories):
    fig, ax = plt.subplots()
    values = list(subdirectories.values())
    labels = list(subdirectories.keys())
    if not values:
        print("No subdirectories to plot")
    else:
        if sum(values) == 0:
            print("Found subdirectories but no images to plot")
        else:
            ax.pie(values, labels=labels)
            plt.show()
    if not values:
        print("No subdirectories to plot")
    else:
        if sum(values) == 0:
            print("Found subdirectories but no images to plot")
        else:
            ax.pie(values, labels=labels)
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
    plot_distribution(subdirectories)
