import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()

sql_query = """ 
    CREATE TABLE book (
    id integer PRIMARY KEY,
    title text NOT NULL,
    author text NOT NULL,
    first_sentence text NOT NULL,
    published integer NOT NULL
)"""
cursor.execute(sql_query)

sql_insert = """ 
    INSERT INTO book (
    title,
    author,
    first_sentence,
    published)
    VALUES ("test", "test", "test", 1555)"""
cursor.execute(sql_insert)