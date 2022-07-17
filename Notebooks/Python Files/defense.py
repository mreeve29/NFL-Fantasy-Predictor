import pandas as pd

# each team is (city, alias) where alias is the name pro-football-reference.com uses in links on their website
# ex. for the cardinals, city is "ARI" and alias is "crd"; full url is "https://www.pro-football-reference.com/teams/crd/2021.htm"
# not all teams will have a different alias for their city
# teams have a different url id when they change names/city (ex. Raiders are "OAK" before 2020 and "LVR" after, which is why "rai" is used for the url)
teams = [
    ("ARI", "crd"),
    ("ATL", "atl"),
    ("BAL", "rav"),
    ("BUF", "buf"),
    ("CAR", "car"),
    ("CHI", "chi"),
    ("CIN", "cin"),
    ("CLE", "cle"),
    ("DAL", "dal"),
    ("DEN", "den"),
    ("DET", "det"),
    ("GNB", "gnb"),
    ("HOU", "htx"),
    ("IND", "clt"),
    ("JAX", "jax"),
    ("KAN", "kan"),
    ("LVR", "rai"),
    ("LAC", "sdg"),
    ("LAR", "ram"),
    ("MIA", "mia"),
    ("MIN", "min"),
    ("NWE", "nwe"),
    ("NOR", "nor"),
    ("NYG", "nyg"),
    ("NYJ", "nyj"),
    ("PHI", "phi"),
    ("PIT", "pit"),
    ("SFO", "sfo"),
    ("SEA", "sea"),
    ("TAM", "tam"),
    ("TEN", "oti"),
    ("WAS", "was")]


def get_defense_year(data, year):
    df_defense_team = pd.DataFrame(columns=["Year", "Games",
                                            "PointsAllowed/G", "YdsAllowed/G", "DefPly/G", "Y/P", "TO/G", "FumGen/G", "1stDsAllowed/G", 
                                            "PassComplete/G", "PassAttempt/G", "PassYdsAllowed/G", "PassTDAllowed/G", "IntGenerated/G", "NetPassYrdAllowed/Attempt", "1stDownPassAllowed/G",
                                            "RushAttempt/G", "RushYdsAllowed/G", "RushTDAllowed/G", "RushYdsAllowed/Attempt", "1stDownRushAllowed/G",
                                            "DriveEndingInScore%", "DriveEndingInTO%"])
    games = 17 if year >= 2021 else 16

    for index,row in data.iterrows():
        df_defense_team.loc[index] = [  year, games, 
                                        row["PF"]/games, row["Yds"]/games, row["Ply"]/games, row["Y/P"], row["TO"]/games, row["FL"]/games, row["1stD"]/games, 
                                        row["Cmp"]/games, row["Att"]/games, row["Yds.1"]/games, row["TD"]/games, row["Int"]/games, row["NY/A"], row["1stD.1"],
                                        row["Att.1"]/games, row["Yds.2"]/games, row["TD.1"]/games, row["Y/A"], row["1stD.2"]/games,
                                        row["Sc%"], row["TO%"]]

    return df_defense_team

def get_all_teams_defense():
    teams_data = {}
    for team in teams:
        teams_data[team[0]] = {}
        for year in range(2020,2022):
            team_url = "https://www.pro-football-reference.com/teams/" + team[1] + "/" + str(year) + ".htm"

            print("Getting data for " + team[0] + " - " + str(year) + " url -> " + team_url + "...")

            df_year = pd.read_html(team_url, header=1)[0].loc[[1]]
            teams_data[team[0]][year] = get_defense_year(df_year, year)
            
    return teams_data