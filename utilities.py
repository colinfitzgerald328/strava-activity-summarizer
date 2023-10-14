import requests
import os 
from datetime import datetime
import json

os.environ["access_token"] = "<access_token>"
os.environ["refresh_token"] = "<refresh_token>"

def check_token_status(access_token):
  url = "https://www.strava.com/api/v3/athlete/activities"
  access_token = os.environ["access_token"]
  headers = {
      "Authorization": f"Bearer {access_token}"
  }
  resp = requests.get(url, headers=headers)
  return resp.status_code == 200
    
# refreshes the access token 
def refresh_failed_token(refresh_token):
    url = "https://www.strava.com/api/v3/oauth/token"
    params = {
        "client_id": "<client_id>", 
        "client_secret": "<client_secret>",
        "grant_type": "refresh_token", 
        "refresh_token": refresh_token
    }
    resp = requests.post(url, params=params)
    json = resp.json()
    return json["access_token"]

# checks the status of the current token and updates when needed 
def generate_new_token_if_necessary():
    current_token_validity = check_token_status(os.environ.get("access_token"))
    if not current_token_validity: 
        new_token = refresh_failed_token(os.environ.get("refresh_token"))
        os.environ["access_token"] = new_token


def iso_to_unix_timestamp(iso_timestamp):
  try:
      dt = datetime.strptime(iso_timestamp, '%Y-%m-%dT%H:%M:%SZ')
      return int(dt.timestamp())
  except ValueError:
      return None


def get_weather_string_for_values(lat, lon, last_activity_timestamp):
  url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
  params = {
      "lat": lat, 
      "lon": lon, 
      "dt": last_activity_timestamp, 
      "appid": "<api_key>", 
      "units": "imperial"
  }
  resp = requests.get(url, params=params)
  json = resp.json()
  cleaned = json["data"][0]
  weather_deg = int(cleaned["temp"])
  cloud_percent = int(cleaned["clouds"])
  humidity = int(cleaned["humidity"])
  description = cleaned["weather"][0]["description"].capitalize()
  return f"Weather: {description}, {weather_deg} degrees, {cloud_percent}% Clouds, {humidity}% Humidity"

def get_key_metrics_string_for_values(average_cadence, average_watts, max_watts, kilojoules):
  key_metrics_string = f"Quick Summary: {average_cadence} SPM, {average_watts} watts (avg), {max_watts} watts (max), [{kilojoules} kJ of work]"
  return key_metrics_string


def get_activity_by_id(activity_id):
  access_token = os.environ["access_token"]
  url = f"https://www.strava.com/api/v3/activities/{activity_id}"
  headers = {
      "Authorization": f"Bearer {access_token}"
  }

  resp = requests.get(url, headers=headers)
  return resp.json()


def generate_clean_activity_json(activity_id):
  activity = get_activity_by_id(activity_id)
  cleaned_dict = []
  cleaned_dict.append({
      "lat": activity["start_latlng"][0], 
      "lon": activity["start_latlng"][1], 
      "last_activity_timestamp": iso_to_unix_timestamp(activity["start_date"]), 
      "average_cadence": int(activity["average_cadence"]) if activity.get("average_cadence") else None,
      "average_watts": int(activity["average_watts"]) if activity.get("average_watts") else None, 
      "max_watts": int(activity["max_watts"]) if activity.get("max_watts") else None, 
      "kilojoules": int(activity["kilojoules"]) if activity.get("kilojoules") else None,  
      "activity_type": activity["sport_type"], 
      "activity_id": activity["id"]
  })
  return cleaned_dict


def update_activity(activity_id):
  generate_new_token_if_necessary()
  access_token = os.environ["access_token"]
  json_data = generate_clean_activity_json(activity_id)[0]
  weather_string = get_weather_string_for_values(json_data["lat"], json_data["lon"], json_data["last_activity_timestamp"])
  summary_string = ""
  if json_data["activity_type"] == "Run": 
      summary_string = get_key_metrics_string_for_values(json_data["average_cadence"], json_data["average_watts"], json_data["max_watts"], json_data["kilojoules"])

  description = weather_string + "\n\n" + summary_string
  headers = {
      "Authorization": f"Bearer {access_token}"
  }
  url = f'https://www.strava.com/api/v3/activities/{json_data["activity_id"]}'
  data = {
      "description": description
  }
  requests.put(url, headers=headers, json=data)