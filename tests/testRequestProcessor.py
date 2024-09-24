import unittest
from unittest.mock import MagicMock
import pandas as pd
import sys
import os
# Get the parent directory of the current file (the 'tests' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the parent (the project root folder)
parent_dir = os.path.dirname(current_dir)
# Add the project root to the Python path
sys.path.append(parent_dir)
from processing import RequestProcessor

class TestRequestProcessor(unittest.TestCase):

    def setUp(self):
        # Mocking the league history object
        self.leagueStorageMock = MagicMock()
        self.leagueHistoryObjectMock = MagicMock()

        # Example data for DataFrame mock
        data = {
            "date": pd.to_datetime(["2018-01-01", "2019-06-01", "2020-07-01", "2021-08-01"])
        }
        self.leagueHistoryMockDF = pd.DataFrame(data)

        # Set up the mock to return this DataFrame
        self.leagueHistoryObjectMock.getLeagueHistoryTable.return_value = self.leagueHistoryMockDF

    def test_leagueSelect(self):
        # Mock a sample dataframe returned by league storage
        league_df_mock = MagicMock()
        self.leagueStorageMock.getALeague.return_value = league_df_mock

        # Call the leagueSelect function
        result = RequestProcessor.leagueSelect("Premier League", self.leagueStorageMock)

        # Assert the getALeague was called with correct league name
        self.leagueStorageMock.getALeague.assert_called_with("Premier League")
        
        # Assert the result is the mocked dataframe
        self.assertEqual(result, league_df_mock)

    def test_yearInterval_with_start_and_end_year(self):
        # Call the yearInterval function
        result = RequestProcessor.yearInterval(2019, 2021, self.leagueHistoryObjectMock)

        # Filter the dataframe to check if the correct rows are returned
        expected_result = self.leagueHistoryMockDF[
            (self.leagueHistoryMockDF["date"].dt.year >= 2019) &
            (self.leagueHistoryMockDF["date"].dt.year <= 2021)
        ]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_yearInterval_with_startYear_only(self):
        # Test with only startYear
        result = RequestProcessor.yearInterval(2020, None, self.leagueHistoryObjectMock)

        # Filter the dataframe to check if the correct rows are returned
        expected_result = self.leagueHistoryMockDF[
            self.leagueHistoryMockDF["date"].dt.year >= 2020
        ]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_yearInterval_with_endYear_only(self):
        # Test with only endYear
        result = RequestProcessor.yearInterval(None, 2019, self.leagueHistoryObjectMock)

        # Filter the dataframe to check if the correct rows are returned
        expected_result = self.leagueHistoryMockDF[
            self.leagueHistoryMockDF["date"].dt.year <= 2019
        ]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_yearInterval_with_no_years(self):
        # Test with no years provided
        result = RequestProcessor.yearInterval(None, None, self.leagueHistoryObjectMock)

        # Assert the entire DataFrame is returned
        pd.testing.assert_frame_equal(result, self.leagueHistoryMockDF)

if __name__ == '__main__':
    unittest.main()