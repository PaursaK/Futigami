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

    #@requests_mock.Mocker()
    def setUp(self):
        url1 = "https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures"
        url2 = "https://fbref.com/en/comps/9/1888-1889/schedule/1888-1889-Football-League-Scores-and-Fixtures"
        
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
        self.assertIn("1888-1889 Football League", container2.text) 
    
    def test_get_tag_of_interest(self):

        # Test fetching all h1 tags within the container
        container1 = self.scraper1.getContainerInfo("div", "info")
        tags1 = self.scraper1.getTagOfInterest(container1, "h1")
        self.assertEqual(len(tags1), 1)
        self.assertEqual(tags1[0].text.strip(), "2023-2024 Premier League Scores & Fixtures")

        # Test fetching all h1 tags within the container
        container2 = self.scraper2.getContainerInfo("div", "info")
        tags2 = self.scraper2.getTagOfInterest(container2, "h1")
        self.assertEqual(len(tags2), 1)
        self.assertEqual(tags2[0].text.strip(), "1888-1889 Football League Scores & Fixtures")
    
    def test_get_season_summary(self):

        # Test fetching season summary data
        summary1 = self.scraper1.getSeasonSummary()
        expected_summary1 = {
        'Champion': 'Manchester City',
        'EndYear': '2024',
        'Governing Country': 'England',
        'League': 'Premier League',
        'Most Assists': 'Ollie Watkins',
        'Most Clean Sheets': 'David Raya',
        'Most Goals': 'Erling Haaland',
        'StartYear': '2023'
        }
        self.assertEqual(summary1, expected_summary1)

        # Test fetching season summary data
        summary2 = self.scraper2.getSeasonSummary()
        expected_summary2 = {
        'Champion': 'Preston',
        'EndYear': '1889',
        'Governing Country': 'England',
        'League': 'Football League',
        'StartYear': '1888'
        }
        self.assertEqual(summary2, expected_summary2)
    
    def test_get_table_rows(self):
        # Test fetching table rows
        rows1 = self.scraper1.getTableRows("tbody", "tr")
        print(rows1[0].find_all("td"))
        self.assertEqual(len(rows1), 423)
        self.assertEqual(rows1[1].find("td").text, "Sat")
        
        # Test fetching table rows
        rows2 = self.scraper2.getTableRows("tbody", "tr")
        print(rows2[0].find_all("td"))
        self.assertEqual(len(rows2), 170)
        self.assertEqual(rows2[1].find("td").text, "Sat")


    def test_initialize_table_columns(self):
        
        # Test initialization of table columns
        rows1 = self.scraper1.getTableRows("tbody", "tr")
        listOfColumns1, dataDict1 = self.scraper1.initializeTableColumns(rows1[0].find_all("td"))
        print(listOfColumns1, dataDict1)
        self.assertIsNotNone(dataDict1)
        self.assertIn("date", dataDict1)
        self.assertIn("home_team", dataDict1)

    def test_fill_data_dict(self):

        # Test populating data into the dictionary
        rows1 = self.scraper1.getTableRows("tbody", "tr")
        listOfColumns1, dataDict1 = self.scraper1.initializeTableColumns(rows1[0].find_all(["th","td"]))
        print(listOfColumns1, dataDict1)
        self.scraper1.fillDataDict(rows1, listOfColumns1, dataDict1)
        self.assertEqual(dataDict1["date"][1], "2023-08-12")
        self.assertEqual(dataDict1["home_team"][2], "Everton")

    def test_read_website_table_data(self):
        pass
        # Test reading table data and converting to dictionary
        dataDict = self.scraper1.readWebsiteTableData("tbody", "tr")
        print(dataDict)
        self.assertIsNotNone(dataDict)
        self.assertEqual(len(dataDict["date"]), len(dataDict["home_team"]))
        

if __name__ == '__main__':
    unittest.main()
