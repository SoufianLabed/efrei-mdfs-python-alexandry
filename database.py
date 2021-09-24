import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()
sql_query = """ 
    CREATE OR REPLACE TABLE book (
    id integer PRIMARY KEY,
    title text NOT NULL,
    author text NOT NULL,
    first_sentence text NOT NULL
    published integer NOT NULL
)"""
cursor.execute(sql_query)


cursor.execute(sql_query)
conn.commit()
conn.close()
