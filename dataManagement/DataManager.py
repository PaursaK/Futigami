import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures-html"
page = requests.get(url)

#print(page.text)
soup = BeautifulSoup(page.text, "html.parser")

#print(soup.prettify)
trList = soup.find("tbody").find_all("tr")
firstRowInfo = trList[0].find_all("td")
print("Column Name: " + str(firstRowInfo[0]["data-stat"]))
print("Column Value: " + str(firstRowInfo[0].text))







#print(soup.find_all(string = "home_team"))

#Plan of Action
# 1 - Retrieive appropriate table tags in order to engage with the prem league fixture table
# 2 - translate that data to a pandas data frame
