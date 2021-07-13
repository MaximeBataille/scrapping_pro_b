import classes.scraping as s

def initialize_ranking():

    ranking_df = s.get_ranking()

    ranking_df = ranking_df.sort_values(by='TEAM')
    ranking_df['id'] = list(range(1, len(ranking_df) + 1))
    teams_df = ranking_df[['id', 'TEAM']]

    return teams_df