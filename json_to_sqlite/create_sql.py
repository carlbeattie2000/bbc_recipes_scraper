import sqlite3 as sql3

def createTable(datbase):
  connection = sql3.connect(datbase)

  connection.execute('''
    CREATE TABLE IF NOT EXISTS 
    bbc_recipes 
    (
      ID INT PRIMARY KEY NOT NULL,
      title TEXT,
      description TEXT,
      image TEXT,
      prep_time TEXT,
      cook_time TEXT,
      serves TEXT,
      ingredients TEXT,
      raw_ingredients_list TEXT,
      methods TEXT
    )
  ''')

  connection.close()