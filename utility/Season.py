import Match
import pandas as pd

class Season:
    

    def __init__(self, startYear, endYear, seasonSummaryDictionary, dictionaryData):
        '''
        seasons constructor that builds a seasons object that holds data on the season year, country, league, and leading stat players
        :param: startYear (Integer) - year the season starts
        :param: endYear (Integer) - year the season ends
        :param: league (String) - name of the league
        :param: country (String) - the country that the league is apart of
        :param: mostGoals (String) - the players name with the most goals
        :param: mostAssists (String) - the players name with the most assists
        :param: mostCleanSheets (String) - the players name with the most clean sheets
        '''

        self.startYear = startYear
        self.endYear = endYear
        self.league, self.country, self.champion, self.mostGoals, self.mostAssists, self.mostCleanSheets = self.storeSeasonSummary(seasonSummaryDictionary)
        self.seasonMatches = []
        self.seasonMatchTable = pd.DataFrame(dictionaryData)


    
    def addMatchToSeason(self, match):
        '''
        helper method that adds a match that has been webscraped to the list of matches in the corresponding season.
        :param: match (Match) - match object 
        '''
        self.seasonMatches.append(match)

    def createMatchObject(self):
        #need to iterate through pandas data frame and store the information
        #update notes column with match object (this will aid in representing the data later for visualization)
        pass
    def storeSeasonSummary(self, seasonSummary):
        return seasonSummary["Governing Country"], seasonSummary["Champion"], seasonSummary["Most Goals"], seasonSummary["Most Assists"], seasonSummary["Most Clean Sheets"]


