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
            except RequestException as err:
                logging.error(f"{err}.\nCan't get data from URL")
            except (IntegrityError, DatabaseError) as err:
                logging.error(f"{err}.\nIncorrect JSON format from URL")
            else:
                place = place_description.get('place')
                if place_description.get('is_new'):
                    imgs = place_description.get('imgs')
                    saved_imgs_number = 0
                    for number, img_url in enumerate(imgs):
                        try:
                            save_place_img(number, url, place)
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
                else:
                    logging.info(
                        f'A place with the title "{place.title}" is already '
                        'in the database'
                    )


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_place(url):
    decoded_place = get_response(url).json()
    formatted_place = {
        'title': decoded_place.get('title'),
        'description_short': decoded_place.get('description_short'),
        'description_long': decoded_place.get('description_long'),
        'lng': decoded_place.get('coordinates').get('lng'),
        'lat': decoded_place.get('coordinates').get('lat')
    }
    place, is_new = Place.objects.get_or_create(**formatted_place)
    imgs = decoded_place.get('imgs')
    place_description = {
        'place': place,
        'is_new': is_new,
        'imgs': imgs
    }
    return place_description


def save_place_img(number, url, place):
    content = get_response(url).content
    filename = get_img_name(url)
    image = Image(number=number)
    image.img.save(filename, ContentFile(content), save=False)
    image.place = place
    image.save()


def get_img_name(url):
    filepath = urlparse(unquote(url)).path
    _, filename = os.path.split(filepath)
    return filename
