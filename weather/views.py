from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests

# Create your views here.


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        url = "https://community-open-weather-map.p.rapidapi.com/find"

        querystring = {"q": f"{city}"}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': ""
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        if not response.json()['list']:
            return HttpResponse("<h1>City Not Found</h1>")

        else:
            rain = response.json()['list'][0]['weather'][0]['description']

            speed = response.json()['list'][0]['wind']['speed']

            temp = response.json()['list'][0]['main']['temp']
            temperature = round(temp - 273.15)

            unix_date = response.json()['list'][0]['dt']
            date = datetime.fromtimestamp(unix_date)
            formatted_date = date.strftime('%d-%m-%y')

            return render(request, 'weather/weather.html', {
                "rain": rain,
                "wind_speed": speed,
                "temperature": temperature,
                "date": formatted_date,
                "city": city,
            })

    return render(request, 'weather/index.html')
