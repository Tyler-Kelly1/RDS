import requests
from bs4 import BeautifulSoup
import csv
import re


class simpleRTScraper:

    def _getMovieID(self, movieName: str) -> str:
        
        #Helper function for formatting the title
        def firstLetterUpper(input, sep = '_'):
            split = input.split(sep)
            
            fixed = []
            
            for word in split:
                front = word[0]
                back = word[1:]
                front = front.upper()
                
                newWord = front + back
                
                fixed.append(newWord)
            
            return '_'.join(fixed)

        searchUrl = f'https://www.rottentomatoes.com/search?search={movieName}'

        # First we fetch the page data using requsts
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(searchUrl, headers=headers)

        if response.status_code == 200:
        
            # STEP ONE PARSE THE DATA INTO A SOUP USING BEAUTIFUL SOUP
            soup = BeautifulSoup(response.text, "html.parser")

            # Example: Find a div with a specific class
            div_content = soup.find("search-page-media-row", attrs={"data-qa":"data-row"})  # Change class name

            # Extract the movie URL:
            children = div_content.contents


            movieURL = (children[1].attrs)['href']
            
            #Obtaining the moive title
            
            pattern = "/([a-zA-Z_0-9]*)$"
            movieFullName = re.findall(pattern=pattern, string=movieURL)   
            movieFullName = firstLetterUpper(movieFullName[0])

                
                
            

                        
            
        
        else:
            return f"Could Not find movie with name {movieName}"
    

        reviewsURL = f'{movieURL}/reviews?type=user'

        response = requests.get(reviewsURL, headers=headers)
    

        if response.status_code == 200:
            html_content = response.text  # Full HTML of the page

            # STEP ONE PARSE THE DATA INTO A SOUP USING BEAUTIFUL SOUP
            soup = BeautifulSoup(response.text, "html.parser")


            # Example: Find a div with a specific class
            div_content = soup.find("review-flag-modal")

            titleID = div_content.get_attribute_list("emsid")

        else:

            print(f"Failed to retrieve title ID for {movieName}")

        return (movieURL, movieFullName, titleID[0])

    def _mineReviws(self, movieID: str, outputFile: str, batchSize: int):
        """
    Function that mines the reviews from the Rotten Tomatos API Endpoint

    Parameters:
    moiveID: str, moveID can be retrived from the Movies API Endpoint
    outputFile str, name of output CSV
    
    Returns:
    None, Saves data to a "moviename.csv" file
        """

    #Helper Functions

        def parseData(data, reviewList):
            """Helper function for patsing data into the proper output format"""

            for r in data['reviews']:
                reviewList.append([r['quote'], r['rating'] ])

            return
    

        def convertToCSV(fn: str) -> str:
            """Ensures output file name is in the proper format to be saved correctly """

            fn = fn.replace(' ', '_')
        
            if(fn.__contains__(".csv")):
                return fn
        
            return f"{fn}.csv"



        outputFile = convertToCSV(outputFile)

        #API Endpoint base URL
        base_url = f"https://www.rottentomatoes.com/cnapi/movie/{movieID}/reviews/user"
        
        #Column Titles for our output data
        reviews = [['Review', 'Score']]
        
        #Headers for our requst 
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        #API Endpoints params
        params = {"pageCount": batchSize}  # Request 20 reviews

        
        #Cursor used to navigate through review sheets
        endCursor = None

        #Load First Reviews
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            parseData(data, reviews)
            pageinfo = data.get("pageInfo")
            endCursor = pageinfo.get("endCursor")
        else:
            print("Failed to fetch:", response.status_code, response.text)

        step = 100
        
        #begin scraping
        while True:

            if endCursor:
                params["after"] = endCursor
                response = requests.get(base_url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    parseData(data, reviews)
                    pageinfo = data.get("pageInfo")
                    endCursor = pageinfo.get("endCursor")
                    
                    if(len(reviews) - 1 > step): 
                        print(f"Fetched {len(reviews)-1} reviews so far...")
                        step *= 2

            else:
                break    

        with open(outputFile, mode="w", newline="", encoding="utf-8") as file:
            
            #Delcare csv writer
            writer = csv.writer(file)

            # Writing the header and rows
            writer.writerows(reviews)
            
        print(f'{len(reviews)} reviews mined and saved to output!')


        return None

    #Constructor
    def __init__(self, movieName):
        self.moiveURL, self.movieName, self.titleID = self._getMovieID(movieName)
        self.data = None

    def __str__(self):
        output = f"""
Movie Name: {self.movieName}
Movie URL: {self.moiveURL}
Movie ID: {self.titleID}
"""
        return output
    
    def getReviews(self, outputFn: str, batchSize = 20):
        self._mineReviws(self.titleID, outputFn, batchSize = batchSize)
