
import argparse
import os
import glob
import csv
import math
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("tracks_folder")
parser.add_argument("output_folder")
args = parser.parse_args()


def get_start_date(input_path):
    return datetime.datetime.strptime(os.path.splitext(os.path.basename(input_path))[0], '%Y-%m-%d_%H-%M-%S')


def get_output_path(input_path, output_folder):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_folder, "{}.kml".format(filename))


equatorial_circumference = 40075
meridional_circumference = 40009


def get_distance(lat_a, long_a, lat_b, long_b):
    return math.sqrt((((lat_b-lat_a)*(equatorial_circumference/360))**2)+(((long_b-long_a)*(math.cos(((lat_b+lat_a)/2)*math.pi/180))*(meridional_circumference/360))**2))


def get_data(points):

    last_point = next(points)
    coordinates = "{},{},0\n".format(last_point[1], last_point[0])
    total_distance = 0

    for point in points:

        coordinates += "{},{},0\n".format(point[1], point[0])

        total_distance += get_distance(float(last_point[0]), float(last_point[1]), float(point[0]), float(point[1]))

        last_point = point

    return coordinates, total_distance*1000, datetime.datetime.fromtimestamp(int(last_point[4])/1000)


template_kml_document = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Document>{}</Document></kml>'
template_track_description = '<name>{}</name><Style id="sty"><LineStyle><color>ffffff55</color><width>2</width></LineStyle></Style><Placemark><name>{}</name><description><![CDATA[{}]]></description><styleUrl>#sty</styleUrl>{}</Placemark>'
template_description = '<html><body style="white-space: nowrap">Fecha: {} de {} a {}<br>Tiempo: {}<br>Distancia: {:.0f} m</body></html>'
template_line = '<LineString><coordinates>{}</coordinates></LineString>'


def print_kml(output_file, start_date, end_date, total_distance, coordinates):

    title_str = start_date.strftime('%Y-%m-%d %H-%M-%S')
    date_str = start_date.strftime('%Y-%m-%d')
    start_time_str = start_date.strftime('%H:%M:%S')
    end_time_str = end_date.strftime('%H:%M:%S')
    duration = end_date - start_date
    duration_str = str(duration)

    description_str = template_description.format(date_str, start_time_str, end_time_str, duration_str, total_distance)
    line_str = template_line.format(coordinates)
    track_description_str = template_track_description.format(title_str, title_str, description_str, line_str)
    kml_document_str = template_kml_document.format(track_description_str)

    print(kml_document_str, file=output_file)


def process_track(track_path):
    output_path = get_output_path(track_path, args.output_folder)
    start_date = get_start_date(track_path)

    with open(track_path) as t, open(output_path, "w") as t_out:
        track_points = csv.reader(t)
        next(track_points)

        coordinates_str, distance, end_date = get_data(track_points)

        print_kml(t_out, start_date, end_date, distance, coordinates_str)


os.makedirs(args.output_folder, exist_ok=True)
for track in glob.glob(os.path.join(args.tracks_folder, "*.csv")):
    print(track)
    process_track(track)
