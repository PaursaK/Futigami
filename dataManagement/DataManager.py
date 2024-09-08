import requests
from bs4 import BeautifulSoup
import pandas as pd


#Plan of Action
    # 1 - Retrieive appropriate table tags in order to engage with the prem league fixture table
    # 2 - translate that data to a pandas data frame

class DataManager:

    def __init__(self, websiteUrl):
        self.url = websiteUrl
        self.page = requests.get(self.url)
        self.soupObject = BeautifulSoup(self.page.text, "html.parser")
        self.seasonData = pd.DataFrame(self.readWebsiteTableData())

    def getSeasonData(self):
        '''getter method that returns a pandas dataframe of the season results for a given year
        :param: None
        :return: pandas DataFrame
        '''
        return self.seasonData


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
            

url = "https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures"

dManager = DataManager(url)
print("-------Pandas DataFrame Below For 2023-2024 Season---------")
print(dManager.getSeasonData().head(3))

url = "https://fbref.com/en/comps/9/2022-2023/schedule/2022-2023-Premier-League-Scores-and-Fixtures"

dManager1 = DataManager(url)
print("-------Pandas DataFrame Below For 2022-2023 Season---------")
print(dManager1.getSeasonData().head(3))

    


