from django.http import JsonResponse
import requests
from django.shortcuts import render

def place_text_search(request):
	key = "AIzaSyAFxstV_u9BzDt2H4DWVX66RUAj6RzUF_0"
	query = request.GET.get('query', 'coded')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page = request.GET.get('nextpage')
	if next_page is not None:
		url += "&pagetoken="+next_page

	response = requests.get(url)

	context = {
		"response" : response.json(),
	}

	#return JsonResponse( response.json(), safe=False)
	return render(request, "place_search.html", context)


def place_detail(request):
	key = "AIzaSyAFxstV_u9BzDt2H4DWVX66RUAj6RzUF_0"
	place_id = request.GET.get('place_id', '')
	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)
	map_key = "AIzaSyALXDo2i1g1mQkUXzcbCUnwngjqOS4h3g0"

	response = requests.get(url)
	context ={
	"response": response.json(),
	"map": map_key,
	}
	return render(request, 'place_detail.html', context)
	#return JsonResponse( response.json(), safe=False)

