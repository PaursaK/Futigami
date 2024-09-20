from utility import Season
import pandas as pd

class LeagueHistory:
    '''class for managing all the data scraped from the webiste
    I imagine that each instance of this class would store/manage a particular league and its history of matches'''

    def __init__(self, leagueName):
        self.leagueName = leagueName
        self.seasonsHistory = []
        self.leagueHistoryTable = None

    def addSeason(self, seasonObject):
        self.seasonsHistory.append(seasonObject)

    def getLeagueHistoryTable(self):
        return self.leagueHistoryTable
    
    def setLeagueHistoryTable(self, df):
        self.leagueHistoryTable = df

    def createSeasonObject(self, seasonSummaryData, fixtureTableDictionary):
        '''creates a new instance of a season given the summaryData and dictionary with all the table information scraped from the website'''
        newSeason = Season(seasonSummaryData, fixtureTableDictionary)
        self.addSeason(newSeason)
        return newSeason
    
    def concatenateHistoryOfLeague (self, seasonObjectList):
        '''function looks to take a list of season instances and combine their associated dataframes 
        into a master dataframe that represents the leagues history'''
        #columns we are interested in aggregating data for
        
    def concatenateHistoryOfLeague(self, seasonObjectList):
        
        # Check if seasonObjectList is empty
        if not seasonObjectList:
            print("Empty Season List")
            return None

        # Start with an empty dataframe
        combinedDF = pd.DataFrame()

        for season in seasonObjectList:
            # Get the current season's dataframe
            seasonDF = season.getSeasonTable()
            #print(seasonDF.head(3))  # Debug to see the dataframe

            if combinedDF.empty:
                combinedDF = seasonDF
            else:
                common_columns = combinedDF.columns.intersection(seasonDF.columns).tolist()
                combinedDF = pd.merge(combinedDF, seasonDF, on=common_columns, how='outer')

        self.setLeagueHistoryTable(combinedDF)
        return combinedDF.drop_duplicates()



    


