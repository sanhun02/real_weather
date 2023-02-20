import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def main_weather(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=ac85cb521fdac09d2ce6ee9f496e0879&units=imperial'
    msg = ''
    msg_class = ''

    if request.method != 'POST':
        city = 'DALLAS'
        form = CityForm()
        r = requests.get(url.format(city)).json()

    elif 'city-input' in request.POST and request.POST['city-input'] != '':
        city = request.POST['city-input'].upper()
        form = CityForm()
        r = requests.get(url.format(city)).json()

        if r['cod'] != 200:
            msg = "City doesn't exist"
            msg_class = 'not-exist'
            city = request.POST['current-city'].upper()
            r = requests.get(url.format(city)).json()

    elif 'city-input' in request.POST and request.POST['city-input'] == '' and \
                                                    'name' not in request.POST:
        city = request.POST['current-city'].upper()
        form = CityForm()
        r = requests.get(url.format(city)).json()

        if r['cod'] != 200:
            msg = "City doesn't exist"
            msg_class = 'not-exist'
            city = request.POST['current-city'].upper()
            r = requests.get(url.format(city)).json()

    elif 'name' in request.POST and request.POST['current-city'] != '':
        city = request.POST['current-city'].upper()
        form = CityForm(request.POST)
        form.set_city(city)
        r = requests.get(url.format(city)).json()

        if form.is_valid():
            add_city = form.cleaned_data['name'].upper()
            existing_count = City.objects.filter(name=add_city).count()

            if existing_count == 0:
                r = requests.get(url.format(add_city)).json()

                if r['cod'] == 200:
                    form.save()
                    msg = 'City added to watchlist'
                    msg_class = 'exist'

            else:
                msg = 'City already in watchlist'
                msg_class = 'not-exist'
                city = request.POST['current-city'].upper()
                r = requests.get(url.format(city)).json()


    city_data = {
                    'city' : city,
                    'temp' : round(r['main']['temp']),
                    'descr' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                    'feels_like' : round(r['main']['feels_like']),
                    'humidity' : r['main']['humidity']
                }

    cities = City.objects.all()

    cities_data = []

    for list_city in cities:
            r = requests.get(url.format(list_city)).json()

            weather_data = {
                        'city' : list_city.name.upper(), 
                        'temp' : round(r['main']['temp']),
                        'descr' : r['weather'][0]['main'],
                        'icon' : r['weather'][0]['icon']
                    }

            cities_data.append(weather_data)

    form = CityForm(initial={'name' : 'Add to Watchlist'})

    context = {
                'cities_data' : cities_data,
                'form' : form,
                'city_data' : city_data,
                'msg' : msg,
                'msg_class' : msg_class
        }

    return render(request, 'weather_app/weather_app.html', context)


def delete_from_watchlist(request, city):
    City.objects.get(name=city).delete()

    return redirect('main_weather')


def go_to_detailed_weather(request, city):
    url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid=ac85cb521fdac09d2ce6ee9f496e0879&units=imperial&cnt=5'
    msg = ''
    msg_class = ''

    if request.method != 'POST':
        r = requests.get(url.format(city)).json()

    elif request.POST['input'] != '':
        city = request.POST['input']
        r = requests.get(url.format(city)).json()

        if r['cod'] != '200':
            msg = "City doesn't exist"
            msg_class = 'not-exist'
            city = request.POST['current-city'].upper()
            r = requests.get(url.format(city)).json()
        
    else:
        city = request.POST['current-city']
        r = requests.get(url.format(city)).json()

        if r['cod'] != '200':
            msg = "City doesn't exist"
            msg_class = 'not-exist'
            city = request.POST['current-city'].upper()
            r = requests.get(url.format(city)).json()


    detail_data = {
                    'city' : city,
                    'temp' : round(r['list'][0]['main']['temp']),
                    'icon' : r['list'][0]['weather'][0]['icon'],
                    'descr' : r['list'][0]['weather'][0]['description'],
                    'wind' : r['list'][0]['wind']['speed'],
                    'feels_like' : round(r['list'][0]['main']['feels_like']),
                    'humidity' : r['list'][0]['main']['humidity'],
                    'preci' : r['list'][0]['pop']
                }

    forecast_data = []
    days = ['Today', 'Tommorow', '2 Days Away', '3 Days Away', '4 Days Away']

    for i in range(5):
                date = days[i]

                forecast = {
                    'date' : date,
                    'temp' : round(r['list'][i]['main']['temp']),
                    'icon' : r['list'][i]['weather'][0]['icon'],
                    'descr' : r['list'][i]['weather'][0]['main'],
                }

                forecast_data.append(forecast)

    context = {
                'detail_data' : detail_data,
                'forecast_data' : forecast_data,
                'msg' : msg,
                'msg_class' : msg_class
            }

    return render(request, 'weather_app/detailed_weather.html', context)