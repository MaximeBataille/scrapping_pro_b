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
