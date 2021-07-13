# packages
import classes.scraping as s
import classes.db_utils as db
import classes.db_initilize as db_init

if __name__ == '__main__':

    conn = db.connect()
    engine = db.engine()

    # update ranking
    ranking_df = s.get_ranking()
    db.truncate_table("RANKING", conn)
    ranking_df.to_sql("RANKING", engine, if_exists='append', index=False, chunksize=10000)

    # update offensive stats
    teams_stats_off_df = s.get_teams_stats('attack')
    db.truncate_table("TEAMS_STATS_OFF", conn)
    teams_stats_off_df.to_sql("TEAMS_STATS_OFF", engine, if_exists='append', index=False, chunksize=10000)

    # update defensive stats
    teams_stats_off_df = s.get_teams_stats('defense')
    db.truncate_table("TEAMS_STATS_DEF", conn)
    teams_stats_off_df.to_sql("TEAMS_STATS_DEF", engine, if_exists='append', index=False, chunksize=10000)

    # add new matches into the database
    # set flag True if played
    # otherwise keep updating the infos
    urls_matches = s.get_url_matches()
    for url_match in urls_matches:
        s.get_match_info()

    conn.close()
