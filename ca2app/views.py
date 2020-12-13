from django.shortcuts import render
from django.http import JsonResponse
from googleplaces import GooglePlaces, types, lang
from .models import Locations


# # Create your views here.
def updatedb(request):
    try:
        lat = request.POST['lat']
        lon = request.POST['lon']

        location = Locations()
        location.lat = lat
        location.lon = lon
        location.save()
        return JsonResponse({"message": 'Update is a success!'}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

def getLocationType(locationType):
    switcher = {
        'restaurant': types.TYPE_RESTAURANT,
        'cafe': types.TYPE_CAFE,
       
    }
    return switcher.get(locationType, "Invalid Argument")

def updateDiffLocation(request):
	
	API_KEY = 'AIzaSyC1M46s5X-xeLG1zzyq3okXN16TDnpGETE'

	try: 
		requestLocationType = request.POST['type']
		currentLat = float(request.POST['lat'])
		currentLng = float(request.POST['lng'])

		
		lat = []
		lng = []
		names = []
		address = []
		google_places = GooglePlaces(API_KEY)

		if requestLocationType == 'default':
			return

		query_result = google_places.nearby_search(
			lat_lng= {'lat': currentLat, 'lng': currentLng }, keyword="Restaurants",
			radius = 3000, types=[getLocationType(requestLocationType)])


		for place in query_result.places:
			print(place.name)
			place.get_details()
			lat.append(float(place.geo_location['lat']))
			lng.append(float(place.geo_location['lng']))
			names.append(place.name)
			address.append(place.formatted_address)

		return JsonResponse({'names':names, 'lat':lat, 'lng':lng, 'address': address}, status=200,safe=False)
	except Exception as e:
		print(e)
		return JsonResponse({"message": str(e)}, status=400)
