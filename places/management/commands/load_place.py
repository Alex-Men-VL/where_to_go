import logging
import os
from urllib.parse import unquote, urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Image, Place


class Command(BaseCommand):
    help = 'Upload data to the site in JSON format'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['urls']:
            response = requests.get(url)
            decoded_place = response.json()
            formatted_place = {
                'title': decoded_place.get('title'),
                'description_short': decoded_place.get('description_short'),
                'description_long': decoded_place.get('description_long'),
                'lng': decoded_place.get('coordinates').get('lng'),
                'lat': decoded_place.get('coordinates').get('lat')
            }
            place, new = Place.objects.get_or_create(**formatted_place)
            if new:
                imgs = decoded_place.get('imgs')
                for number, img_url in enumerate(imgs):
                    response = requests.get(img_url)
                    content = response.content
                    filepath = urlparse(unquote(img_url)).path
                    _, filename = os.path.split(filepath)
                    image = Image(number=number)
                    image.img.save(filename, ContentFile(content), save=False)
                    image.place = place
                    image.save()
                logging.info(
                    f'A place with the title "{place.title}" has been added'
                )
            else:
                logging.info(
                    f'The place with the title "{place.title}" is already in '
                    'the database'
                )
