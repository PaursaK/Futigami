from utility import Season
import pandas as pd

class LeagueHistory:
    '''class for managing all the data scraped from the webiste
    I imagine that each instance of this class would store/manage a particular league and its history of matches'''

    def __init__(self, leagueName):
        self.leagueName = leagueName
        self.leagueStartYear = None
        self.seasonsHistory = []
        self.leagueHistoryTable = None

    def addSeason(self, seasonObject):
        self.seasonsHistory.append(seasonObject)
    
    def getLeagueName(self):
        return self.leagueName 
    
    def setLeagueStartYear(self, startYear):
        self.leagueStartYear = startYear

    def getLeagueStartYear(self):
        return self.leagueStartYear

    def getLeagueHistoryTable(self):
        return self.leagueHistoryTable
    
    def setLeagueHistoryTable(self, df):
        self.leagueHistoryTable = df

    def splitScoreLine(self, df):
        '''helper method that adds two additional columns 'home_score' and 'away_score' to the pandas dataframe'''

        # Replace en dash with hyphen
        df['score'] = df['score'].str.replace('–', '-', regex=False)
        
        # Now split the score column
        try:
            df[['home_score', 'away_score']] = df['score'].str.split('-', expand=True)
            
            # Convert to integers
            df['home_score'] = df['home_score'].astype(int)
            df['away_score'] = df['away_score'].astype(int)
        except Exception as e:
            print("Error while splitting score column:", e)

    def formatDate(self, df):

        # Convert the 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'])



    def createSeasonObject(self, seasonSummaryData, fixtureTableDictionary):
        '''creates a new instance of a season given the summaryData and dictionary with all the table information scraped from the website'''
        newSeason = Season(seasonSummaryData, fixtureTableDictionary)
        self.addSeason(newSeason)
        return newSeason
    
    def findEarliestStartYear(self, dateSeries):
        '''helper to extract earliest date in the leagues history'''
        if dateSeries is None or dateSeries.empty:
            return None
        
        earliest_date = dateSeries.min()
        return earliest_date.year if pd.notna(earliest_date) else None

    def concatenateHistoryOfLeague(self, seasonObjectList):
        '''returns the concatenated version '''
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
        
        #clean up and adjust master dataframe and then set it for the league
        combinedDF = combinedDF.drop_duplicates()
        self.splitScoreLine(combinedDF)
        self.formatDate(combinedDF)
        self.setLeagueHistoryTable(combinedDF)

        #set league origin year
        startOfLeague = self.findEarliestStartYear(combinedDF["date"])
        self.setLeagueStartYear(startOfLeague)

        return combinedDF
    
    def __str__(self):
        return "League Name: " + self.getLeagueName() + "\n" + "Year Established: " + str(self.getLeagueStartYear())



    


