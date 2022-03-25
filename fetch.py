from zipfile import ZipFile
import requests
from io import IOBase, BytesIO

def _extract_file(f: IOBase, dir: str):
    with ZipFile(f) as zip:
        print('\tExtracting data from zip file...')
        zip.extractall(dir)

def fetch_gtfs(URL: str, dir: str):
    print('Fetching GTFS data...')
    res = requests.get(URL)
    if not res.ok:
        print('Bad request')
        return

    _extract_file(BytesIO(res.content), dir)