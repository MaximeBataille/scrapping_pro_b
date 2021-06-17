# libraries
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import math



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
    
    story_df["home_actions"] = story_df["home"].apply(lambda x:extract_actions(x, actions))
    story_df["home_player"] = story_df["home"].apply(lambda x:remove_actions(x, actions))
    story_df["away_actions"] = story_df["away"].apply(lambda x:extract_actions(x, actions))
    story_df["away_player"] = story_df["away"].apply(lambda x:remove_actions(x, actions))
    
    story_df["time"] = story_df["score"].apply(lambda x: x[:5])
    story_df["home_score"] = story_df["score"].apply(lambda x: x[5:].split("-")[0])
    story_df["away_score"] = story_df["score"].apply(lambda x: x[5:].split("-")[1])
    story_df = story_df.drop(["home", "away", "score"], axis=1)
    
    return story_df

def get_players_stats(team):
    
    return None 

def get_match_pbp(num_url_match):
    
    return None

###### utils
def extract_actions(x, actions):
    
    """
    extract action in a string thanks to 
    a predefined list of actions
    
    Args:
        x : string
        actions : list of predefined actions
        
    Return:
        action
    """
    if isinstance(x, str):
        for action in actions:
            if action in x:
                break
    elif math.isnan(x):
        action =  np.nan
    return action

def remove_actions(x, actions):
    
    """
    remove action in a string thanks to 
    a predefined list of actions
    
    Args:
        x : string
        actions : list of predefined actions
        
    Return:
        string without action (player, nan, empty string)
    """
    if isinstance(x, str):
        for action in actions:
            if action in x:
                player_action = x.replace(action, "")
                player_action = player_action.split(".")[1]
                player_action = player_action.strip()
    elif math.isnan(x):
        player_action =  np.nan
    return player_action
