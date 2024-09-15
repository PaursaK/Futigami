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
        self.page = requests.get(self.url)
        self.soupObject = BeautifulSoup(self.page.text, "html.parser")


    '''def getLeagueHistory(self):
        getter method that returns a pandas dataframe of the season results for a given year
        :param: None
        :return: pandas DataFrame
        
        return self.seasonData'''
    
    def getPageHeader(self, containerTag = "div", containerId ="info", headerTag = "h1"):
        containerInfo = self. getContainerInfo(containerTag, containerId)
        header = self.getTagOfInterest(containerInfo,headerTag)
        return header[0].text.strip()
    
    def getSeasonDetails(self, headerString):
        # Regex pattern to capture two sets of four digits and the league name
        pattern = r"(\d{4})\s*-\s*(\d{4})\s*(.*)\s+Scores & Fixtures"
        match = re.search(pattern, headerString)
        
        if match:
            # Extract the years and league name
            start_year = match.group(1)
            end_year = match.group(2)
            league_name = match.group(3).strip()
            return start_year, end_year, league_name
        
        # Return None or raise an error if no match is found
        return None
        
    def getContainerInfo(self, containerTag, containerId=None):
        '''Get container info by tag and optional id.'''
        if containerId:
            return self.soupObject.find(containerTag, id=containerId)
        return self.soupObject.find(containerTag)
    
    def getTagOfInterest(self, containerInfo, tagOfInterest):
        print(containerInfo)
        print(tagOfInterest)
        tagList = containerInfo.find_all(tagOfInterest)
        return tagList


    def getSeasonSummary(self, containerInfo = ["div", "info"], tagsOfInterest = ["p", "a", "strong"], 
                         listOfSummaryData = ["Governing Country", "Champion", "Most Goals", "Most Assists", "Most Clean Sheets"]):

        # Initialize dictionary for storing the season summary
        seasonSummaryDictionary = {}

        seasonDetails = self.getSeasonDetails(self.getPageHeader())

        seasonSummaryDictionary["StartYear"] = seasonDetails[0]
        seasonSummaryDictionary["EndYear"] = seasonDetails[1]
        seasonSummaryDictionary["League"] = seasonDetails[2]

        # Get the container (div or other) based on tag and id
        div_info = self.getContainerInfo(containerInfo[0], containerInfo[1])
        if div_info is None:
            return seasonSummaryDictionary  # Return empty dict if no container found

        # Get all tags of interest (e.g., all <p> tags)
        tagList = self.getTagOfInterest(div_info, tagsOfInterest[0])
        
        # Iterate through the tags
        for tag in tagList:
            # Find the strong and a tags within the tag
            strong_tag = tag.find(tagsOfInterest[2])
            a_tag = tag.find(tagsOfInterest[1])

            # Continue only if both strong and a tags are found
            if strong_tag and a_tag and strong_tag.text in listOfSummaryData:
                seasonSummaryDictionary[strong_tag.text] = a_tag.text

        return seasonSummaryDictionary

    def getTableRows(self, tableTag, tableRowTag):
        '''Fetches table rows from the soup object.'''
        table = self.soupObject.find(tableTag)
        if not table:
            return None
        return table.find_all(tableRowTag)
    
    def initializeTableColumns(self, headRow):
        '''Extracts the column names from the header row and initializes the data dictionary.'''
        listOfColumns = [column["data-stat"] for column in headRow]
        dataDict = {column: [] for column in listOfColumns}
        return listOfColumns, dataDict

    def fillDataDict(self, tableRows, listOfColumns, dataDict):
        '''Populate the dataDictionary with row data from the table'''
        for row in tableRows:
            rowData = [column.text.strip() for column in row]
            for i, column in enumerate(listOfColumns):
                dataDict[column].append(rowData[i])

    def readWebsiteTableData(self, tableTag = "tbody", tableRowTag = "tr"):
        '''method that reads table data from a webscraped url and returns a data dictionary ready for conversion to a pandas data frame
        :param: tableTag = 'tbody'
        :param: tableRowTag = "tr"
        :return: dictionary with aggregate list of data per columnn found in a table on a website
        '''
        tableRows = self.getTableRows(tableTag, tableRowTag)
        listOfColumns, dataDict = self.initializeTableColumns(tableRows[0])
        self.fillDataDict(tableRows, listOfColumns, dataDict)

        return dataDict


    


