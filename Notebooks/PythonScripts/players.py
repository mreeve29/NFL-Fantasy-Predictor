import matplotlib.pyplot as plt
import pandas as pd
import datetime

import re
import requests
from bs4 import BeautifulSoup


def get_all_fantasy_players():        
    res = requests.get("https://www.pro-football-reference.com/years/2021/fantasy.htm")
    soup = BeautifulSoup(res.text,features='html.parser')

    tbody = soup.find_all("tbody")[-1]

    usernames = []

    for tr in tbody.find_all("tr"):
        if(tr.get("class") is not None and tr.get("class")[0] == "thead"):
            continue
        first = tr.td
        a = first.a
        pos = first.next_sibling.next_sibling.text.lower()
        if(pos != ""):
            username = re.search("\/(.{6}\d{2}).htm", a.get("href")).group(1)
            usernames.append((username, pos))

    return usernames


def get_headers(html):
    soup = BeautifulSoup(html,features='html.parser')
    thead = soup.find_all("thead")[0]
    ths = thead.tr.findChildren()
    
    headers = []
    col_index = 0
    for th in ths:
        start_index = col_index
        
        if(th.get("colspan") is not None):
            col_index = col_index + int(th.get("colspan"))
        else:
            col_index = col_index + 1

        if(th.text != ''):
            headers.append((th.text, start_index, col_index))
    return headers

def get_player_df(username, pos, startYear):
    url = "https://www.pro-football-reference.com/players/K/" + username + "/gamelog/"
    res = requests.get(url)

    df = pd.read_html(res.text, header=1)[0]
    df = df.head(df.shape[0] - 1)

    df = df[df['Age'].notnull()]

    # These lines may not be necessary because of the previous line
    df = df[df['Date'] != "Date"]
    df = df[df['GS'] != "Did Not Play"]
    df = df[df['GS'] != "Inactive"]
    df = df[df['GS'] != "Injured Reserve"]
    df = df[df['GS'] != "COVID-19 List"]
    df = df[df['GS'] != "Suspended"]

    df.drop(columns=["GS"])
    df = df[df['Year'].astype(int) >= startYear]

    df = df.reset_index(drop=True).fillna(0)

    headers = get_headers(res.text)

    if pos.lower() == 'qb':
        return get_qb_df(df, headers)
    else :
        return get_flex_df(df, headers)


def get_flex_df(df, headers):
    df_flex = pd.DataFrame(columns=['Year','Date','Week','Team','Opp','Location',
                                   'Tgt','Rec','RecYd','RecYd/Rec','RecYd/Tgt','Catch%','RecTD',
                                   'RushAtt','RushYd','RushYd/Att','RushTD',
                                   'OffSnapCount','OffSnap%'
                                ])

    # Add common columns
    df_flex["Year"] = df["Year"]
    df_flex["Date"] = df["Date"]
    df_flex["Week"] = df["Week"]
    df_flex["Team"] = df["Tm"]
    df_flex["Opp"] = df["Opp"]
    df_flex["Location"] = df["Unnamed: 7"].apply(lambda x: "A" if x == "@" else "H")



    for header, start, end in headers:
        if header.lower() == "receiving":
            receiving_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))

            df_flex["Tgt"] = receiving_df["Tgt"].astype(int)
            df_flex["Rec"] = receiving_df["Rec"].astype(int)
            df_flex["RecYd"] = receiving_df["Yds"].astype(int)
            df_flex["RecYd/Rec"] = receiving_df["Y/R"].astype(float)
            df_flex["RecYd/Tgt"] = receiving_df["Y/Tgt"].astype(float)
            df_flex["Catch%"] = receiving_df["Ctch%"].apply(lambda x: float(x) if isinstance(x, int) else float(x.replace("%", "")))
            df_flex["RecTD"] = receiving_df["TD"].astype(int)

        elif header.lower() == "rushing":
            rush_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))

            df_flex["RushAtt"] = rush_df["Att"].astype(int)
            df_flex["RushYd"] = rush_df["Yds"].astype(int)
            df_flex["RushYd/Att"] = rush_df["Y/A"].astype(float)
            df_flex["RushTD"] = rush_df["TD"].astype(int)

        elif header.lower() == "off. snaps":
            snap_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))

            df_flex["OffSnapCount"] = snap_df["Num"].astype(int)
            df_flex["OffSnap%"] = snap_df["Pct"].apply(lambda x: float(x) if isinstance(x, int) else float(x.replace("%", "")))
            
    return df_flex.fillna(0)

# Adjusted Yards per pass attempt: (PassingYds + 20PassTD - 45Int)/(Passes attempted)
def get_qb_df(df, headers):
    df_qb = pd.DataFrame(columns=['Year','Date','Week','Team','Opp','Location',
                                    'Cmp','PassAtt','Cmp%','PassYds','PassTD','Int','QBRating','Sacks','PassYd/Att','AdjPassYd/Att',
                                    'RushAtt','RushYd','RushYd/Att','RushTD',
                                    'OffSnapCount','OffSnap%'
                                    ])

    df_qb["Year"] = df["Year"]
    df_qb["Date"] = df["Date"]
    df_qb["Week"] = df["Week"]
    df_qb["Team"] = df["Tm"]
    df_qb["Opp"] = df["Opp"]
    df_qb["Location"] = df["Unnamed: 7"].apply(lambda x: "A" if x == "@" else "H")

    for header, start, end in headers:
        if header.lower() == "passing":
            pass_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))

            df_qb["Cmp"] = pass_df["Cmp"].astype(int)
            df_qb["PassAtt"] = pass_df["Att"].astype(int)
            df_qb["Cmp%"] = pass_df["Cmp%"].astype(float)
            df_qb["PassYds"] = pass_df["Yds"].iloc[:, 0].astype(int) # after regex, passing yards and yards lost by sack are both 'Yds', so we take the first one which is passing yards
            df_qb["PassTD"] = pass_df["TD"].astype(int)
            df_qb["Int"] = pass_df["Int"].astype(int)
            df_qb["QBRating"] = pass_df["Rate"].astype(float)
            df_qb["Sacks"] = pass_df["Sk"].astype(int)
            df_qb["PassYd/Att"] = pass_df["Y/A"].astype(float)
            df_qb["AdjPassYd/Att"] = pass_df["AY/A"].astype(float)

        elif header.lower() == "rushing":
            rush_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))

            df_qb["RushAtt"] = rush_df["Att"].astype(int)
            df_qb["RushYd"] = rush_df["Yds"].astype(int)
            df_qb["RushYd/Att"] = rush_df["Y/A"].astype(float)
            df_qb["RushTD"] = rush_df["TD"].astype(int)

        elif header.lower() == "off. snaps":
            snap_df = df.iloc[:, start:end].rename(columns=lambda x: re.sub('\.[0-9]', '', x))
            
            df_qb["OffSnapCount"] = snap_df["Num"].astype(int)
            df_qb["OffSnap%"] = snap_df["Pct"].apply(lambda x: float(x) if isinstance(x, int) else float(x.replace("%", "")))
            
    return df_qb.fillna(0)