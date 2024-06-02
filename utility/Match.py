class Match:
    '''Object created to record data about soccer matches'''
    
    def __init__(self, homeTeam, homeScore, home_XG, awayTeam, awayScore, away_XG, gameWeek, date, venue):
        '''
        constructor for Match in soccer. records the home team, away team, location and statistics related to match.
        :param: homeTeam (String) - home team name
        :param: homeScore (Integer) - home team score
        :param: home_XG (Float) - home team expected goals
        :param: awayTeam (String) - away team name
        :param: awayScore (Integer) - away team score
        :param: away_XG (Float) - away team expected goals
        :param: venue (String) - name of the stadium where the match was held
        :param: gameWeek (Integer) - match week
        :param: date (String) - date of which the match was played
        '''

        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.gameWeek = gameWeek
        self.date = date
        self.venue = venue
        self.scoreReport = self.ScoreReport(homeScore, home_XG, awayScore, away_XG)


    class ScoreReport:
        '''
        inner class of the outer class Match that holds data in regards to the scoreline for a soccer match
        '''

        def __init__(self, homeScore, home_XG, awayScore, away_XG):
            '''
            constructor that creates a score report given the following parameters:

            :param: homeScore (Integer)
            :param: home_XG (Float)
            :param: awayScore (Integer)
            :param: away_XG (Float)
            '''
            self.homeScore = homeScore
            self.home_XG = home_XG
            self.awayScore = awayScore
            self.away_XG = away_XG




    
    
    