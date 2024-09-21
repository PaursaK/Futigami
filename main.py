from dataManagement import WebScraper, LeagueStorage
from utility import LeagueHistory
from processing import RequestProcessor


LH = LeagueHistory("Premier League")
LH1 = LeagueHistory("Serie A")

for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/9/{i}-{i+1}/schedule/{i}-{i+1}-Premier-League-Scores-and-Fixtures"

    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

for i in range(2020, 2024):
    url1 = f"https://fbref.com/en/comps/11/{i}-{i+1}/schedule/{i}-{i+1}-Serie-A-Scores-and-Fixtures"

    webscraper1 = WebScraper(url1)
    seasonSummaryDictionary1 = webscraper1.getSeasonSummary()
    fixtureTableDictionary1 = webscraper1.readWebsiteTableData()
    eachSeason1 = LH1.createSeasonObject(seasonSummaryDictionary1, fixtureTableDictionary1)


seasonList = LH.seasonsHistory
LH.concatenateHistoryOfLeague(seasonList)
#print(LH.getLeagueHistoryTable())

seasonList1 = LH1.seasonsHistory
LH1.concatenateHistoryOfLeague(seasonList1)
#print(LH1.getLeagueHistoryTable())

leagueStorage = LeagueStorage()
leagueStorage.addLeague(LH)
leagueStorage.addLeague(LH1)

print(leagueStorage.getLeagues())

response = None
while(response != "q"):

    response = input("What league are you interested in seeing? ")
    if response == "q":
        break
    league = RequestProcessor.leagueSelect(response, leagueStorage)
    print(league)
    response = input("What Years do you want to see the history of it? ")
    if response == "q":
        break
    startYear, endYear = tuple(response.split(" "))
    print(RequestProcessor.yearInterval(int(startYear), int(endYear), league))
    

    

#for season in LH.seasonsHistory:
#    print(season)
#    print(season.seasonMatchTable.head(5))
#    print("-----------------------------------------------------------------------------------------------")





