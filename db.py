import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect the py file with the database.
try:
    # Try to connect with the database if exists.
    con = psycopg2.connect(
        host = "localhost",
        database = "phrasalverbsdb",
        user = "postgres",
        password = "HERE_POSTGRES_PASSWORD"
    )
except:
    # Creates a connection between the py file and Postgres.
    con = psycopg2.connect(
        user = "postgres",
        password = "HERE_POSTGRES_PASSWORD"
    )
    # Allows to run 'Create Database' as part of a transaction block.
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Creates the database.
    cur = con.cursor()
    cur.execute('''CREATE DATABASE phrasalverbsdb''')
    cur.close()
    con.close()

    # Closes the previous connection and creates a new one with the database just created.
    con = psycopg2.connect(
        host = "localhost",
        user = "postgres",
        password = "HERE_POSTGRES_PASSWORD",
        database = "phrasalverbsdb"
    )
    cur = con.cursor()

    # Creates a standarised table to be used for the phrasal_verb.py script.
    cur.execute('''CREATE TABLE IF NOT EXISTS phrasalverbs 
        (id serial PRIMARY KEY, phrasal_verb VARCHAR 
        ( 16 ) NOT NULL, 
        explanations VARCHAR(255)[], 
        english_examples VARCHAR(255)[], 
        spanish_equivalent VARCHAR ( 255 ) NOT NULL)
    ;''')
    con.commit()
    cur.close()

def stop_connection():
    con.close()

# 1. Cursor acts like a vessel between the py file and the db. 2. Commit the data into the database. 3. Close the cursor. Stop the vessel from acting.
def inserting_data(pv, expla, engexpl, spaequ):
    cur = con.cursor()
    cur.execute("INSERT INTO phrasalverbs (phrasal_verb, explanations, english_examples, spanish_equivalent) VALUES (%s, %s, %s, %s)", (pv, expla, engexpl, spaequ))
    con.commit()
    cur.close()

def all_data_query():
    # RealDictCursor allows to return a group of tuples with the key/values pairs.
    cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM phrasalverbs")
    rec = cur.fetchall()
    return rec

def pv_exists_query(phrasal_verb):
    cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("SELECT phrasal_verb FROM phrasalverbs WHERE phrasal_verb=%s", (phrasal_verb,))
    rec = cur.fetchone()
    if rec:
        return rec['phrasal_verb']
    else:
        return

def update_query(id, pv, expla, engexpl, spaequ):
    cur = con.cursor()
    cur.execute("UPDATE phrasalverbs SET phrasal_verb=%s, explanations=%s, english_examples=%s, spanish_equivalent=%s WHERE id=%s", (pv, expla, engexpl, spaequ, id))
    con.commit()
    cur.close()