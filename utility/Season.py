import Match
import pandas as pd

class Season:
    

    def __init__(self, startYear, endYear, league, country, mostGoals, mostAssists, mostCleanSheets, dictionaryData):
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
        self.league = league
        self.country = country
        self.mostGoals = mostGoals
        self.mostAssists = mostAssists
        self.mostCleanSheets = mostCleanSheets
        self.seasonMatchTable = pd.DataFrame(dictionaryData)

    
    def addMatchToSeason(self, match):
        '''
        helper method that adds a match that has been webscraped to the list of matches in the corresponding season.
        :param: match (Match) - match object 
        '''
        self.seasonMatches.append(match)

