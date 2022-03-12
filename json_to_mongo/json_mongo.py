import pymongo
import json
import sys

if len(sys.argv) < 2:
  print("INVALID CMD ARGUMENTS OR NONE PROVIDED")
  print("py json_mongo.py input.json")
  exit(1)

INPUT = sys.argv[1]

myClientConnection = pymongo.MongoClient("mongodb://localhost:27017/")
myRecipeDatabase = myClientConnection["recipes"]
bbcRecpieCollection = myRecipeDatabase["bbc_recpies"]

JSON_LOADED = {}

with open(INPUT) as json_file:
  JSON_LOADED = json.load(json_file)

mongoAdded = bbcRecpieCollection.insert_many(JSON_LOADED)