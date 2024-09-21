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
        if startYear is None or endYear is None:
            return df
        
        return df[(df["date"].dt.year >= startYear) & (df["date"].dt.year <= endYear)]

