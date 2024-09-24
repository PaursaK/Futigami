#this class will incorporate plotly and host a local session (at first) to display all the information gathered from fbref
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
from processing import RequestProcessor

class UserInterface:
    
    def __init__(self, leagueStorage):

        #store reference to the top 5 leagues data
        self.leagueStorage = leagueStorage

        #initialize the Dash app
        self.app = dash.Dash(__name__)

        #setup the layout of the app
        self.app.layout = self.layout()

        #setup callbacks
        self.registerCallbacks()

    def layout(self):
        """Define the layout of the Dash app."""
        return html.Div([
            dcc.Dropdown(
                id='league-dropdown',
                options=[{'label': league, 'value': league} for league in self.leagueStorage.getLeagues().keys()],
                value="Premier League"
            ),
            dcc.Dropdown(
                id='start-year-dropdown',
                value=None
            ),
            dcc.Dropdown(
                id='end-year-dropdown',
                value=None
            ),
            dcc.Graph(id='heatmap'),
            html.Div(id='match-table-container')
        ])
    
    def registerCallbacks(self):
        """Register callbacks to update the heatmap based on user input."""

        # Dynamic year range callback
        @self.app.callback(
            [Output('start-year-dropdown', 'options'),
             Output('end-year-dropdown', 'options')],
            [Input('league-dropdown', 'value')]
        )
        def update_year_dropdowns(selectedLeague):
            """Update the year range dropdowns based on selected league."""
            if selectedLeague:
                league_info = self.leagueStorage.getALeague(selectedLeague)
                start_year = league_info.getLeagueStartYear()  # Retrieve the origination year for the selected league
                end_year = 2024  # Define the max year as 2024 or current year
                year_range = [{'label': str(year), 'value': year} for year in range(start_year, end_year + 1)]
                
                return year_range, year_range
            return [], []  # Return empty options if no league is selected

        @self.app.callback(
            Output('heatmap', 'figure'),
            Input('league-dropdown', 'value'),
            Input('start-year-dropdown', 'value'),
            Input('end-year-dropdown', 'value')
        )
        def update_heatmap(selectedLeague, startYear, endYear):
            # Handle None values before calling int()
            startYear = int(startYear) if startYear is not None else None
            endYear = int(endYear) if endYear is not None else None

            league = RequestProcessor.leagueSelect(selectedLeague, self.leagueStorage)
            filtered_df = RequestProcessor.yearInterval(startYear, endYear, league)

            # Create a heatmap
            fig = px.density_heatmap(
                filtered_df,
                x='home_score',
                y='away_score',
                z='date',
                histfunc='count',
                title=f'Density Heatmap for {selectedLeague} ({startYear} - {endYear})',
                labels={'home_score': 'Home Score', 'away_score': 'Away Score'},
                text_auto=True
            )

            return fig
        
        # Callback to show the match details on click
        @self.app.callback(
            Output('match-table-container', 'children'),
            Input('heatmap', 'clickData'),  # Capture click events
            Input('league-dropdown', 'value'),
            Input('start-year-dropdown', 'value'),
            Input('end-year-dropdown', 'value')
        )
        def show_match_details(clickData, selectedLeague, startYear, endYear):
            """Display matches corresponding to the clicked heatmap tile."""
            if clickData is None:
                return "Click on a tile in the heatmap to see match details."
            
            # Extract home_score and away_score from the clicked data
            clicked_home_score = clickData['points'][0]['x']
            clicked_away_score = clickData['points'][0]['y']

            # Handle None values before calling int()
            startYear = int(startYear) if startYear is not None else None
            endYear = int(endYear) if endYear is not None else None

            # Get the filtered data for the selected league and year range
            league = RequestProcessor.leagueSelect(selectedLeague, self.leagueStorage)
            filtered_df = RequestProcessor.yearInterval(startYear, endYear, league)

            # Filter matches by the clicked home_score and away_score
            matches = filtered_df[(filtered_df['home_score'] == clicked_home_score) & 
                                  (filtered_df['away_score'] == clicked_away_score)]

            if matches.empty:
                return "No matches found for the selected score."

            # Filter the DataFrame to show only the required columns
            matches = matches[['date', 'home_team', 'away_team', 'home_score', 'away_score']]

            # Create a DataTable to display the filtered matches
            return html.Div([
                html.H4(f"Matches with Home Score: {clicked_home_score} and Away Score: {clicked_away_score}"),
                dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in matches.columns],
                    data=matches.to_dict('records'),
                    page_size=10
                )
            ])
    
    def run(self):
        """Run the Dash app."""
        self.app.run_server(debug=True)
