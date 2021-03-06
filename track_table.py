
import argparse
import os
import glob
import csv
import math
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("tracks_folder")
args = parser.parse_args()


def get_start_date(input_path):
    return datetime.datetime.strptime(os.path.splitext(os.path.basename(input_path))[0], '%Y-%m-%d_%H-%M-%S')


equatorial_circumference = 40075
meridional_circumference = 40009

def get_distance(lat_a, long_a, lat_b, long_b):
    return math.sqrt((((lat_b-lat_a)*(equatorial_circumference/360))**2)+(((long_b-long_a)*(math.cos(((lat_b+lat_a)/2)*math.pi/180))*(meridional_circumference/360))**2))


def get_data(points):

    last_point = next(points)
    total_distance = 0

    for point in points:

        total_distance += get_distance(float(last_point[0]), float(last_point[1]), float(point[0]), float(point[1]))

        last_point = point

    return total_distance*1000, datetime.datetime.fromtimestamp(int(last_point[4])/1000)


def process_track(track_path):
    start_date = get_start_date(track_path)

    with open(track_path) as t:
        track_points = csv.reader(t)
        next(track_points)

        distance, end_date = get_data(track_points)
        if 10000 < distance < 50000:
            print("{},{},{},0{},{:.0f}".format(start_date.strftime("%d/%m/%y"), start_date.strftime("%H:%M:%S"),
                                               end_date.strftime("%H:%M:%S"), (end_date - start_date), distance))


print("Fecha,Inicio,Fin,Tiempo,- / -")
for track in sorted(glob.glob(os.path.join(args.tracks_folder, "*.csv"))):
    process_track(track)
