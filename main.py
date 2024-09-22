from dataManagement import WebScraper, LeagueStorage
from utility import LeagueHistory
from processing import RequestProcessor
from userInterface import UserInterface
import requests
import random
import time
from fake_useragent import UserAgent

# Europe Top 5 Leagues Setup
leagues = {
    "Premier League": "9",
    "Serie A": "11",
    "La Liga": "12",
    "Bundesliga": "20",
    "Ligue 1": "13"
}

# Function to scrape league data with throttling and user agent rotation
def scrape_league_data(league_name, league_id):
    LH = LeagueHistory(league_name)
    ua = UserAgent()  # For rotating user agents

    # Scrape data for seasons from 2023 to 2024
    for year in range(1950, 2024):
        url = f"https://fbref.com/en/comps/{league_id}/{year}-{year + 1}/schedule/{year}-{year + 1}-{league_name.replace(' ', '-')}-Scores-and-Fixtures"

        headers = {
            'User-Agent': ua.random  # Random user agent
        }
        
        # Adding a delay before each request to avoid getting blocked
        time.sleep(random.uniform(1, 10))  # Wait 1-3 seconds before making a request

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            webscraper = WebScraper(url)  # Pass the content of the response
            season_summary_dict = webscraper.getSeasonSummary()
            fixture_table_dict = webscraper.readWebsiteTableData()
            each_season = LH.createSeasonObject(season_summary_dict, fixture_table_dict)
        else:
            print(f"Failed to scrape {url}: {response.status_code}")

    # Concatenate and store the history of the league
    LH.concatenateHistoryOfLeague(LH.seasonsHistory)
    return LH

# Initialize LeagueStorage
league_storage = LeagueStorage()

# Initialize LeagueHistory for each league and scrape data
for league_name, league_id in leagues.items():
    league_history = scrape_league_data(league_name, league_id)
    league_storage.addLeague(league_history)

# Example of how you would instantiate and run the UserInterface class
if __name__ == '__main__':
    ui = UserInterface(league_storage)
    ui.run()

'''# Europe Top 5 Leagues Setup
leagues = {
    "Premier League": "9",
    "Serie A": "11",
    "La Liga": "12",
    "Bundesliga": "20",
    "Ligue 1": "13"
}

# Initialize LeagueHistory for each league
league_histories = {}
for league_name, league_id in leagues.items():
    LH = LeagueHistory(league_name)
    
    # Scrape data for seasons from 2020 to 2024
    for year in range(1950, 2024):
        url = f"https://fbref.com/en/comps/{league_id}/{year}-{year+1}/schedule/{year}-{year+1}-{league_name.replace(' ', '-')}-Scores-and-Fixtures"
        webscraper = WebScraper(url)
        season_summary_dict = webscraper.getSeasonSummary()
        fixture_table_dict = webscraper.readWebsiteTableData()
        each_season = LH.createSeasonObject(season_summary_dict, fixture_table_dict)
    
    # Concatenate and store the history of the league
    LH.concatenateHistoryOfLeague(LH.seasonsHistory)
    league_histories[league_name] = LH

# Store all leagues in LeagueStorage
league_storage = LeagueStorage()
for LH in league_histories.values():
    league_storage.addLeague(LH)

# Example of how you would instantiate and run the UserInterface class
if __name__ == '__main__':
    ui = UserInterface(league_storage)
    ui.run()'''

