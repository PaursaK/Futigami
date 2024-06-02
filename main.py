import requests
from bs4 import BeautifulSoup
url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup"

page = requests.get(url)

print(page.text)
soup = BeautifulSoup(page.text, "html.parser")

print(soup.prettify)
