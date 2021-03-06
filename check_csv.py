
import argparse
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument("tracks_folder")
args = parser.parse_args()


for track in glob.glob(os.path.join(args.tracks_folder, "*.csv")):
    with open(track) as t:
        lines = t.readlines()
        if len(lines) < 2:
            print(track)
            continue

        sp = lines[-1].split(",")
        if len(sp) != 5:
            print(track)
            continue

        ts = sp[4]
        if len(ts) != 14:
            print(track)
            continue

        if not ts[:-1].isdigit():
            print(track)
