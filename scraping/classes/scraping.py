# libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import math
from bs4 import BeautifulSoup
import requests
import re
from datetime import * 

import classes.utils as utils
import classes.db_utils as db


def get_ranking():
    
    """ 
    Description:
    Get a simple table ranking with:
    - number of game played 
    - number of victories
    - number of defeats

    args : 

    return : 
    dictionnary with team as a key 
        and basics stats in values (rank, victory, etc...)
    """
    
    url = "https://www.lnb.fr/fr/pro-b/classement-2-57.html"
    res = pd.read_html(url)
    df = res[0]

    columns = list(df.columns.droplevel())
    columns.remove('Unnamed: 2_level_1')
    df = df.drop('équipe', axis=1)
    df.columns = columns

    df = df.rename(columns={'Pos.':'RANK', 'équipe':'TEAM', '% vict.':'WINp', 'MJ':'GP',
                        'V':'W', 'D':'L', 'PR':'FOR', 'PR':'MPTS', 'CTR':'MPTSA'})

    df['WINp'] = df['WINp'].apply(lambda x: float(x[:-1]))

    df = df.sort_values(by='TEAM')
    df['team_id'] = list(range(1, len(df) + 1))

    return df 

def get_teams_stats(option):
    
    """ 
    Description:
    Get global statistics in attack for every teams:

    args : 
    option:
        - "attack"
        - "defense"

    return : 
    dictionnary with team as a key 
        and basics in values
    """
    
    if option == "attack":  
        url = "https://www.lnb.fr/fr/pro-b/statistiques-equipes-1-61.html?season=2020&competition=241&format=total&team_stats_type=attaque"
    elif option == "defense":
        url = "https://www.lnb.fr/fr/pro-b/statistiques-equipes-1-61.html?season=2020&competition=241&format=total&team_stats_type=defense"
    else:
        return print("bad option: give 'attack' or 'defense' ")
    
    res = pd.read_html(url)
    df = res[0]
    columns = list(df.columns.droplevel())
    df.columns = columns

    df["FG"] = df["Tirs"].apply(lambda x: int(x.split("-")[0]))
    df["FGA"] = df["Tirs"].apply(lambda x: int(x.split("-")[1]))
    df["3PM"] = df["3 pts"].apply(lambda x: int(x.split("-")[0]))
    df["3PA"] = df["3 pts"].apply(lambda x: int(x.split("-")[1]))
    df["FTM"] = df["LF"].apply(lambda x: int(x.split("-")[0]))            
    df["FTA"] = df["LF"].apply(lambda x: int(x.split("-")[1]))
    df = df.drop(["Tirs", "3 pts", "LF"], axis=1)

    df = df.rename(columns={'Equipes':'TEAM', 'MJ':'GP', 'Min':'MIN', 'Pts':'PTS',
                            'O':'OREB', 'D':'DREB', 'T':'REB', 'Pr':'BLK',
                            'Ct':'BLKA', 'Pd':'AST', 'In':'STL', 'Bp':'TOV',
                            'Fte':'PF', 'Fpr':'PFD', 'Év':'EVAL', 
                            '%':'FGp', '%.1':'3Pp',  '%.2':'FTp'})

    df = df.sort_values(by='TEAM')
    df['team_id'] = list(range(1, len(df) + 1))

    # team_id in first position
    cols = list(df.columns)
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    return df

def get_url_matches():

    url = 'https://www.lnb.fr/fr/pro-b/calendrier-prob-59.html'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    urls = soup.find_all('a', href=True)

    codes_match = [int(re.findall('\d+', url['href'])[0]) for url in urls if 'prob/match' in url['href']]
    codes_match = list(set(codes_match))

    return codes_match


def get_match_id():

    conn = db.connect()
    
    url = "https://www.lnb.fr/fr/prob/match/fos-sur-mer-rouen-201666835.html#stats"

    res = pd.read_html(url)

    home_team = res[0].columns[0][0]
    away_team = res[1].columns[0][0]

    df_teams = db.select_table("TEAMS", conn)
    home_id = df_teams[df_teams['TEAM'] == home_team].iloc[0]['id']
    away_id = df_teams[df_teams['TEAM'] == away_team].iloc[0]['id']

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    select_tag = soup.find(id="gameday").find_all("option")
    day =  int(re.findall('\d+', select_tag[0].text)[0])

    match_id = int(str(day) + str(home_id) + str(away_id))

    conn.close()
    
    return match_id

def get_match_teams():
    
    url = "https://www.lnb.fr/fr/prob/match/fos-sur-mer-rouen-201666835.html#stats"

    res = pd.read_html(url)
    home_team = res[0].columns[0][0]
    away_team = res[1].columns[0][0]

    return home_team, away_team

def get_match_date():

    url = "https://www.lnb.fr/fr/prob/match/fos-sur-mer-rouen-201666835.html#stats"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    res = soup.find("p")
    day = int(res.text.split('-')[0].split('.')[1])
    month = int(res.text.split('-')[0].split('.')[2])
    year = int(res.text.split('-')[0].split('.')[3])

    return datetime(year, month, day)

def get_match_info():

    match_id = get_match_id()
    home_team, away_team = get_match_teams()
    match_date = get_match_date()

    return {'match_id':match_id, 'home_team':home_team,
            'away_team':away_team, 'match_date':match_date}

def get_match_story():

    conn = db.connect()
    
    url = "https://www.lnb.fr/fr/prob/match/fos-sur-mer-rouen-201666835.html#stats"
    res = pd.read_html(url)

    story_df = res[2]
    columns = ["home", "score", "away"]
    story_df.columns = columns
    
    actions = ["Passes décisives", "Tir intérieur réussi", 
               "Tir à trois points manqué", "Balle perdue",
               "Lancer franc réussi", "Faute provoquée",
               "Lancer franc manqué", "Passes décisives",
               "Rebond défensif", "Contre", "Tir intérieur manqué",
               "Faute", "Tir à trois points réussi", 
               "Interception", "Balle perdue",
               "Remplacement - joueur sortant",
               "Remplacement - joueur entrant",
               "Rebond offensif", "Temps mort",
               "team-turnover", "Dunk réussi",
               "Tir extérieur réussi", "Tir extérieur manqué",
               "Tir contré", "Tir à 3 points réussi", "dunk_missed"]
    
    story_df["home_actions"] = story_df["home"].apply(lambda x:utils.extract_actions(x, actions))
    story_df["home_player"] = story_df["home"].apply(lambda x:utils.remove_actions(x, actions))
    story_df["away_actions"] = story_df["away"].apply(lambda x:utils.extract_actions(x, actions))
    story_df["away_player"] = story_df["away"].apply(lambda x:utils.remove_actions(x, actions))
    
    story_df["time"] = story_df["score"].apply(lambda x: x[:5])
    story_df["home_score"] = story_df["score"].apply(lambda x: x[5:].split("-")[0])
    story_df["away_score"] = story_df["score"].apply(lambda x: x[5:].split("-")[1])
    story_df = story_df.drop(["home", "away", "score"], axis=1)
    
    return story_df


def get_players_stats(team):
    
    return None 

def get_match_pbp(num_url_match):
    
    return None