'''#Europe Top 5 Leagues Initialized
LH = LeagueHistory("Premier League")
LH1 = LeagueHistory("Serie A")
LH2 = LeagueHistory("La Liga")
LH3 = LeagueHistory("Bundesliga")
LH4 = LeagueHistory("Ligue 1")

#Premier League Initialization
for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/9/{i}-{i+1}/schedule/{i}-{i+1}-Premier-League-Scores-and-Fixtures"
    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

seasonList = LH.seasonsHistory
LH.concatenateHistoryOfLeague(seasonList)
#print(LH.getLeagueHistoryTable())

#Serie A Initialization
for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/11/{i}-{i+1}/schedule/{i}-{i+1}-Serie-A-Scores-and-Fixtures"
    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH1.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

seasonList1 = LH1.seasonsHistory
LH1.concatenateHistoryOfLeague(seasonList1)
#print(LH1.getLeagueHistoryTable())

#La Liga Initialization
for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/12/{i}-{i+1}/{i}-{i+1}-La-Liga-Scores-and-Fixtures"
    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH2.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

seasonList2 = LH2.seasonsHistory
LH2.concatenateHistoryOfLeague(seasonList2)
#print(LH2.getLeagueHistoryTable())

#Bundesliga Intiialization
for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/20/{i}-{i+1}/{i}-{i+1}-Bundesliga-Scores-and-Fixtures"
    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH3.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

seasonList3 = LH3.seasonsHistory
LH3.concatenateHistoryOfLeague(seasonList3)
#print(LH3.getLeagueHistoryTable())

#Ligue 1 Initialization
for i in range(2020, 2024):
    url = f"https://fbref.com/en/comps/13/{i}-{i+1}/{i}-{i+1}-Ligue-1-Scores-and-Fixtures"

    webscraper = WebScraper(url)
    seasonSummaryDictionary = webscraper.getSeasonSummary()
    fixtureTableDictionary = webscraper.readWebsiteTableData()
    eachSeason = LH4.createSeasonObject(seasonSummaryDictionary, fixtureTableDictionary)

seasonList4 = LH4.seasonsHistory
LH4.concatenateHistoryOfLeague(seasonList4)
#print(LH4.getLeagueHistoryTable())

leagueStorage = LeagueStorage()
leagueStorage.addLeague(LH)
leagueStorage.addLeague(LH1)
leagueStorage.addLeague(LH2)
leagueStorage.addLeague(LH3)
leagueStorage.addLeague(LH4)

# Example of how you would instantiate and run the UserInterface class
if __name__ == '__main__':

    ui = UserInterface(leagueStorage)
    ui.run()'''
# Sample dataframes for different leagues
'''dataframes = {
    'Premier League': pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', periods=100, freq='D'),
        'home_team': ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'] * 20,
        'away_team': ['Team F', 'Team G', 'Team H', 'Team I', 'Team J'] * 20,
        'score': ['2-1', '3-2', '1-1', '0-0', '4-3'] * 20
    }),
    'La Liga': pd.DataFrame({
        'date': pd.date_range(start='2019-01-01', periods=100, freq='D'),
        'home_team': ['Team K', 'Team L', 'Team M', 'Team N', 'Team O'] * 20,
        'away_team': ['Team P', 'Team Q', 'Team R', 'Team S', 'Team T'] * 20,
        'score': ['1-0', '2-3', '3-1', '4-2', '5-2'] * 20
    }),
}

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='league-dropdown',
        options=[{'label': league, 'value': league} for league in leagueStorage.getLeagues().keys()],
        value='Premier League'
    ),
    dcc.Dropdown(
        id='start-year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2020, 2024)],
        value=2020
    ),
    dcc.Dropdown(
        id='end-year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2020, 2025)],
        value=2024
    ),
    dcc.Graph(id='heatmap')
])

@app.callback(
    Output('heatmap', 'figure'),
    Input('league-dropdown', 'value'),
    Input('start-year-dropdown', 'value'),
    Input('end-year-dropdown', 'value')
)
def update_heatmap(selected_league, startYear, endYear):
    global leagueStorage
    league = RequestProcessor.leagueSelect(selected_league, leagueStorage)
    filtered_df = RequestProcessor.yearInterval(int(startYear), int(endYear), league)


    # Create a heatmap
    fig = px.density_heatmap(
        filtered_df,
        x='home_score',
        y='away_score',
        z='date',
        histfunc='count',
        title=f'Density Heatmap for {selected_league} ({startYear} - {endYear})',
        labels={'home_score': 'Home Score', 'away_score': 'Away Score'},
        text_auto= True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


print(leagueStorage.getLeagues())

response = None
while(response != "q"):

    response = input("What league are you interested in seeing? ")
    if response == "q":
        break
    league = RequestProcessor.leagueSelect(response, leagueStorage)
    fig = px.density_heatmap(league.getLeagueHistoryTable(), x = "home_score", y = "away_score")
    fig.show()
    #print(league)
    #response = input("What Years do you want to see the history of it? ")
    #if response == "q":
        #break
    #startYear, endYear = tuple(response.split(" "))
    #print(RequestProcessor.yearInterval(int(startYear), int(endYear), league))
    

    

#for season in LH.seasonsHistory:
#    print(season)
#    print(season.seasonMatchTable.head(5))
#    print("-----------------------------------------------------------------------------------------------")'''





