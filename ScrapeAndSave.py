from bs4 import BeautifulSoup
import requests

league = "Serie-A"
folder = "seriea"
index = "11"

for year in range(2011, 2024):
    url = f"https://fbref.com/en/comps/{index}/{year}-{year + 1}/schedule/{year}-{year + 1}-{league}-Scores-and-Fixtures"
    
    # Request the page content
    page = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if page.status_code == 200:
        # Create a file name based on the year
        file_name = f"/Users/pkamalian/Desktop/Personal/CS Projects/Futigami/data/{folder}/{league}_{year}_{year+1}.txt"
        
        
        # Write the page content to the file
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(page.text)
        
        print(f"Saved {file_name}")
    else:
        print(f"Failed to retrieve data for {year}-{year+1}")