
import argparse
import os
import glob
import csv
import math
import datetime
import kml_document
from collections import defaultdict

equatorial_circumference = 40075
meridional_circumference = 40009

def get_distance(lat_a, long_a, lat_b, long_b):
    return math.sqrt(
        (((lat_b-lat_a)*(equatorial_circumference/360))**2)
        +
        (((long_b-long_a)*(math.cos(((lat_b+lat_a)/2)*math.pi/180))*(meridional_circumference/360))**2)
    )

def get_start_date(input_path):
    return datetime.datetime.strptime(os.path.splitext(os.path.basename(input_path))[0], '%Y-%m-%d_%H-%M-%S')

def get_filenames(path):

    year_filenames = defaultdict(list)

    filenames = glob.glob(os.path.join(path, "*.csv"))
    filenames.sort()

    for filename in filenames:
        start_date = get_start_date(filename)
        year_filenames[start_date.year].append({"filename": filename, "start_date": start_date})

    return year_filenames

def get_quarter(date):
    return (date.month-1)//3

def get_line(filename):

    with open(filename["filename"]) as file:
        points = csv.reader(file)
        next(points)
        last_point = next(points)
        total_distance = 0

        line = kml_document.kml_line(filename["start_date"].strftime('%Y-%m-%d %H-%M-%S'), "")
        line.add_coordinate(last_point[1], last_point[0])

        for point in points:

            line.add_coordinate(point[1], point[0])

            total_distance += get_distance(float(last_point[0]), float(last_point[1]), float(point[0]), float(point[1]))

            last_point = point

        line.description = ""

        return line

def get_lines(filenames):

    q1 = kml_document.kml_folder("Q1")
    q2 = kml_document.kml_folder("Q2")
    q3 = kml_document.kml_folder("Q3")
    q4 = kml_document.kml_folder("Q4")
    quarters = [q1, q2, q3, q4]

    for filename in filenames:
        print(filename["filename"])
        quarter = get_quarter(filename["start_date"])
        quarters[quarter].add_child(get_line(filename))

    lines_folder = kml_document.kml_folder("lines")
    lines_folder.add_child(q1)
    lines_folder.add_child(q2)
    lines_folder.add_child(q3)
    lines_folder.add_child(q4)
    return lines_folder

def get_track_points(filename, points, labels):

    with open(filename["filename"]) as file:
        points = csv.reader(file)
        next(points)

        folder = kml_document.kml_folder(filename["start_date"].strftime('%Y-%m-%d %H-%M-%S'))

        for point in points:
            folder.add_child(kml_document.kml_point(point[4], 0, point[1], point[0], False))

        return folder

def get_points(filenames, points, labels):

    q1 = kml_document.kml_folder("Q1")
    q2 = kml_document.kml_folder("Q2")
    q3 = kml_document.kml_folder("Q3")
    q4 = kml_document.kml_folder("Q4")
    quarters = [q1, q2, q3, q4]

    for filename in filenames:
        print(filename["filename"])
        quarter = get_quarter(filename["start_date"])
        quarters[quarter].add_child(get_track_points(filename, points, labels))

    points_folder = kml_document.kml_folder("points")
    points_folder.add_child(q1)
    points_folder.add_child(q2)
    points_folder.add_child(q3)
    points_folder.add_child(q4)
    return points_folder

def main(args):

    os.makedirs(args.output_folder, exist_ok=True)

    filenames = get_filenames(args.tracks_folder)

    for year in filenames:
        print(year)
        document = kml_document.kml_document(year)

        if not args.no_line:
            document.add_child(get_lines(filenames[year]))

        if args.points:
            document.add_child(get_points(filenames[year], args.points, args.labels))

        document.write_to_file(os.path.join(args.output_folder, "{}.kml".format(year)))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("tracks_folder")
    parser.add_argument("output_folder")
    parser.add_argument("--no_line", default=False, action="store_true")
    parser.add_argument("--points", default=None, type=int)
    parser.add_argument("--labels", default=300)

    main(parser.parse_args())