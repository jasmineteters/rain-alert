import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient


# THIS CODE WILL NOT WORK UNTIL YOU INPUT YOUR API-KEY, ACCOUNT_SID, AUTH_TOKEN, FROM NUMBER AND TO NUMBER
OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = ""

account_sid = {Insert your account sid here}
auth_token = {Insert your auth token here}


weather_params = {
    "lat": 59.616667,
    "lon": -150.033333,
    "appid": api_key,
    "units": "imperial",
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_Endpoint, params=weather_params)
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]



for hour in weather_slice:
    # print(hour["weather"])
    weather_temp = hour["temp"]
    # print(weather_temp)
    weather_code = hour["weather"][0]["id"]
    description = hour["weather"][0]["description"]
    if weather_code <= 700:
        will_rain = True
        sunshine = False
    elif weather_temp >= 75:
        sunshine = True
        will_rain = False
        # print(f"Bring sunscreen if you go outsite, it'll be {weather_temp} today! ☀️")
    else:
        will_rain = False
        sunshine = False
        # print("no update")

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's going to rain today, bring an umbrella ☂️",
        from_={your twilio number here},
        to= {your verified number here}
    )
    print(message.status)
elif sunshine:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="Bring sunscreen if you go outsite, it'll be {weather_temp} today! ☀️",
        from_={your twilio number here},
        to= {your verified number here}
    )
    print(message.status)



