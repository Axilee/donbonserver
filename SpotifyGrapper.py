import requests
import json 
import base64

import configparser
config = configparser.ConfigParser()
konfig = config.read("Oauth2/identity.ini")

def getCurrentlyPlaying(oAuthToken):
    #daj input tutaj tokenu ----UWAGA----
    #curl -X "GET" "https://api.spotify.com/v1/me/player/currently-playing" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer BQCxM462V2lEG6WNyFwrXeK80CyzFxYNlZjIw8DAZSZWVLqi7PKwtnytjC-kMGe2G3_Ke5mbtMA9T73mj696at1naASSvSvwb7Ra2zrzc-mcoi3v2IpwSNvePb4ErIOqa1mTyz_H9Oc_b1KcXcWgCO-SJEKNAqVAkuCRvnNKHy2CPTbuPusKM1N4R-SvO0ZJfQ0vij3LLg"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + oAuthToken
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    if response.status_code == 200:

        response_data = json.loads(response.text)
        track_name = response_data['item']['name']
        artist_name = response_data["item"]["album"]["artists"][0]["name"]
        return "Aktualnie leci: " + track_name + " - " + artist_name

    elif response.status_code == 204:
        return "No track currently playing."
    else:
        return 'Error:', response.status_code

# currentlyPlaying = getCurrentlyPlaying(config['SPOTIFY']['access_token']) 
# print(currentlyPlaying)