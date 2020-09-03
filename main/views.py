from django.shortcuts import render

import json
# urllib.request to make a request to api
import urllib.request


def index(request):
    if request.method == 'POST':

        city = request.POST['city']
        base = 'http://api.openweathermap.org/data/2.5/weather?q='
        api_key = '&appid=ac7c75b9937a495021393024d0a90c44'
        unit = request.POST['units']


        # source contain json data from api

        source = urllib.request.urlopen(
            base + city + "&units=" + unit + api_key).read()

        # converting json data to dictionary

        list_of_data = json.loads(source)

        if unit == 'metric':
            u = ' C'
        elif unit == 'imperial':
            u = ' F'
        else:
            u = ' K'

        # data for variable list_of_data

        context = {
            'city_name': city,
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": 'Long: ' + str(list_of_data['coord']['lon']) + ' ,Lat : ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + u,
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(context)
    else:
        context = {}
    return render(request, 'main/index.html', context=context)
