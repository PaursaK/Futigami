import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
import requests_mock
import sys
import os
# Get the parent directory of the current file (the 'tests' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the parent (the project root folder)
parent_dir = os.path.dirname(current_dir)
# Add the project root to the Python path
sys.path.append(parent_dir)
from dataManagement import WebScraper  # Import your WebScraper class from your project module

class TestWebScraper(unittest.TestCase):

    @requests_mock.Mocker()
    def setUp(self, mocker):

        url1 = "https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures"
        url2 = "https://fbref.com/en/comps/9/1888-1889/schedule/1888-1889-Premier-League-Scores-and-Fixtures"
        
        # Create a WebScraper instance
        self.scraper1 = WebScraper(url1)
        self.scraper2 = WebScraper(url2)

    def test_get_page_header(self):
        # Test for successful extraction of the header
        header1 = self.scraper1.getPageHeader()
        header2 = self.scraper2.getPageHeader()

        self.assertEqual(header1, "2023-2024 Premier League Scores & Fixtures")
        self.assertEqual(header2, "1888-1889 Football League Scores & Fixtures")
    
    def test_get_season_details(self):
        # Test successful extraction of season details
        header1 = self.scraper1.getPageHeader()
        season_details1 = self.scraper1.getSeasonDetails(header1)
        self.assertEqual(season_details1, ("2023", "2024", "Premier League"))

        header2 = self.scraper2.getPageHeader()
        season_details2 = self.scraper2.getSeasonDetails(header2)
        self.assertEqual(season_details2, ("1888", "1889", "Football League"))
    
    def test_get_container_info(self):
        # Test getting container div with id="info"
        container1 = self.scraper1.getContainerInfo("div", "info")
        self.assertIsNotNone(container1)
        self.assertIn("2023-2024 Premier League", container1.text)

        # Test getting container div with id="info"
        container2 = self.scraper2.getContainerInfo("div", "info")
        self.assertIsNotNone(container2)
        self.assertIn("1889-1889 Football League", container2.text)
    
    def test_get_tag_of_interest(self):
        pass
        # Test fetching all h1 tags within the container
        container = self.scraper.getContainerInfo("div", "info")
        tags = self.scraper.getTagOfInterest(container, "h1")
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text.strip(), "2023-2024 Premier League Scores & Fixtures")
    
    def test_get_season_summary(self):
        pass
        # Test fetching season summary data
        summary = self.scraper.getSeasonSummary()
        expected_summary = {
            "StartYear": "2023",
            "EndYear": "2024",
            "League": "Premier League",
            "Governing Country": "England",
            "Champion": "Manchester City"
        }
        self.assertEqual(summary, expected_summary)
    
    def test_get_table_rows(self):
        # Test fetching table rows
        rows = self.scraper.getTableRows("tbody", "tr")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].find("td").text, "2023-08-11")

    def test_initialize_table_columns(self):
        pass
        # Test initialization of table columns
        rows = self.scraper.getTableRows("tbody", "tr")
        listOfColumns, dataDict = self.scraper.initializeTableColumns(rows[0].find_all("td"))
        print(listOfColumns, dataDict)
        self.assertEqual(listOfColumns, ["date", "team"])
        self.assertIsNotNone(dataDict)
        self.assertIn("date", dataDict)
        self.assertIn("team", dataDict)

    def test_fill_data_dict(self):
        pass
        # Test populating data into the dictionary
        rows = self.scraper.getTableRows("tbody", "tr")
        listOfColumns, dataDict = self.scraper.initializeTableColumns(rows[0].find_all("td"))
        print(listOfColumns, dataDict)
        self.scraper.fillDataDict(rows, listOfColumns, dataDict)
        self.assertEqual(dataDict["date"], ["2023-08-11", "2023-08-12"])
        self.assertEqual(dataDict["team"], ["Manchester United", "Liverpool"])

    def test_read_website_table_data(self):
        pass
        # Test reading table data and converting to dictionary
        dataDict = self.scraper.readWebsiteTableData("tbody", "tr")
        print(dataDict)
        self.assertIsNotNone(dataDict)
        self.assertEqual(dataDict["date"], ["2023-08-11", "2023-08-12"])
        self.assertEqual(dataDict["team"], ["Manchester United", "Liverpool"])

if __name__ == '__main__':
    unittest.main()
