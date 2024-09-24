#this class will incorporate plotly and host a local session (at first) to display all the information gathered from fbref
import dash
from dash import dcc, html, Input, Output
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
                value=None
            ),
            dcc.Dropdown(
                id='start-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in range(1950, 2024)],
                value=None
            ),
            dcc.Dropdown(
                id='end-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in range(1950, 2025)],
                value=None
            ),
            dcc.Graph(id='heatmap')
        ])
    
    def registerCallbacks(self):
        """Register callbacks to update the heatmap based on user input."""
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
    
    def run(self):
        """Run the Dash app."""
        self.app.run_server(debug=True)
