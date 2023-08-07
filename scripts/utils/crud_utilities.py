import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2
from contextlib import contextmanager

load_dotenv()


# Database part
@contextmanager
def get_postgres_cnx() -> psycopg2.connect:
    try:
        cnx = psycopg2.connect(
            dbname="fullstack",
            user="balthapaixao",  # os.getenv("DE_POSTGRES_USER"),
            password=os.getenv("DE_POSTGRES_PASSWORD"),
            host="localhost",
            port=5432,
        )
        yield cnx
    finally:
        cnx.close()


def execute_values(conn: psycopg2.connect, df: pd.DataFrame, table: str):
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ",".join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


def read_from_postgres(query: str) -> pd.DataFrame:
    with get_postgres_cnx() as cnx:
        return pd.read_sql(sql=query, con=cnx)


def insert_postgres(df: pd.DataFrame, table_name: str) -> None:
    with get_postgres_cnx() as cnx:
        execute_values(cnx, df, table_name)

    return None
