import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
# "e78aba737f8643d8bf886fd920be0099"
account_sid = "ACf3194b367baf21f930441285af6d8ee1"
auth_token = os.environ.get("AUTH_TOKEN")
# "216b390622b9210a5cd3c391c32fd007"
weather_params = {
    "lat":  36.162663,
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
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https' : os.environ['http_proxy']}

    client = Client(account_sid, auth_token, http_client = proxy_client)
    message = client.messages.create(
        body="It is going to rain today. Don't forget to take an umbrella!!!",
        from_="+18883781312",
        to="+17015008460"
    )
    print(message.status)