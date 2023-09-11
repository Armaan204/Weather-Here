from django.shortcuts import render
from django.http import JsonResponse
import requests
import os


# Create your views here.
def home(request):
    return render(request, 'index.html')


def get_location_from_ip(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the API error gracefully, you can customize this error message
        return {"error": "Location data not available at the moment."}


def get_weather_from_ip(request):
    ip_address = request.GET.get("ip")
    location = get_location_from_ip(ip_address)

    if "error" in location:
        # Handle the error case
        data = {"weather_data": location["error"]}
    else:
        city = location.get("city")
        country_code = location.get("countryCode")
        weather_data = get_weather_from_location(city, country_code)
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        s = "You're in {}, {}. You can expect {} with a temperature of {} degrees".format(
            city, country_code, description, temperature)
        data = {"weather_data": s}

    return JsonResponse(data)


def get_weather_from_location(city, country_code):
    token = os.environ.get("OPEN_WEATHER_TOKEN")
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}".format(
        city, country_code, token)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the API error gracefully, you can customize this error message
        return {"error": "Weather data not available at the moment."}
