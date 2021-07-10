import psycopg2

def connect():

    conn = psycopg2.connect(
    host="localhost",
    database="prob",
    user="postgres",
    password="22a7u6k")

    return conn

def insert_df_into_db(conn, table_name, values):

    # values as a tuple
    cursor = conn.cursor()

    query = f"""INSERT INTO "{table_name}" VALUES{values};"""
    cursor.execute(query)

def truncate_table(table_name, conn):

    cursor = conn.cursor()

    query = f"""TRUNCATE TABLE "{table_name}";"""
    cursor.execute(query)
    

