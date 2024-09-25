from dataManagement import WebScraper, LeagueStorage
from utility import LeagueHistory
from userInterface import UserInterface
from logger import Logger
import os

# Folder where the data is stored
data_folder = "data"

#help to convert folder names to properly formated league names
leagueFormalName = {
    'ligue1' : "Ligue 1",
    'seriea' : "Serie A",
    'premierleague' : "Premier League",
    'laliga' : "La Liga",
    'bundesliga' : "Bundesliga"
}

# Initialize LeagueStorage
league_storage = LeagueStorage()

# Instantiate the singleton Logger
logger = Logger()

# Iterate through each league folder within 'data'
for league_folder in os.listdir(data_folder):

    LH = LeagueHistory(leagueFormalName[league_folder])

    league_path = os.path.join(data_folder, league_folder)
    
    # Make sure we're only processing directories (each league folder)
    if os.path.isdir(league_path):
        logger.log(f"Processing league: {league_folder}")
        
        # Iterate through each file in the league folder
        for page_file in os.listdir(league_path):
            file_path = os.path.join(league_path, page_file)
            
            # Only process .txt files
            if file_path.endswith(".txt"):
                logger.log(f"Reading file: {page_file}")
                
                # Read the text content of the file
                with open(file_path, "r", encoding="utf-8") as f:
                    page_text = f.read()
                
                    # Pass the content to the WebScraper
                    scraper = WebScraper(pageText=page_text)
                    season_summary_dict = scraper.getSeasonSummary()
                    fixture_table_dict = scraper.readWebsiteTableData()
                    each_season = LH.createSeasonObject(season_summary_dict, fixture_table_dict)
                
                # processing the parsed content
                if scraper.soupObject:
                    logger.log(f"Successfully parsed {page_file}")
                    # Example: log the page title
                    title = scraper.soupObject.title.string if scraper.soupObject.title else "No title"
                    logger.log(f"Title: {title}")
                else:
                    logger.log(f"Failed to parse {page_file}")
    
    LH.concatenateHistoryOfLeague(LH.seasonsHistory)
    league_storage.addLeague(LH)

#run the UI
if __name__ == '__main__':
    ui = UserInterface(league_storage)
    ui.run()






