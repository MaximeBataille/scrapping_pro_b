# packages
import classes.scraping as s
import classes.db_utils as db
import classes.db_initialize as db_init

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

    # SIMPLIFIER LE SCRAPING pour gagner du temps
    # add new matches into the database
    #db.truncate_table("MATCH", conn) 
    new_urls_matches = s.new_url_matches()
    for new_url_match in new_urls_matches:
        match_info_df = s.get_match_info(new_url_match)
        match_info_df.to_sql("MATCH", engine, if_exists='append', index=False, chunksize=10000)

    # urls_to_be_updated = s.get_url_match_to_play()
    # for url_to_be_updated in urls_to_be_updated:
    #     match_info_df = s.get_match_info(new_url_match)
    #     ... update with new values


    

    conn.close()
