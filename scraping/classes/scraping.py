# libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import math

import classes.utils as utils


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

    df = df.rename(columns={'Pos.':'RANK', 'équipe':'TEAM', '% vict.':'WIN%', 'MJ':'GP',
                        'V':'W', 'D':'L', 'PR':'FOR', 'PR':'MPTS', 'CTR':'MPTSA'})

    df['WIN%'] = df['WIN%'].apply(lambda x: float(x[:-1]))

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

    df["shoots_in"] = df["Tirs"].apply(lambda x: int(x.split("-")[0]))
    df["shoots_total"] = df["Tirs"].apply(lambda x: int(x.split("-")[1]))
    df["three_pts_in"] = df["3 pts"].apply(lambda x: int(x.split("-")[0]))
    df["three_pts_total"] = df["3 pts"].apply(lambda x: int(x.split("-")[1]))
    df["lf_in"] = df["LF"].apply(lambda x: int(x.split("-")[0]))
    df["lf_total"] = df["LF"].apply(lambda x: int(x.split("-")[1]))
    df = df.drop(["Tirs", "3 pts", "LF", "%", "%.1", "%.2"], axis=1)

    return df

def get_match_story():
    
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

