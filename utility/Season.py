import pandas as pd

class Season:
    
    def __init__(self, seasonSummaryDictionary, dictionaryData):
        '''
        seasons constructor that builds a seasons object that holds data on the season year, country, league, and leading stat players
        :param: seasonSummaryDictionary - holds information related to champions, top goal scorer, etc.
        :param: dictionaryData - holds all the data related to each match
        '''

        self.startYear, self.endYear, self.league, self.country, self.champion, self.mostGoals, self.mostAssists, self.mostCleanSheets = self.storeSeasonSummary(seasonSummaryDictionary)
        self.seasonMatchTable = pd.DataFrame(dictionaryData)

    def getSeasonTable(self):
        return self.seasonMatchTable


    def storeSeasonSummary(self, seasonSummary):
        startYear = seasonSummary.get("StartYear", None)
        endYear = seasonSummary.get("EndYear", None)
        league = seasonSummary.get("League", None)
        country = seasonSummary.get("Governing Country", None)
        champion = seasonSummary.get("Champion", None)
        mostGoals = seasonSummary.get("Most Goals", None)
        mostAssists = seasonSummary.get("Most Assists", None)
        mostCleanSheets = seasonSummary.get("Most Clean Sheets", None)
        return startYear, endYear, league, country, champion, mostGoals, mostAssists, mostCleanSheets
    
    def __str__(self):
        return "League: " + str(self.league) + "\n"  + "Start: " + str(self.startYear) + "\n" + "End: " + str(self.endYear) + "\n" + "Champion: " + str(self.champion) + "\n" + "Most Goals: " + str(self.mostGoals) + "\n" + "Most Assists: " + str(self.mostAssists) + "\n" + "Most Clean Sheets: " + str(self.mostCleanSheets)



