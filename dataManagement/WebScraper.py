import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


#Plan of Action
    # this class should be holding all season and match data, it should not store an individual season dataframe
    # will need to rethink the constructor to make this a more accurate representation of a data management tier
                # potentially build a method that parses an html page rather than have a soupObject designated for the Data Manager
                # only class variables should be a list of seasons parsed and maybe a beautiful soup object

class WebScraper:

    def __init__(self, websiteUrl):
        self.url = websiteUrl
        self.page = None
        self.soupObject = None
        
        # Error handling for request and parsing
        try:
            self.page = requests.get(self.url)
            self.page.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            self.soupObject = BeautifulSoup(self.page.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
        except Exception as e:
            print(f"An error occurred while parsing the page: {e}")
    
    def getPageHeader(self, containerTag = "div", containerId ="info", headerTag = "h1"):
        try:
            containerInfo = self.getContainerInfo(containerTag, containerId)
            if containerInfo is None:
                raise ValueError(f"Could not find container with tag '{containerTag}' and id '{containerId}'.")

            header = self.getTagOfInterest(containerInfo, headerTag)
            if not header:
                raise ValueError(f"No header tag '{headerTag}' found inside the container.")
            
            return header[0].text.strip()
        
        except Exception as e:
            print(f"An error occurred while getting the page header: {e}")
            return None
    
    def getSeasonDetails(self, headerString):
        try:
            # Regex pattern to capture two sets of four digits and the league name
            pattern = r"(\d{4})\s*-\s*(\d{4})\s*(.*)\s+Scores & Fixtures"
            match = re.search(pattern, headerString)
            
            if match:
                # Extract the years and league name
                start_year = match.group(1)
                end_year = match.group(2)
                league_name = match.group(3).strip()
                return start_year, end_year, league_name
            else:
                raise ValueError("No match found for the header string.")
        
        except re.error as e:
            print(f"Regex error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while extracting league info: {e}")
            return None
        
    def getContainerInfo(self, containerTag, containerId=None):
        '''Get container info by tag and optional id.'''
        try:
            if containerId:
                container = self.soupObject.find(containerTag, id=containerId)
            else:
                container = self.soupObject.find(containerTag)
            
            if container is None:
                raise ValueError(f"No container found with tag '{containerTag}'" +
                                 (f" and id '{containerId}'" if containerId else ""))
            
            return container
        
        except Exception as e:
            print(f"An error occurred while getting container info: {e}")
            return None
    
    def getTagOfInterest(self, containerInfo, tagOfInterest):
        '''Get all tags of interest within a given container.'''
        try:
            if containerInfo is None:
                raise ValueError("The container is None. Unable to search for tags.")
            
            tagList = containerInfo.find_all(tagOfInterest)
            
            if not tagList:
                raise ValueError(f"No tags of interest '{tagOfInterest}' found in the container.")
            
            return tagList
        
        except Exception as e:
            print(f"An error occurred while getting the tag of interest: {e}")
            return None


    def getSeasonSummary(self, containerInfo = ["div", "info"], tagsOfInterest = ["p", "a", "strong"], 
                         listOfSummaryData = ["Governing Country", "Champion", "Most Goals", "Most Assists", "Most Clean Sheets"]):

        '''Fetches the season summary from a specific container and tags of interest.'''

        # Initialize dictionary for storing the season summary
        seasonSummaryDictionary = {}

        try:
            # Get season details from the page header
            seasonDetails = self.getSeasonDetails(self.getPageHeader())
            if seasonDetails is None:
                raise ValueError("Season details could not be extracted.")
            
            seasonSummaryDictionary["StartYear"] = seasonDetails[0]
            seasonSummaryDictionary["EndYear"] = seasonDetails[1]
            seasonSummaryDictionary["League"] = seasonDetails[2]

            # Get the container (div or other) based on the tag and id
            div_info = self.getContainerInfo(containerInfo[0], containerInfo[1])
            if div_info is None:
                print("Container not found. Returning partial summary.")
                return seasonSummaryDictionary  # Return dictionary with partial data if no container is found

            # Get all tags of interest (e.g., all <p> tags)
            tagList = self.getTagOfInterest(div_info, tagsOfInterest[0])
            if tagList is None:
                raise ValueError(f"No tags of interest '{tagsOfInterest[0]}' found in the container.")

            # Iterate through the tags
            for tag in tagList:
                # Find the strong and a tags within the tag
                strong_tag = tag.find(tagsOfInterest[2])
                a_tag = tag.find(tagsOfInterest[1])

                # Continue only if both strong and a tags are found and strong_tag text is in the summary data
                if strong_tag and a_tag and strong_tag.text in listOfSummaryData:
                    seasonSummaryDictionary[strong_tag.text] = a_tag.text

            return seasonSummaryDictionary

        except Exception as e:
            print(f"An error occurred while getting the season summary: {e}")
            return seasonSummaryDictionary  # Return whatever data has been collected so far

    def getTableRows(self, tableTag, tableRowTag):
        '''Fetches table rows from the soup object.'''
        try:
            # Find the table with the specified tag
            table = self.soupObject.find(tableTag)
            if table is None:
                raise ValueError(f"Table with tag '{tableTag}' not found.")
            
            # Find all rows within the table
            tableRows = table.find_all(tableRowTag)
            if not tableRows:
                raise ValueError(f"No rows with tag '{tableRowTag}' found in the table.")
            
            return tableRows
        
        except Exception as e:
            print(f"An error occurred while fetching table rows: {e}")
            return None
    
    def initializeTableColumns(self, headRow):
        '''Extracts the column names from the header row and initializes the data dictionary.'''
        try:
            # Ensure headRow is not None and has the expected structure
            if not headRow:
                raise ValueError("Header row is empty or None.")
            
            # Extract column names using the "data-stat" attribute
            listOfColumns = [column.get("data-stat") for column in headRow]
            
            # Check for missing 'data-stat' attributes
            if None in listOfColumns:
                raise ValueError("Some columns are missing the 'data-stat' attribute.")
            
            # Initialize data dictionary with empty lists for each column
            dataDict = {column: [] for column in listOfColumns}
            
            return listOfColumns, dataDict
        
        except Exception as e:
            print(f"An error occurred while initializing table columns: {e}")
            return None, None

    def fillDataDict(self, tableRows, listOfColumns, dataDict):
        '''Populate the data dictionary with row data from the table.'''
        try:
            # Ensure that tableRows, listOfColumns, and dataDict are not None or empty
            if not tableRows:
                raise ValueError("Table rows are empty or None.")
            if not listOfColumns:
                raise ValueError("List of columns is empty or None.")
            if not dataDict:
                raise ValueError("Data dictionary is empty or None.")

            # Loop through each row in tableRows
            for row in tableRows:
                # Extract text from each cell, including both <th> and <td> elements
                rowData = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                
                # Skip the row if it is empty
                if not rowData or all(cell == "" for cell in rowData):
                    continue
                    
                # Populate the data dictionary with the row data
                for i, column in enumerate(listOfColumns):
                    dataDict[column].append(rowData[i])
        
        except Exception as e:
            print(f"An error occurred while filling the data dictionary: {e}")

    def readWebsiteTableData(self, tableTag = "tbody", tableRowTag = "tr"):
        '''
        Reads table data from a web-scraped URL and returns a data dictionary ready for conversion to a pandas DataFrame.
        :param tableTag: The tag of the table to search for (default 'tbody').
        :param tableRowTag: The tag of the rows within the table (default 'tr').
        :return: Dictionary with aggregate list of data per column found in a table on a website.
        '''
        try:
            # Fetch the table rows
            tableRows = self.getTableRows(tableTag, tableRowTag)
            if not tableRows:
                raise ValueError(f"No table rows found for tableTag '{tableTag}' and tableRowTag '{tableRowTag}'.")

            # Initialize the column headers and the data dictionary
            listOfColumns, dataDict = self.initializeTableColumns(tableRows[0])
            if listOfColumns is None or dataDict is None:
                raise ValueError("Failed to initialize columns or data dictionary.")

            # Populate the data dictionary with the rows of data
            self.fillDataDict(tableRows[1:], listOfColumns, dataDict)

            return dataDict

        except Exception as e:
            print(f"An error occurred while reading table data: {e}")
            return None


    


