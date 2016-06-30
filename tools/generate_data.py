#!/usr/bin/env python3

"""
Prepare summary.json for the bench of different JS frameworks.
"""

import os
import json

PROJDIR = os.path.dirname(os.path.dirname(__file__))
COLORS = ("Lavender", "Thistle", "Plum", "Violet",
          "Orchid", "Fuchsia", "MediumOrchid", "MediumPurple",
          "BlueViolet", "DarkViolet", "DarkOrchid", "DarkMagenta",
          "Purple", "Indigo", "SlateBlue", "DarkSlateBlue",
          "MediumSlateBlue")
IMAGES = os.listdir(os.path.join(PROJDIR, "data/images/100_100"))
IMAGES.sort()


def all_files(path="/usr/lib"):
    """
    yield each entry with it's attributes
    """
    image_index = 0
    color_index = 0
    for root, dirs, files in os.walk(path):
        for fil in files:
            full_path = os.path.join(root, fil)
            try:
                stat = os.stat(full_path)
            except FileNotFoundError:
                next
            yield {
                "filename":full_path,
                "size":stat.st_size,
                "uid":stat.st_uid,
                "gid":stat.st_gid,
                "date":stat.st_ctime,
                "color":COLORS[color_index],
                "img":IMAGES[image_index],
            }
            color_index = (color_index + 1) % len(COLORS)
            image_index = (image_index + 1) % len(IMAGES)


def main():
    """
    main
    """
    with open(os.path.join(PROJDIR, "data/summary.json"), "w") as fil:
        fil.write(json.dumps(list(all_files()), indent=1))


if __name__ == "__main__":
    main()
