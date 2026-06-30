import os
import requests

API_KEY = os.environ.get("LIQUIPEDIA_API_KEY")
BASE_URL = "https://api.liquipedia.net/api/v3/match"

headers = {
    "Authorization": f"Apikey {API_KEY}"
}

params = {
    "wiki": "rocketleague",
    "limit": 5
}

response = requests.get(BASE_URL, headers=headers, params=params)

print("Status code:", response.status_code)
print(response.json())