from create_sql import *

import sqlite3 as sql3
import json
import sys

if len(sys.argv) < 3:
  print("INVALID CMD ARGUMENTS OR NONE PROVIDED")
  print("py __main__.py file.json ./database.db")
  exit(1)

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]

createTable(OUTPUT)
connection = sql3.connect(OUTPUT)

# Load JSON into script
def loadDataFromObjectKey(object, key):
    try:
        return object[key]
    except:
        return "none provided"


def insertIntoDatabase(id, title, description, image, prep_time,
                       cook_time, serves, ingredients, raw_ingredients, methods):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO bbc_recipes(
   ID, title, description, image, prep_time, cook_time, serves, ingredients, raw_ingredients_list, methods) VALUES 
   (?, ?,?,?,?,?,?,?,?,?)''', (id, title, description, image, prep_time, cook_time, serves, ingredients, raw_ingredients, methods))


JSON_OBJECT_LOADED = {}
ID_ = 1

with open(INPUT) as json_file:
    JSON_OBJECT_LOADED = json.load(json_file)

for json_item in JSON_OBJECT_LOADED:
    title = loadDataFromObjectKey(json_item, "title")
    description = loadDataFromObjectKey(json_item, "description")
    image = loadDataFromObjectKey(json_item, "image")
    prep_time = loadDataFromObjectKey(json_item, "prep_time")
    cook_time = loadDataFromObjectKey(json_item, "cook_time")
    serves = loadDataFromObjectKey(json_item, "servers")

    # Arrays to convert to strings
    try:
        ingredients = json.dumps(json_item["ingredients"])
    except:
        ingredients = "none provided"

    try:
        raw_ingredients = json.dumps(json_item["raw_ingredients_list"])
    except:
        raw_ingredients = "none provided"

    try:
        methods = json.dumps(json_item["methods"])
    except:
        methods = "none provided"

    insertIntoDatabase(ID_, title, description, image,
                       prep_time, cook_time, serves, ingredients, raw_ingredients, methods)
    ID_ += 1

connection.commit()
connection.close()

print("completed")
