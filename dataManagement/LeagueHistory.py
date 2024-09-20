from .WebScraper import WebScraper
from utility import Season
import pandas as pd

class LeagueHistory:
    '''class for managing all the data scraped from the webiste
    I imagine that each instance of this class would store/manage a particular league and its history of matches'''

    def __init__(self, leagueName):
        self.leagueName = leagueName
        self.seasonsHistory = []

    def addSeason(self, seasonObject):
        self.seasonsHistory.append(seasonObject)

    def createSeasonObject(self, seasonSummaryData, fixtureTableDictionary):
        
        newSeason = Season(seasonSummaryData, fixtureTableDictionary)
        self.addSeason(newSeason)
        return newSeason
    
    def concatenateHistoryOfLeague (self, seasonObjectList):

        combinedDF = pd.DataFrame({'gameweek':[],'dayofweek':[], 'date':[], 'start_time':[], 'home_team':[], 'score':[], 'away_team':[], 'attendance':[], 'venue':[], 'referee':[], 'match_report' :[], 'notes': []})

        for season in seasonObjectList:
            combinedDF = pd.merge(combinedDF, season.getSeasonTable(), on=['gameweek','dayofweek', 'date', 'start_time', 'home_team', 'score', 'away_team', 'attendance', 'venue', 'referee', 'match_report', 'notes'], how='outer')
        
        return combinedDF.drop_duplicates()


    


