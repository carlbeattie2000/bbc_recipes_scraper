from time import sleep, time
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import lxml
import cchardet
from random import randint

STRIPED_BASE_URL = "https://www.bbc.co.uk"
BASE_WEBSITE_URL = "https://www.bbc.co.uk/food/recipes/a-z/"

session = requests.Session()

headers = requests.utils.default_headers()
headers.update(
  {
    'User-agent': "My User Agent 1.0",
  }
)

currentPageNumber = 1
maxPages = 0

currentCharacterCode = 97
maxCharacterCode = 122

globalStorageList = []

totalRequestsMade = 0

# This function attempts to retrieve the page, but if we have made to many requests we pause for a some amount of time.
def getPage(url, headers):
  pageRetrived = False
  
  while (pageRetrived == False):
    try:
      pageRetrived = session.get(url, headers=headers)
    except:
      pageRetrived = False
      sleep(randint(20, 30))

  return pageRetrived

def BeautifulSoupWithParseOnly(page, elementToTarget):
  return BeautifulSoup(page.text, "lxml", parse_only=SoupStrainer(elementToTarget))

# Run the loop while current character is bellow z
while (currentCharacterCode < maxCharacterCode):

  timeStart = round(time() * 1000)

  currentCharacterConverted = chr(currentCharacterCode)

  # Get the max amount of pages
  retrievedPageForPageLimitGet = getPage(BASE_WEBSITE_URL + f"{currentCharacterConverted}/{currentPageNumber}", headers)

  if (retrievedPageForPageLimitGet.status_code == "301"):
    continue

  pageForPageLimitRetrievalSoup = BeautifulSoupWithParseOnly(retrievedPageForPageLimitGet, "a")

  findMaxPageLimit = pageForPageLimitRetrievalSoup.find_all("a", class_="pagination__link")

  if len(findMaxPageLimit) > 0:
    maxPages = int(findMaxPageLimit[len(findMaxPageLimit) - 2].text)
  else:
    maxPages = 1

  while (currentPageNumber < maxPages):
    currentMainPage = getPage(BASE_WEBSITE_URL + f"{currentCharacterConverted}/{currentPageNumber}", headers)

    print(BASE_WEBSITE_URL + f"{currentCharacterConverted}/{currentPageNumber}")

    currentPageSoup = BeautifulSoupWithParseOnly(currentMainPage, "div")

    recipesFound = currentPageSoup.find(id=f"az-recipes-{currentCharacterConverted}-recipes")

    recipesFoundLinks = recipesFound.find_all("a", href=True)

    for recipeLink in recipesFoundLinks:
      recipeLocalStorage = {}

      currentRecpiePage = getPage(STRIPED_BASE_URL + recipeLink["href"], headers)

      if str(currentRecpiePage.status_code) == "500":
        continue

      currentRecpiePageSoup = BeautifulSoupWithParseOnly(currentRecpiePage, "div")

      pageMainContent = currentRecpiePageSoup.find(id="main-content")

      ingredientsListWrapper = pageMainContent.find("div", class_="recipe-ingredients-wrapper")

      recipeTitle = pageMainContent.find("h1", class_="gel-trafalgar content-title__text")
      recipeLocalStorage["title"] = recipeTitle.text.strip()

      recipeDescription = pageMainContent.find("p", class_="recipe-description__text")

      if recipeDescription:
        recipeLocalStorage["description"] = recipeDescription.text.strip()

      recipePrepTime = pageMainContent.find("p", class_="recipe-metadata__prep-time")

      if recipePrepTime:
        recipeLocalStorage["prep_time"] = recipePrepTime.text.strip()

      recipeCookTime = pageMainContent.find("p", class_="recipe-metadata__cook-time")

      if recipeCookTime:
        recipeLocalStorage["cook_time"] = recipeCookTime.text.strip()

      recipeServes = pageMainContent.find("p", class_="recipe-metadata__serving")

      if recipeServes:
        recipeLocalStorage["serves"] = recipeServes.text.strip()

      recipeImage = pageMainContent.find("div", class_="recipe-media")

      if recipeImage != None:
        try:
          recipeLocalStorage["image"] = recipeImage.find("img")["src"]
        except:
          print("no image found", recipeImage)

      ingredientSubHeaders = ingredientsListWrapper.find_all("h3", class_="recipe-ingredients__sub-heading")

      ingredientLists = ingredientsListWrapper.find_all("ul", class_="recipe-ingredients__list")

      recipeLocalStorage["ingredients"] = []
      rawIngredientNames = []

      for ing in ingredientLists:
        ingredientLocalStorage = {}
        ingredientListsArray = []

        previousElement = ing.find_previous()

        for item in ing:
          ingredientListsArray.append(item.text)

          try:
            ingredientRawName = item.find("a", href=True)
            rawIngredientNames.append(ingredientRawName.text)
          except:
            pass

        if ("recipe-ingredients__sub-heading" in previousElement["class"]):
          ingredientLocalStorage["header"] = previousElement.text

        ingredientLocalStorage["ingredients_list"] = ingredientListsArray

        recipeLocalStorage["ingredients"].append(ingredientLocalStorage)

      recipeLocalStorage["raw_ingredients_list"] = rawIngredientNames
      
      recipePageMethods = pageMainContent.find("ol", class_="recipe-method__list")

      if len(recipePageMethods) > 0:
        recipeMethodsList = []

        num = 1

        for method in recipePageMethods:
          recipeMethodsList.append({num: method.text})

          num += 1
        
        recipeLocalStorage["methods"] = recipeMethodsList
      
      globalStorageList.append(recipeLocalStorage)

    currentPageNumber += 1
  
  print("page", currentCharacterConverted, "all requests took", (round(time() * 1000) - timeStart) / 1000, "seconds" )
  
  file = open("recipes.json", "w")
  json.dump(globalStorageList, file, indent=2, separators=(',',': '))
  file.close()

  currentCharacterCode += 1
  currentPageNumber = 1