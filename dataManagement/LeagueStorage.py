from utility import LeagueHistory
import pandas as pd

class LeagueStorage:

    def __init__(self):
        '''constructor for the LeagueStorage object. This object will house all the leagues of interest'''
        self.leaguesDict = {}

    def getLeagues(self):
        '''returns a copy of the leagueDictionary; adheres to the encapulsation standard'''
        return self.leaguesDict
    
    def getALeague(self, leagueName):
        '''returns a league requested by name'''
        if (leagueName == None or leagueName == '' or leagueName not in self.getLeagues()):
            return None
        else:
            return self.getLeagues()[leagueName]

    
    def addLeague(self, league):
        """
        Add provided league to the leagueDict if it exists and is not empty.
        Return True if league was successfully added, False otherwise.
        """
        if league is None or league.getLeagueHistoryTable().empty:
            # Return False if the league is None or its table is empty
            return False

        leagueName = league.getLeagueName()
        
        # Check if the league already exists in the dictionary
        if leagueName in self.getLeagues():
            print("Duplicate entry detected")
            return False
        else:
            # Add the league to the dictionary
            self.getLeagues()[leagueName] = league
            return True



