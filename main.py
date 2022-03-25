from filter import filter_gtfs
from fetch import fetch_gtfs
import json

def _main():
    # TODO: use TemporaryDirectories
    tmp_directory = 'tmp'

    # TODO: add cmdline args for config path
    config_path = 'config/config.json'

    try:
        f = open(config_path)
        data = json.load(f)
        URL = data['url']
        valid_route_numbers = data['valid_route_numbers']
    except:
        print(f'Invalid config path: {config_path}')
        return

    fetch_gtfs(URL, tmp_directory)
    filter_gtfs(tmp_directory, valid_route_numbers)

if __name__ == '__main__':
    _main()