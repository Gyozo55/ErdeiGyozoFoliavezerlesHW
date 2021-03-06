import time
from datetime import datetime, timedelta

import requests
import json


# 46.912438, 19.692221


def fetch_data(url, querystring):
    headers = {
        'x-api-key': "3cf45bb0481e5c6b574a7f63be5665ec1caff37d66155477581926a9acc7fd15",
        'Content-type': "application/json"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


def temp_to_celsius(temp):
    return round((5 / 9) * (temp - 32))


def result_writer(filename, content):
    file = open(filename, "a")
    file.write(f"{content}\n")
    file.close()


# Weather Current

def current_weather():
    url = "https://api.ambeedata.com/weather/latest/by-lat-lng"
    querystring = {"lat": "46.912438", "lng": "19.692221"}

    response = fetch_data(url, querystring)

    summary_string = json.loads(response.text).get('data').get('summary')
    temperature_in_celsius = temp_to_celsius(int(json.loads(response.text).get('data').get('temperature')))

    result_writer('currentWeathers.txt', f"{datetime.now().strftime('%c')}: {summary_string}, "
                                         f"{str(temperature_in_celsius)} °C")


# Weather Forecast

def forecast_weather():
    url = "https://api.ambeedata.com/weather/forecast/by-lat-lng"
    querystring = {"lat": "46.912438", "lng": "19.692221"}

    response = fetch_data(url, querystring)

    summary_string = json.loads(response.text).get('data').get('forecast')[0].get('summary')
    temperature_in_celsius = temp_to_celsius(int(json.loads(response.text).get('data').get('forecast')[0]
                                                 .get('temperature')))

    result_writer('forecastWeathers.txt', f"{(datetime.now() + timedelta(hours=1)).strftime('%c')}: {summary_string}, "
                                          f"{str(temperature_in_celsius)} °C")


def interval_data_creation():
    while True:
        forecast_weather()
        current_weather()
        time.sleep(300)


if __name__ == '__main__':
    interval_data_creation()
