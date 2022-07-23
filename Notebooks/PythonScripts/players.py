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


def get_player_df(username, startYear):
    url = "https://www.pro-football-reference.com/players/K/" + username + "/gamelog/"
    df = pd.read_html(url, header=1)[0]
    df = df.head(df.shape[0] - 1)
    df = df[df['Date'] != "Date"]
    df = df[df['GS'] != "Did Not Play"]
    df = df[df['GS'] != "Inactive"]
    df = df[df['GS'] != "Injured Reserve"]
    df = df[df['GS'] != "COVID-19 List"]
    df.drop(columns=["GS"])
    df = df[df['Year'].astype(int) >= startYear]
    return df


# Adjusted Yards per pass attempt: (PassingYds + 20PassTD - 45Int)/(Passes attempted)
def get_rec_df(df):
    df_rec = pd.DataFrame(columns=['Year','Date','Week','Team','Opp','Location',
                                   'Tgt','Rec','RecYd','RecYd/Rec','RecYd/Tgt','Catch%','RecTD',
                                   'RushAtt','RushYd','RushYd/Att','RushTD',
                                   'OffSnapCount','OffSnap%'
                                ])

    for index,row in df.iterrows():
        loc = ""
        if row['Unnamed: 7'] == "@":
            loc = "A"
        else:
            loc = "H"
        catch = re.search("^(.*)%$", row['Ctch%']).group(1)
        snap = re.search("^(.*)%$", row['Pct']).group(1)
        df_rec.loc[index] = [int(row['Year']),row['Date'],int(row['Week']),str(row['Tm']),str(row['Opp']),loc,
                                int(row['Tgt']),int(row['Rec']),int(row['Yds']),float(row['Y/R']),float(row['Y/Tgt']),float(catch),int(row['TD']),
                                int(row['Att']),int(row['Yds.1']),float(row['Y/A']),int(row['TD.1']),
                                int(row['Num']),int(snap)
                               ]
                             
    df_rec = df_rec.fillna(0)
    return df_rec

def get_qb_df(df):
    df_qb = pd.DataFrame(columns=['Year','Date','Week','Team','Opp','Location',
                                  'Cmp','PassAtt','Cmp%','PassYd','PassTD','Int','QBRating','Sacks','PassYd/Att','AdjPassYd/Att',
                                  'RushAtt','RushYd','RushYd/Att','RushTD',
                                  'OffSnapCount','OffSnap%'
                                ])
    for index,row in df.iterrows():
        lst_date = row['Date'].split("-")
        date = datetime.datetime(int(lst_date[0]), int(lst_date[1]), int(lst_date[2]))
        loc = ""
        if row['Unnamed: 7'] == "@":
            loc = "A"
        else:
            loc = "H"
        snap = re.search("^(.*)%$", row['Pct']).group(1)
        df_qb.loc[index] = [int(row['Year']),date,int(row['Week']),str(row['Tm']),str(row['Opp']),loc,
                                int(row['Cmp']),int(row['Att']),float(row['Cmp%']),int(row['Yds']),int(row['TD']),int(row['Int']),float(row['Rate']),int(row['Sk']),float(row['Y/A']),float(row['AY/A']),
                                int(row['Att.1']),int(row['Yds.1']),float(row['Y/A.1']),int(row['TD.1']),
                                int(row['Num']),int(snap)

                           ]
    df_qb = df_qb.fillna(0)
    return df_qb

def get_rb_df(df):
    df_rb = pd.DataFrame(columns=['Year','Date','Week','Team','Opp','Location',
                                  'RushAtt','RushYd','RushYd/Att','RushTD',
                                  'Tgt','Rec','RecYd','RecYd/Rec','RecYd/Tgt','Catch%','RecTD',
                                  'OffSnapCount','OffSnap%'
                                ])
    for index,row in df.iterrows():
        lst_date = row['Date'].split("-")
        date = datetime.datetime(int(lst_date[0]), int(lst_date[1]), int(lst_date[2]))
        loc = ""
        if row['Unnamed: 7'] == "@":
            loc = "A"
        else:
            loc = "H"
        catch = re.search("^(.*)%$", row['Ctch%']).group(1)
        snap = re.search("^(.*)%$", row['Pct']).group(1)
        df_rb.loc[index] = [int(row['Year']),date,int(row['Week']),str(row['Tm']),str(row['Opp']),loc,
                                int(row['Att']),int(row['Yds']),float(row['Y/A']),int(row['TD']),
                                int(row['Tgt']),int(row['Rec']),int(row['Yds.1']),float(row['Y/R']),float(row['Y/Tgt']),float(catch),int(row['TD.1']),
                                int(row['Num']),int(snap)
                               ]
    df_rb = df_rb.fillna(0)
    return df_rb

#print(get_qb_df(get_player_df("WilsRu00", 2019)))