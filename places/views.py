import pprint

from django.shortcuts import render
from .models import Place


def index(request):
    places = Place.objects.all()
    locations_features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.coordinate_lng, place.coordinate_lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": "static/places/moscow_legends.json"
            }
        }
        locations_features.append(feature)
    context = {
        'locations': {
            "type": "FeatureCollection",
            "features": locations_features
        }
    }
    pprint.pprint(context, sort_dicts=False)
    return render(request, 'index.html', context=context)
