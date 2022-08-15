from fastapi import FastAPI
import pandas as pd
import nfl_data.nfl_data_manager as ndm


app = FastAPI()


@app.get("/player/info")
def player_info(name: str):
    info = ndm.get_player_info(name)
    if info is not None:
        return {
            "player_name": info[3], 
            "pos": info[1], 
            "team": info[2], 
            "player_id": info[0]
            }
    else:
        return {"error": "Player not found"}

@app.get("/player/df_json")
def player_df(name: str):
    player_info_df = ndm.get_player_df(name)
    if player_info_df is not None:
        info = player_info_df[0]
        df = player_info_df[1]
        return {
            "player_name": info[3], 
            "pos": info[1], 
            "team": info[2], 
            "player_id": info[0], 
            "df": df.to_json()
            }
    else:
        return {"error": "Player not found"}

@app.get("/player/df_html")
def player_df(name: str):
    player_info_df = ndm.get_player_df(name)
    if player_info_df is not None:
        info = player_info_df[0]
        df = player_info_df[1]
        return {
            "player_name": info[3], 
            "pos": info[1], 
            "team": info[2], 
            "player_id": info[0], 
            "df": df.html()
            }
    else:
        return {"error": "Player not found"}

@app.get("/all_players_df_json")
def all_players():
    return {"df" : ndm.get_all_players_df().to_json() }

@app.get("/all_players_df_html")
def all_players():
    return {"df" : ndm.get_all_players_df().to_html() }
