from dataManagement import LeagueHistory, WebScraper
#from utility import Season


def process_season(url, league_name):
    try:
        webscraper = WebScraper(url)
        seasonSummaryDictionary = webscraper.getSeasonSummary()
        fixtureTableDictionary = webscraper.readWebsiteTableData()

        LH = LeagueHistory(seasonSummaryDictionary.get("League", "Unknown League"))
        seasonObject = LH.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)
        
        print(seasonObject)
        print(f"-------Pandas DataFrame Below For {league_name}---------")
        print(seasonObject.seasonMatchTable.head(3))
    except Exception as e:
        print(f"An error occurred: {e}")

# URL and League names
url1 = "https://fbref.com/en/comps/11/2023-2024/schedule/2023-2024-Serie-A-Scores-and-Fixtures"
league_name1 = "2023-2024 Serie A"

url2 = "https://fbref.com/en/comps/9/2022-2023/schedule/2022-2023-Premier-League-Scores-and-Fixtures"
league_name2 = "2022-2023 Premier League"

# Process both seasons
process_season(url1, league_name1)
process_season(url2, league_name2)



