#importing the Scrapper Class
#Ensure that the class and example file are in the same directory
from classes.simpleRTScrapper import simpleRTScraper

#Creating a Scraper object
myScraper = simpleRTScraper("Electric State")

#Displaying Info about scrapper
print(myScraper)

#Scrapping the Reviews and outputting the reviews to a CSV file
myScraper.getReviews("Electic State Reviews", 50)

