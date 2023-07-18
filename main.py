import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "e78aba737f8643d8bf886fd920be0099"

account_sid = "ACf3194b367baf21f930441285af6d8ee1"
auth_token = "216b390622b9210a5cd3c391c32fd007"

weather_params = {
    "lat": 36.162663,
    "lon": -86.781601,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.post(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

# print(weather_data)
# weather_hours = weather_data['hourly'][0]['weather'][0]['id']
# print(weather_hours)

weather_slice = weather_data['hourly'][:12]

for hour_data in weather_slice:
    weather_condition = hour_data['weather'][0]['id']
    if int(weather_condition) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It is going to rain today. Don't forget to take an umbrella!!!",
        from_="+18883781312",
        to="+17015008460"
    )
    print(message.status)