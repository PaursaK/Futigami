import requests
from bs4 import BeautifulSoup
url = "https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures"
page = requests.get(url)

#print(page.text)
soup = BeautifulSoup(page.text, "html.parser")

div_info = soup.find("div", id = "info")
ptagList = div_info.find_all("p")
print(ptagList)

for ptag in ptagList:
    atag = ptag.find("a")
    strongtag = ptag.find("strong")

    if strongtag == None or atag == None:
        continue
    else:
        print(strongtag.text + ": " + atag.text)

    #print(ptag.find("a").text)
#atagList = div_info.find_all("a")
#print(atagList)
#for atag in atagList:
#    print(atag.text)
#print(soup.prettify)


