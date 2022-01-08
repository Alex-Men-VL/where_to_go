from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Place


def index(request):
    places = Place.objects.all()
    locations_features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"places/{place.pk}"
            }
        }
        locations_features.append(feature)
    context = {
        'locations': {
            "type": "FeatureCollection",
            "features": locations_features
        }
    }
    return render(request, 'index.html', context=context)


def place_details(request, pk):
    place = get_object_or_404(Place, pk=pk)
    response = {
        'title': place.title,
        'imgs': [image.img.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lat,
        },
    }
    return JsonResponse(response, safe=False,
                        json_dumps_params={'ensure_ascii': False,
                                           'indent': 2})
