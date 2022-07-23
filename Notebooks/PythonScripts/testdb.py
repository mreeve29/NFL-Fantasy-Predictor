from pymongo import MongoClient
import pandas as pd
import players as players
uri = "mongodb+srv://nfl-data.cgmvb2j.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../../../nfl-data-key.pem')
db = client['nfl-data']


all_players = players.get_all_fantasy_players()
for player,pos in all_players:
    player_df = players.get_player_df(player, 2020)
    old_games = []
    current_season_games = []

    if pos == "wr" or pos == "te":
        old_games = players.get_rec_df(player_df)
    elif pos == "qb":
        old_games = players.get_qb_df(player_df)
    elif pos == "rb":
        old_games = players.get_rb_df(player_df)

    print(player)
    print(old_games.to_dict())
    # db.players.insert_one({"_fts": player , "pos" : pos, "old_games" : old_games.to_dict(), "current_season_games" : []})
    db.players.insert_many(old_games.to_dict("records"))


# _fts ex. KuppCo00 
# pos ex. wr
# old_games ex. []
# current_season_games ex. []

# db.players.update_one({"_fts" : "KuppCo00", "pos" : "wr", "games" : []})