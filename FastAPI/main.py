from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB_URL)

base = declarative_base()
base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    try:
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        yield db
    finally:
        db.close()


def get_player_df(name: str, db: Session = Depends(get_db)):
    metadata = MetaData(engine)

    players = Table('players', metadata, autoload=True, autoload_with=engine)

    pquery = select([players.columns.player_id, players.columns.pos]).where(players.columns.player_name == name)

    result = db.execute(pquery)

    res_set = result.fetchall()

    if len(res_set) == 0:
        return None

    player_id = res_set[0][0]
    pos = res_set[0][1]
    
    table = "qb_stats" if pos == 'qb' else "flex_stats"

    stat_table = Table(table, metadata, autoload=True, autoload_with=engine)

    stat_query = select([stat_table]).where(stat_table.columns.player_id == player_id)



    return pd.read_sql_query(stat_query, db).drop(columns=['player_id'])
    
def get_all_players_df(db: Session = Depends(get_db)):
    metadata = MetaData(engine)

    players = Table('players', metadata, autoload=True, autoload_with=engine)

    players_query = select([players])



    return pd.read_sql_query(players_query, db).drop(columns=['player_id'])


@app.get("/player/df_json")
def player_df(name: str):
    df = get_player_df(name)
    if df is None:
        return { "error": "Player not found" }
    
    return {
        "player_name": name,
        "response" : df.to_json(orient='records') 
        }

@app.get("/player/df_html")
def player_df(name: str):
    df = get_player_df(name)
    if df is None:
        return { "error": "Player not found" }
    
    return { 
        "player_name": name,
        "response" : df.to_html() 
        }

@app.get("/all_players_df_json")
def all_players():
    return { "response": get_all_players_df().to_json(orient='records') }

@app.get("/all_players_df_html")
def all_players():
    return { "response": get_all_players_df().to_html() }
