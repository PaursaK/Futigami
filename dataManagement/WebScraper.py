import requests
from bs4 import BeautifulSoup
import pandas as pd


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
        self.seasonData = pd.DataFrame(self.readWebsiteTableData())


    def getLeagueHistory(self):
        '''getter method that returns a pandas dataframe of the season results for a given year
        :param: None
        :return: pandas DataFrame
        '''
        return self.seasonData

    def getSeasonSummary(self, containerInfo = ["div", "info"], tagsOfInterest = ["p", "a", "strong"], 
                         listOfSummaryData = ["Governing Country", "Champion", "Most Goals", "Most Assists", "Most Clean Sheets"]):
        
        seasonSummaryDictionary = {}

        div_info = self.soupObject.find(containerInfo[0], id = containerInfo[1])
        tagList = div_info.find_all(tagsOfInterest[0])

        for tag in tagList:
            atag = tag.find(tagsOfInterest[1])
            strongtag = tag.find(tagsOfInterest[2])

            if strongtag == None or atag == None:
                continue
            elif strongtag.text in listOfSummaryData:
                seasonSummaryDictionary[strongtag.text] = atag.text

        return seasonSummaryDictionary
                



    def readWebsiteTableData(self, tableTag = "tbody", tableRowTag = "tr"):
        '''method that reads table data from a webscraped url and returns a data dictionary ready for conversion to a pandas data frame
        :param: tableTag = 'tbody'
        :param: tableRowTag = "tr"
        :return: dictionary with aggregate list of data per columnn found in a table on a website
        
        '''
        tableRows = self.soupObject.find(tableTag).find_all(tableRowTag)

        #list of columns for the website table
        listOfColumns = None
        
        #dictionary for pandas dataframe conversion
        dataDict = {}

        #iterate through the rows found on website table
        for row in tableRows:
            
            #initialize the columns in the pandas dictionaryData
            if listOfColumns == None:
                #grabs all the columns
                listOfColumns = [column["data-stat"] for column in row]
                #for each column initialize a dictionary entry with a list
                for column in listOfColumns:
                    dataDict[column] = []
            
            #per row, collect the data found in each column
            rowData = [column.text for column in row]
            #print(rowData)

            #append row data with respect to column index
            for i in range(len(listOfColumns)):
                dataDict[listOfColumns[i]].append(rowData[i])

        #return data dictionary for panda dataframe integration
        return dataDict
            

url = "https://fbref.com/en/comps/11/2023-2024/schedule/2023-2024-Serie-A-Scores-and-Fixtures"

ws = WebScraper(url)
print("-------Pandas DataFrame Below For 2023-2024 Season---------")
print(ws.getLeagueHistory().head(3))
print(ws.getSeasonSummary())

url = "https://fbref.com/en/comps/9/2022-2023/schedule/2022-2023-Premier-League-Scores-and-Fixtures"

ws1 = WebScraper(url)
print("-------Pandas DataFrame Below For 2022-2023 Season---------")
print(ws1.getLeagueHistory().head(3))
print(ws1.getSeasonSummary())


    


