import csv
from io import TextIOWrapper
from typing import Callable

def _write_row(writer: TextIOWrapper, row: list):
    writer.write(f'{(",").join(row)}\n')

def _filter_files(filename: str, action: Callable[[TextIOWrapper, TextIOWrapper], None]):
    print(f'\tFiltering through {filename}...')
    with open(filename, 'r') as reader, open(filename, 'r+') as writer:
        action(reader, writer)

def _handle_routes(valid_route_numbers: list, valid_route_ids: list):
    def ret(reader: TextIOWrapper, writer: TextIOWrapper):
        csvreader = csv.reader(reader)
        is_header = True
        for row in csvreader:
            if is_header:
                is_header = False
                _write_row(writer, row)
                continue

            route_id = row[0]
            route_number = row[1]
            if not route_number:
                continue

            # Each element is a string originally
            route_number = int(route_number)
            if route_number in valid_route_numbers:
                _write_row(writer, row)
                valid_route_ids.append(route_id)
        writer.truncate()
    return ret

def _handle_trips(valid_route_ids: list, valid_trip_ids: list, valid_shape_ids: list):
    def ret(reader: TextIOWrapper, writer: TextIOWrapper):
        csvreader = csv.reader(reader)
        is_header = True
        for row in csvreader:
            if is_header:
                is_header = False
                _write_row(writer, row)
                continue
            route_id = row[0]
            if route_id in valid_route_ids:
                trip_id = row[2]
                shape_id = row[8]

                valid_trip_ids.append(trip_id)
                valid_shape_ids.append(shape_id)
                _write_row(writer, row)
        writer.truncate()
    return ret

def _handle_shapes(valid_shape_ids: list):
    def ret(reader: TextIOWrapper, writer: TextIOWrapper):
        csvreader = csv.reader(reader)
        is_header = True
        for row in csvreader:
            if is_header:
                is_header = False
                _write_row(writer, row)
                continue
            shape_id = row[0]
            if shape_id in valid_shape_ids:
                _write_row(writer, row)
        writer.truncate()
    return ret

def _handle_stop_times(valid_trip_ids: list, valid_stop_ids: list):
    def ret(reader: TextIOWrapper, writer: TextIOWrapper):
        csvreader = csv.reader(reader)
        is_header = True
        for row in csvreader:
            if is_header:
                is_header = False
                _write_row(writer, row)
                continue
            trip_id = row[0]
            if trip_id in valid_trip_ids:
                stop_id = row[3]
                valid_stop_ids.append(stop_id)
                _write_row(writer, row)
        writer.truncate()
    return ret

def _handle_stops(valid_stop_ids: list):
    def ret(reader: TextIOWrapper, writer: TextIOWrapper):
        csvreader = csv.reader(reader)
        is_header = True
        for row in csvreader:
            if is_header:
                is_header = False
                _write_row(writer, row)
                continue
            stop_id = row[0]
            if stop_id in valid_stop_ids:
                _write_row(writer, row)
        writer.truncate()
    return ret

def filter_gtfs(dir, valid_route_numbers):
    print('Filtering through GTFS data...')
    valid_route_ids = []
    valid_trip_ids = []
    valid_shape_ids = []
    valid_stop_ids = []
    _filter_files(f'{dir}/routes.txt', _handle_routes(valid_route_numbers, valid_route_ids))
    _filter_files(f'{dir}/trips.txt', _handle_trips(valid_route_ids, valid_trip_ids, valid_shape_ids))
    _filter_files(f'{dir}/shapes.txt', _handle_shapes(valid_shape_ids))
    _filter_files(f'{dir}/stop_times.txt', _handle_stop_times(valid_trip_ids, valid_stop_ids))
    _filter_files(f'{dir}/stops.txt', _handle_stops(valid_stop_ids))