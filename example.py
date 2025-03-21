#importing the Scrapper Class
from simpleRTScrapper import simpleRTScraper

#loading the url and drive path
myScraper = simpleRTScraper("https://www.rottentomatoes.com/m/iron_man/reviews?type=user", "chromedriver-win64\chromedriver.exe" )

#Start Scrapping
myScraper.beginScrapping()

#Save Reuslts to CSV
myScraper.saveToCSV()

#Print out details about this Scraper Instance
print(myScraper)