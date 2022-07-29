import requests
import pandas as pd

def get_player_df(name):
    url = "http://129.213.58.231:8000/player/df?&name=" + name
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        print("Error: " + data["error"])
        return None
    else:
        return pd.read_json(data["response"])

def get_all_players_df():
    url = "http://129.213.58.231:8000/all_players_df"
    response = requests.get(url)
    data = response.json()
    if len(data) == 0:
        return None
    else:
        return pd.read_json(data["response"])