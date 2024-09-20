from dataManagement import WebScraper
from utility import Season, LeagueHistory

print(WebScraper)
print(Season)
print(LeagueHistory)

LH = LeagueHistory("Premier League")

for i in range(1888, 2024, 15):
    url = f"https://fbref.com/en/comps/9/{i}-{i+1}/schedule/{i}-{i+1}-Premier-League-Scores-and-Fixtures"

    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)


seasonList = LH.seasonsHistory
LH.concatenateHistoryOfLeague(seasonList)
print(LH.getLeagueHistoryTable())

#for season in LH.seasonsHistory:
#    print(season)
#    print(season.seasonMatchTable.head(5))
#    print("-----------------------------------------------------------------------------------------------")





