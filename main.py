from dataManagement import LeagueHistory, WebScraper
from utility import Season

LH = LeagueHistory("Premier League")

for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/9/{i}-{i+1}/schedule/{i}-{i+1}-Premier-League-Scores-and-Fixtures"

    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)


seasonList = LH.seasonsHistory
leagueHistoryDF = LH.concatenateHistoryOfLeague(seasonList)
print(leagueHistoryDF)

#for season in LH.seasonsHistory:
#    print(season)
#    print(season.seasonMatchTable.head(20))
#    print("-----------------------------------------------------------------------------------------------")





