import os
import requests
from twilio.rest import Client

# API_KEY = "8452be5e1d06e33f15820d907ebe6a06"
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
MY_PHONE = os.environ['MY_PHONE']
VIRT_PHONE = os.environ['VIRT_PHONE']

parameters = {
    "q": "Moscow",
    "appid": os.environ.get("API_KEY"),
}

# request weather using "Current Weather Data"
# response = requests.get(url="http://api.openweathermap.org/data/2.5/weather", params=parameters)
# print(response.json())

# request weather using "One call API"

# raining right now:
# lat: -22.701250
# lon: -46.764290
# my place:
# lat: 55.539938
# lon: 37.458260
one_call_params = {
    "lat": -22.701250,
    "lon": -46.764290,
    "exclude": "current,minutely,daily",
    "appid": os.environ.get("API_KEY"),
    "units": "metric",
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=one_call_params)
response.raise_for_status()
weather_data = response.json()

# making slice - get first 12 hours of the forecast
weather_data_sliced = weather_data['hourly'][:12]
twelve_hours_code = []
for hour in range(0, 12):
    twelve_hours_code.append(weather_data_sliced[hour]['weather'][0]['id'])

# checking condition - if weather code < 600 then it will be snow or rain
will_be_rain = False
for code in twelve_hours_code:
    if code < 600:
        will_be_rain = True

# printing result
if will_be_rain:
    # print("will be rain")
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It's going to rain today. Bring an ☂️!",
            from_=VIRT_PHONE,
            to=MY_PHONE,
            )
    print(message.status)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
