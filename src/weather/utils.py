from datetime import datetime
import geopy
from geopy.geocoders import Nominatim

import openmeteo_requests

import requests_cache
from retry_requests import retry


list_times = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
              '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

def get_coordinates(city: str):


    # Создаем объект геолокатора
    geolocator = Nominatim(user_agent="my_app")

    # Геокодируем адрес
    try:
        location = geolocator.geocode(city)
    except geopy.errors.GeocoderTimedOut:
        print("Ошибка при поиске местоположения")
        return 'Ошибка при поиске местоположения'
    else:
        # Получаем координаты местоположения
        latitude = location.latitude
        longitude = location.longitude
        #print(f"Координаты местоположения: Latitude={latitude}, Longitude={longitude}")
        return latitude, longitude




def get_forecast(lan, lon):


    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lan,
        "longitude": lon,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        'timezone': 'EET'

    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    return hourly_temperature_2m.tolist()


def get_forecast_weather(city):
    coordinates = get_coordinates(city)
    if len(coordinates) == 2:
        res_weather = get_forecast(*coordinates)
        res_weather = list(map(int, res_weather))
        hour_now = datetime.now().hour
        times = list_times[hour_now:] + list_times[:hour_now]
        if len(res_weather) == 24:
            res = list(zip(times, res_weather))
            #print(res)
            return res
        else:
            return [('', 'Произошла ошибка')]
    else:
        return {'res': 'Проверьте название города'}