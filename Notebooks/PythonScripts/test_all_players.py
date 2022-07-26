import players

all_players = players.get_all_fantasy_players()

count = 0
for player,pos in all_players:
    print("[" + str(count) + "] Processing " + player)
    players.get_player_df(player, pos, 2020)
    print("[" + str(count) + "]  Processed " + player)
    count += 1

print("Total Players Processed: " + str(count))
print("Total Players: " + str(len(all_players)))