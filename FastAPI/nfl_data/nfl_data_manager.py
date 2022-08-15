import pandas as pd
import os

def player_exists(player_name, df):
    return df[df['player_name'] == player_name].shape[0] > 0

def get_all_players_df():
    df = pd.read_parquet('nfl_data/parquet_files/all_players.parquet')
    return df

def get_player_info(player_name):
    df = get_all_players_df()

    if player_exists(player_name, df):
        player_row = df[df['player_name'] == player_name].iloc[0].values.tolist()
        return (player_row[0], player_row[1], player_row[2], player_row[3])
    else:
        return None

    
def get_player_df(player_name):
    player_info = get_player_info(player_name)

    if player_info is not None:
        pos = player_info[1]
        table = "qb_stats" if pos == 'qb' else "flex_stats"
        df = pd.read_parquet('nfl_data/parquet_files/' + table + '.parquet')

        player_df = df[df['player_id'] == player_info[0]]
        player_df = player_df.reset_index(drop=True)
        return (player_info, player_df)
    else:
        return None