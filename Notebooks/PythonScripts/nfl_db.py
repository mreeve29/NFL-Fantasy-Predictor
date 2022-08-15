import requests
import pandas as pd

def get_player_info(name):
    url = "https://nfl-fantasy-predictor-db.herokuapp.com/player/info?&name=" + name
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        print("Error: " + data["error"])
        return None
    else:
        return (data["player_name"], data["pos"], data["team"], data["player_id"])


def get_player_df(name):
    url = "https://nfl-fantasy-predictor-db.herokuapp.com/player/df_json?&name=" + name
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        print("Error: " + data["error"])
        return None
    else:
        return (data["player_name"], data["pos"], data["team"], data["player_id"], pd.read_json(data["df"]))

def get_all_players_df():
    url = "https://nfl-fantasy-predictor-db.herokuapp.com/all_players_df_json"
    response = requests.get(url)
    data = response.json()
    if len(data) == 0:
        return None
    else:
        return pd.read_json(data["df"])