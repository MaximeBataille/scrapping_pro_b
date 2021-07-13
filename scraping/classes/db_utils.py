import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import pandas.io.sql as sqlio

def connect():

    conn = psycopg2.connect(
    host="localhost",
    database="prob",
    user="postgres",
    password="22a7u6k")

    conn.autocommit = True

    return conn

def engine():

    db_connection_url = "postgresql://{}:{}@{}:{}/{}".format(
        "postgres", 
        "22a7u6k",
        "localhost",
        5432,
        "prob")

    return create_engine(db_connection_url)

def insert_df_into_table(df, conn, table_name, columns):

    cursor = conn.cursor()

    if isinstance(df, pd.core.frame.DataFrame):
        data = [tuple(row) for _, row in df.iterrows()]
        records_list_template = ','.join(['%s'] * len(data))
        print(data)
        query = f"""INSERT INTO "{table_name}" ({columns}) VALUES {records_list_template}"""

    elif isinstance(df, pd.core.series.Series):
        serie = df.copy()
        data = [tuple([value]) for value in serie]
        print(data)
        records_list_template = ','.join(['%s'] * len(data))
        query = f"""INSERT INTO "{table_name}" ({columns}) VALUES {records_list_template}"""

    print(query)

    cursor.execute(query, data)

def insert_values_into_db(conn, table_name, values):

    # values as a tuple
    cursor = conn.cursor()

    if len(values) == 1:
        query = f"""INSERT INTO "{table_name}" VALUES {values};"""
        cursor.execute(query)
    else:
        query = f"""INSERT INTO "{table_name}" VALUES {values};"""
        cursor.execute(query)
        
def truncate_table(table_name, conn):

    cursor = conn.cursor()

    query = f"""TRUNCATE TABLE "{table_name}";"""
    cursor.execute(query)
    
def select_table(table_name, conn):

    query = f"""select * from "{table_name}" ;"""
    return sqlio.read_sql_query(query, conn)

