import requests
from datetime import datetime
import pytz
import pandas
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv("weather_api_key")
"""https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/
[location]/[date1]/[date2]?key=YOUR_API_KEY """




def get_weather_url(location=None, start_date=None, end_date=None, latitude=None, longitude=None):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    if location:
        location_date = f"{location}/{start_date}/{end_date}"
    else:
        location_date = f"{latitude},{longitude}/{start_date}/{end_date}"
    params = (
        f"?key={API_KEY}"
        f"&unitGroup=metric"
        f"&include=hours"
        f"&elements=cloudcover,description,feelslike,precip,humidity,conditions,datetime,snow"
    )
    return f"{base_url}{location_date}{params}"




def filter_forecast_data(forecast_data):
    filtered_data = {key: forecast_data[key] for key in forecast_data if key != 'days'}  # Copy all fields except 'days'
    filtered_data['days'] = []  # Initialize an empty list for the filtered days
    for day in forecast_data['days']:
        filtered_day = {key: day[key] for key in day if key != 'hours'}
        filtered_hours = []
        for hour_data in day['hours']:
            hour_datetime = datetime.strptime(hour_data['datetime'], '%H:%M:%S')
            hour = hour_datetime.hour
            accepted_values = {8, 10, 12, 14, 18, 20}
            if hour in accepted_values:
                filtered_hours.append({
                    "time": f"{hour}:00",
                    "feelslike": hour_data['feelslike'],
                    "humidity": hour_data['humidity'],
                    "precip": hour_data['precip'],
                    "snow": hour_data['snow'],
                    "cloudcover": hour_data['cloudcover'],
                    "conditions": hour_data['conditions']
                })
        filtered_day['hours'] = filtered_hours  # Add the filtered hours to the filtered_day
        filtered_day = {key: filtered_day[key] for key in filtered_day if key == 'hours' or key == "datetime"}
        filtered_data['days'].append(filtered_day)  # Add the filtered_day to the filtered_data
    return filtered_data['days']




def forecast_between_dates_location(location, start_date, end_date):
    URL = get_weather_url(location=location, start_date=start_date, end_date=end_date)
    response = requests.get(URL)
    if response.status_code == 200:
        forecast_data = response.json()
        return filter_forecast_data(forecast_data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None




def forecast_between_dates_coordinates(longitude, latitude, start_date, end_date):
    URL = get_weather_url(start_date=start_date, end_date=end_date, latitude=latitude, longitude=longitude)
    response = requests.get(URL)
    if response.status_code == 200:
        forecast_data = response.json()
        return filter_forecast_data(forecast_data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


def good_weather(days_data):
    total_hours = 1
    good_hours = 0
    for day in days_data:
        for hour in day['hours']:
            total_hours += 1
            feelslike = hour.get('feelslike', None)
            humidity = hour.get('humidity', None)
            precip = hour.get('precip', None)
            snow = hour.get('snow', None)
            conditions = hour.get('conditions', None)
            good_feelslike = feelslike is not None and -10 <= feelslike <= 25
            good_humidity = humidity is not None and humidity <= 90
            good_precip = precip is None or precip <= 2
            good_snow = snow is None or snow < 1
            good_conditions = conditions is not None and conditions.lower() not in ["Rain","Snow"]
            if good_feelslike and good_humidity and good_precip and good_snow and good_conditions:
                good_hours += 1
    return good_hours / total_hours >= 0.75



"""
Gives forecast for only days(Much simpler than main one
"""
def forecast_between_dates_coordinates_days(latitude, longitude, start_date, end_date):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    coordinates_date = f"{latitude},{longitude}/{start_date}/{end_date}"
    params = (
        f"?key={API_KEY}"
        f"&unitGroup=metric"
        f"&include=days"
        f"&elements=cloudcover,description,feelslike,precip,humidity"
    )
    URL = f"{base_url}{coordinates_date}{params}"
    response = requests.get(URL)
    # Check for a valid response
    if response.status_code == 200:
        # Parse the JSON response
        forecast_data = response.json()
        return forecast_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

"""
print("The names and the order of keys in the returned list's dictionaries")
print()
location = "Glasgow, UK"
start_date = "2023-11-01"
end_date = "2023-11-03"
output = forecast_between_dates_location(location, start_date, end_date)
print(json.dumps(output, indent=4))
print(good_weather(output))
"""


