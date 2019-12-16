import json
import requests

OPENWEATHERMAP_API_KEY = "55d79b326f3720654f6ab31b68231d4a"

class WeatherInfo:
    def __init__(self,city_name, country, temp, wind_speed, wind_deg):
        self.city_name = city_name
        self.country = country
        self.temp_K = temp
        if self.temp_K is not None:
            self.temp_C = round(self.temp_K - 273, 2)
        else:
            self.temp_C = None
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg

    @staticmethod
    def from_json(json_data):
        city_name = json_data['name']
        country_name = json_data ['sys']['country']
        temp = json_data['main']['temp']
        wind_speed = json_data['wind']['speed']
        wind_deg = json_data['wind']['deg']
        weather_info = WeatherInfo(
            city_name, country_name, temp, wind_speed, wind_deg
        )
        return weather_info

def get_weather_data(city_name):
    site_url = "api.openweathermap.org/data/2.5/weather"
    city = f"q={city_name}"
    app_id = f"appid={OPENWEATHERMAP_API_KEY}"


    url=f"https://{site_url}?{city}&{app_id}"
    response = requests.get(url)
    json_data = response.json()
    if json_data['cod'] !=200:
        weather_info = WeatherInfo(city_name, None, None, None, None)
    else:
        weather_info = WeatherInfo.from_json(json_data)
    return weather_info


if __name__ == '__main__':
    weather_data = get_weather_data("London")   # nimmt immer Stadt mit höchster Einwohnerzahl

    print(f"Weather in {weather_data.city_name}")
    print(f"Windspeed {weather_data.wind_speed}")
    print(f"Wind direction {weather_data.wind_deg}°")
    print (f"Temperature {weather_data.temp_K} K ({weather_data.temp_C} °C)")