import classes.scraping as s
import classes.db_utils as db
import classes.db_initilize as db_init

conn = db.connect()
engine = db.engine()

try:
    teams_df = db_init.initialize_ranking()
    #db.truncate_table("TEAMS", conn)
    teams_df.to_sql("TEAMS", engine, if_exists='fail', index=False, chunksize=10000)


    conn.close()

except:
    conn.close()

