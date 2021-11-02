from os import listdir
from os.path import isfile, join
from pathlib import Path
import json, os
import requests
from caching import APICaching
import datetime
import click

api_caching = APICaching()



ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PLACE_IMG_PATH = os.path.join(ROOT_DIR,'theme','static','images','places_image')


def write_img_from_gmap_api(place_id, photo_ref):
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key=AIzaSyBxO1khE-LHn5Z5U2SWpA36D4nKqoWzNRg"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    new_file = open(os.path.join(PLACE_IMG_PATH, f'{place_id}photo.jpeg'), 'wb') 
    new_file.write(response.content)


def download_img(api_caching, all_img, data):
    for sup_data in data:
        place_id = sup_data['place_id']
        if not ('photos' in sup_data) or (f'{place_id}photo.jpeg' in all_img):
            continue
        x = datetime.datetime.now()
        out = x.strftime("%d:%m:%y %X")
        print('[' + x.strftime("%d:%m:%y %X")+ ']' + f" {place_id}photo.jpeg has been downloaded")
        photo_ref = sup_data['photos'][0]['photo_reference']
        write_img_from_gmap_api(place_id, photo_ref) 
        api_caching.expire(f'{place_id}photo.jpeg', 168)

def run():
    while True:
        all_cache_file = [f for f in listdir(join(ROOT_DIR,'__cache__')) if isfile(join(join(ROOT_DIR,'__cache__'), f))]
        if not os.path.exists(PLACE_IMG_PATH):
            os.mkdir(PLACE_IMG_PATH)
        all_img = [f for f in listdir(PLACE_IMG_PATH) if isfile(join(PLACE_IMG_PATH, f))]

        for file in all_cache_file:
            if not ('searchresult' in file):
                continue
            data = json.loads(api_caching.get(f'{file[:-6]}'))["results"]
            download_img(api_caching, all_img, data)

@click.group()
def cli():
    pass

@click.command()
def start():
    print("""
    ████████╗ ██████╗░ ░░░░░░ ░█████╗░ ░█████╗░ ░█████╗░ ██╗░░██╗ ██╗ ███╗░░██╗ ░██████╗░
    ╚══██╔══╝ ██╔══██╗ ░░░░░░ ██╔══██╗ ██╔══██╗ ██╔══██╗ ██║░░██║ ██║ ████╗░██║ ██╔════╝░
    ░░░██║░░░ ██████╔╝ █████╗ ██║░░╚═╝ ███████║ ██║░░╚═╝ ███████║ ██║ ██╔██╗██║ ██║░░██╗░
    ░░░██║░░░ ██╔══██╗ ╚════╝ ██║░░██╗ ██╔══██║ ██║░░██╗ ██╔══██║ ██║ ██║╚████║ ██║░░╚██╗
    ░░░██║░░░ ██║░░██║ ░░░░░░ ╚█████╔╝ ██╔══██║ ╚█████╔╝ ██║░░██║ ██║ ██║░╚███║ ╚██████╔╝
    ░░░╚═╝░░░ ╚═╝░░╚═╝ ░░░░░░ ░╚════╝░ ╚═╝░░╚═╝ ░╚════╝░ ╚═╝░░╚═╝ ╚═╝ ╚═╝░░╚══╝╝░╚═════╝░
    version 0.1.0
    """) 
    run()


cli.add_command(start)