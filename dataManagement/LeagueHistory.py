from .WebScraper import WebScraper
from utility import Season

class LeagueHistory:
    '''class for managing all the data scraped from the webiste
    I imagine that each instance of this class would store/manage a particular league and its history of matches'''

    def __init__(self, leagueName):
        self.leagueName = leagueName
        self.seasonsHistory = []

    def addSeason(self, seasonObject):
        self.seasonsHistory.append(seasonObject)

    def createSeasonObject(self, seasonSummaryData, fixtureTableDictionary):

        return Season(seasonSummaryData, fixtureTableDictionary)
    


