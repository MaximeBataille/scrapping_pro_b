# libraries

import math 
import numpy as np

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


def nb_periods(story_df):

    """
    Return the number of period in a match

    Compute this number by looking for the number of times
        when the chrono goes from 0 minutes to 9 minutes.

    Args:
        story_df : Dataframe of the match story

    Return:
        number of periods
    """

    minutes = list(df["time"].apply(lambda x: int(x.split(":")[0])))

    memory = 10
    cpt = 0
    for minute in minutes:
        if minute > memory:
            cpt += 1
        memory = minute

    return cpt
