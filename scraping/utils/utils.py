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


def nb_periods(serie_time):

    """
    Return the number of period in a match

    Compute this number by looking for the number of times
        when the chrono goes from 0 minutes to 9 minutes.

    Args:
        serie_time : column time of the story_df

    Return:
        number of periods
    """

    minutes = list(serie_time.apply(lambda x: int(x.split(":")[0])))

    memory = 10
    cpt = 0
    for minute in minutes:
        if minute > memory:
            cpt += 1
        memory = minute

    return cpt


def list_periods(serie_time):

    """
    Return the the period number for each action

    Compute this number by looking for the number of times
        when the chrono goes from 0 minutes to 9 minutes.

    Args:
        serie_time : column time of the story_df

    Return:
        list --> period number for each moment of the match
    """

    minutes = list(serie_time.apply(lambda x: int(x.split(":")[0])))

    period = []

    memory = 10
    cpt = 0
    for minute in minutes:
        if minute > memory:
            cpt += 1
        memory = minute
        period.append(cpt)

    return period


def list_players(read_html):

    """
    Return the list of players for both teams

    Args:
        read_html : the output of the read_htmk function from pandas
            to scrap a datatable
    
    Return:
        A tuple with the lists of players for home_team and away_team
    """

    players_home_team = read_html[0].iloc[:, 1]
    players_away_team = read_html[1].iloc[:, 1]

    return players_home_team, players_away_team

def nb_seconds(serie_time):

    """
    Return the number of seconds in a match

    Args:
        serie_time : column time of the story_df
    
    Return:
        int --> number of seconds
    """

    n_periods = nb_periods(serie_time)

    # number of seconds in a match
    if n_periods <= 4:
        seconds = 10 * 4 * 60
        return seconds
    # if extra time
    elif n_periods > 4:
        seconds = 10 * 4 * 60
        extra_times = n_periods - 4
        seconds += seconds + (extra_times * 5 * 60)
        return seconds

def second_on_the_ground(df, player):

    """
    Return a boolean list. True if the player is on the ground, False otherwise, for each second

    Args:
        story_df : story of the match
        player : player name
    
    Return:
        list --> True / False for each second
    """

    story_df = df.copy()

    # home or away for player
    home_players = list(story_df["home_player"])
    away_players = list(story_df["away_player"])
    print(player)

    if player in home_players:
        col_place = "home"
    elif player in away_players:
        col_place = "away"
    else :
        print("Error : do not find home / away")

    seconds = nb_seconds(story_df['time'])
    seconds_list = list(range(seconds))

    story_df['period'] = list_periods(story_df.time)

    on_ground = [0] * len(seconds_list)

    for i, row in story_df.iterrows():
        period = row['period']
        period += 1
        time = row['time']

        if period > 4:
            minutes = 5 - int(time.split(":")[0])
            seconds = 60 - int(time.split(":")[1])
            seconds = seconds%60
        elif period <= 4:
            minutes = 10 - int(time.split(":")[0])
            seconds = 60 - int(time.split(":")[1])
            seconds = seconds%60

        # if during extra time
        if period > 4:
            seconds_match = (4 * 10 * 60) + ((period - 4 - 1) * 5 * 60) + minutes * 60 + seconds
        elif period <= 4:
            seconds_match = ((period - 1) * 10 * 60) + minutes * 60 + seconds

        action = row[col_place + '_actions']
        player_action = row[col_place + '_player']

        if player == player_action:
            if action == 'Remplacement - joueur entrant':
                on_ground[seconds_match] = True
            elif action == 'Remplacement - joueur sortant':
                print(time)
                print(period)
                print(seconds_match)
                on_ground[seconds_match] = False
                print(on_ground[seconds_match])

    # fullfill 0 with True or False
    for i in range(len(on_ground)):
        og = on_ground[i]
        if og is False or og is True:
            break

    on_ground[0] = og
    for i in range(len(on_ground)):
        og = on_ground[i]
        if og is False or og is True:
            memory = og
        else:
            on_ground[i] = memory

    return on_ground






