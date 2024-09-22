#this class/file will be in charge of doing all the computations related to actions requested by user
#will come up with default options available and expand from there
from dataManagement import LeagueStorage

class RequestProcessor:

    def leagueSelect(leagueName, leagueStorage):
        '''returns the dataframe associated with the league selected'''
        return leagueStorage.getALeague(leagueName)
    
    def yearInterval(startYear, endYear, leagueHistoryObject):
        '''return a subset of the leagueHistory for specified years'''
        
        df = leagueHistoryObject.getLeagueHistoryTable()

        # If start year and/or end year not specified, return the entire history
        if startYear is None and endYear is None:
            return df
        
        #if startYear not specified return everything earlier or equal to end year
        elif startYear is None:
            return df[(df["date"].dt.year <= endYear)]
        
        #if endYear not specified return everything equal to or later than startYear
        elif endYear is None:
            return df[(df["date"].dt.year >= startYear)]
        

        
        return df[(df["date"].dt.year >= startYear) & (df["date"].dt.year <= endYear)]

