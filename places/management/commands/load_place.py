import logging
import os
from urllib.parse import unquote, urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError
from requests.exceptions import InvalidURL, RequestException

from places.models import Image, Place


class Command(BaseCommand):
    help = 'Upload data to the site in JSON format'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['urls']:
            try:
                place_description = save_place(url)
            except InvalidURL as err:
                logging.error(f"{err}.\nError in the URL")
                continue
            except RequestException as err:
                logging.error(f"{err}.\nCan't get data from URL")
                continue
            except (IntegrityError, DatabaseError, KeyError) as err:
                logging.error(f"{err}.\nIncorrect JSON format from URL")
                continue

            place = place_description['place']
            if not place_description['is_new']:
                logging.info(
                    f'A place with the title "{place.title}" is already '
                    'in the database'
                )
                continue

            imgs = place_description['imgs']
            saved_imgs_number = 0
            for number, img_url in enumerate(imgs):
                try:
                    save_place_img(number, img_url, place)
                except RequestException as err:
                    logging.error(
                        f"{err}.\nImage not added"
                    )
                else:
                    saved_imgs_number += 1
            logging.info(
                f'A place with the title "{place.title}" has been added'
                f'\nNumber of saved images: {saved_imgs_number} out of '
                f'{number+1}'
            )


def save_place(url):
    response = requests.get(url)
    response.raise_for_status()

    decoded_place = response.json()
    formatted_place = {
        'title': decoded_place['title'],
        'description_short': decoded_place['description_short'],
        'description_long': decoded_place['description_long'],
        'lng': decoded_place['coordinates']['lng'],
        'lat': decoded_place['coordinates']['lat']
    }
    place, is_new = Place.objects.get_or_create(**formatted_place)
    imgs = decoded_place.get('imgs') or []
    place_description = {
        'place': place,
        'is_new': is_new,
        'imgs': imgs
    }
    return place_description


def save_place_img(number, url, place):
    response = requests.get(url)
    response.raise_for_status()

    content = response.content
    filename = get_img_name(url)
    image = Image(number=number)
    image.img.save(filename, ContentFile(content), save=False)
    image.place = place
    image.save()


def get_img_name(url):
    filepath = urlparse(unquote(url)).path
    _, filename = os.path.split(filepath)
    return filename
