# BBC recipes web scrapper
- ![bbc_logo](https://static.wikia.nocookie.net/logopedia/images/d/d7/BBC_2021.svg/revision/latest/scale-to-width-down/250?cb=20210705123032)
- ![python_logo](https://www.python.org/static/community_logos/python-powered-w-100x40.png)
  
## A simple python script to convert all the recipes listed on the bbc's website into json format.

### First time doing anything web scrapping related, so not the cleanest but get's the job done 

#### The web scrapper script
 The BBC recipes website, paginates by alphabetical order, then by the results for that character. Starting at ```/a/1``` and ending at ```/z/1```. Each character has an unspecified amount of pages, so this is the first thing the script get's when looking at a new characters page.

 Total runtime of the script is between 30-40 minutes, with random pauses. Once completed you will have a JSON file with 9,000+recipes

##### The JSON format
```json
  {
    "title": "",
    "description": "",
    "prep_time": "",
    "cook_time": "",
    "serves": "",
    "ingredients": [
      {
        "header": "",
        "ingredients_list": []
      },
    ],
    "raw_ingredients_list": ["This data is extracted from inside <a> tags which included links to the ingredient, as the ingredients_list contains measurements ect, and i wanted a clean array of the raw ingredients names to do some filtering "],
    "methods": [
      {
        "1": ""
      },
    ]
  },
``` 

##### Helper scripts
 Once the data scrapping is completed, there are two helper files included which can quickly import the data into either mongodb or sqlite3.

##### Json to mongo
 ```bash
  py json_mongo.py input.json
 ```

##### Json to sqlite3
```bash
  py __main__.py input.json output.db
```
 