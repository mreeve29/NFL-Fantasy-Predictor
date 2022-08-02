from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)


app = FastAPI()

def get_player_stats(name: str):
    engine  = create_engine(DB_URL)
    pos = ""

    with engine.connect() as con:
        res = con.execute("select pos from players where player_name = '" + name + "'")

        all = res.all()
        
        if(len(all) == 0):
            return {"error": "Player not found."}
        else:
            pos = all[0]['pos']
        
        con.close()
    
    table = "qb_stats" if pos == 'qb' else "flex_stats"

    df_json = pd.read_sql_query("select * from " + table + " where player_id in (SELECT player_id from players where player_name = '" + name + "');", engine).drop(columns=['player_id']).to_json(orient='records')

    return {"response": df_json}

def get_all_players_df():
    engine  = create_engine(DB_URL)
    return pd.read_sql_query("select * from players", engine).to_json(orient='records')


@app.get("/player/df")
def player_df(name: str):
    return get_player_stats(name)

@app.get("/all_players_df")
def all_players():
    return { "response": get_all_players_df() }
