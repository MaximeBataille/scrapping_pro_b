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
                if "Faute provoquée" in x:
                    return "Faute provoquée"
                else:
                    return action
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
                if "Faute provoquée" in x:
                    action = "Faute provoquée"
                player_action = x.replace(action, "")
                player_action = player_action.split(".")[1]
                player_action = player_action.strip()
                break
    elif math.isnan(x):
        player_action =  np.nan
    else:
        player_action = 'caca'
    return player_action

def merge_players_actions(story_df):

    df = story_df.copy()

    df['action'] = df.home_actions.fillna(df.away_actions)
    df['player'] = df.home_player.fillna(df.away_player)

    return df 

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
        if minute > memory and minute >= 9:
            cpt += 1
        memory = minute

    return cpt

def get_periods(serie_time):

    """
    Return the number the period of each moment of the match

    Compute this number by looking for the number of times
        when the chrono goes from 0 minutes to 9 minutes.

    Args:
        serie_time : column time of the story_df

    Return:
        timeserie with period number at each moment of the match
    """

    periods = []
    minutes = list(serie_time.apply(lambda x: int(x.split(":")[0])))

    memory = 10
    cpt = 0
    for minute in minutes:
        if minute > memory and minute >= 9:
            cpt += 1
        memory = minute
        periods.append(cpt)

    return periods

def list_periods(serie_time):

    """
    Return the period number for each action

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

def get_seconds(serie_time):

    """
    Return the the second of each moment of the match

    Args:
        serie_time : column time of the story_df
    
    Return:
        serie --> second for each moment of the match
    """

    periods = get_periods(serie_time)
    minutes = list(serie_time.apply(lambda x: int(x.split(":")[0])))
    seconds = list(serie_time.apply(lambda x: int(x.split(":")[1])))

    seconds_list = []

    for period, minute, second in zip(periods, minutes, seconds):
        if period < 4:
            sec = (period * 10 * 60) + (600 - (minute * 60 + second))
            seconds_list.append(sec)
        elif period >= 4:
            sec = (period * 5 * 60) + (300 - (minute * 60 + second))
            seconds_list.append(sec) 
    
    return seconds_list

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

def get_sequence_on_ground(story_df, player):

    story_df['period'] = get_periods(story_df.time)
    story_df['seconds'] = get_seconds(story_df.time)
    df_player = story_df[story_df.player == player]

    check_start_five = False 
    on_ground = False # player on the ground or not
    sub_in = None 
    out = None
    sub_in_list = []
    out_list = []

    for i, row in df_player.iterrows():
        action = row['action']

        if action == 'Remplacement - joueur sortant':
            out = row['seconds']
            if check_start_five == False:
                sub_in = 0
                sub_in_list.append(sub_in)
            on_ground = False
            out_list.append(out)

        elif action == 'Remplacement - joueur entrant':
            sub_in = row['seconds']
            if check_start_five == False:
                check_start_five = True
            on_ground = True
            sub_in_list.append(sub_in)

        if i == df_player.index[-1]: # if a player finishes the match
            if on_ground:
                out = nb_seconds(story_df.time) # number of seconds in the match
                out_list.append(out)

    sequence = [(i, o) for i,o in zip(sub_in_list, out_list)]

    return sequence



