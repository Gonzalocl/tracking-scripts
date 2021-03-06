
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("tracks_folder")
args = parser.parse_args()

remove_last_line = []

remove_file = []

for filename in remove_last_line:
    print(filename)
    with open(os.path.join(args.tracks_folder, filename), "r+") as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell() - 1
        while pos > 0 and f.read(1) != "\n":
            pos -= 1
            f.seek(pos, os.SEEK_SET)
        if pos > 0:
            f.seek(pos, os.SEEK_SET)
            f.truncate()

for filename in remove_file:
    print(filename)
    if os.path.exists(os.path.join(args.tracks_folder, filename)):
        os.remove(os.path.join(args.tracks_folder, filename))


