import requests
from bs4 import BeautifulSoup
url = "https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures"
page = requests.get(url)

#print(page.text)
soup = BeautifulSoup(page.text, "html.parser")

def getContainerInfo(soup, containerTag, containerId):
    div_info = soup.find(containerTag, id = containerId)
    div_info.find_all("p")
    return div_info

def getTagOfInterest(containerInfo, tagOfInterest):
    tagList = containerInfo.find_all(tagOfInterest)
    return tagList

def getLeagueName(soup, containerTag = "div", containerId ="info", headerTag = "h1"):
    containerInfo = getContainerInfo(soup, containerTag, containerId)
    header = getTagOfInterest(containerInfo, headerTag)
    return header[0].text.strip()

def getSeasonYearInterval(headerString):
    interval = headerString.split("-")
    return interval[0].strip(), interval[1][:4].strip()

div_info = getContainerInfo(soup, "div", "info")
tagList = getTagOfInterest(div_info, "p")
leagueName = getLeagueName(soup, "div", "info", "h1")
seasonYear = getSeasonYearInterval(leagueName)
print(leagueName)
print(seasonYear)

print(tagList)



