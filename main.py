import requests
from bs4 import BeautifulSoup
url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures-html"
page = requests.get(url)

print(page.text)
soup = BeautifulSoup(page.text, "html.parser")

print(soup.prettify)
