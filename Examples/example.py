#importing the Scrapper Class
from Classes.simpleRTScrapper import simpleRTScraper

myScraper = simpleRTScraper("Electric State")

print(myScraper)

myScraper.getReviews("Electic State Reviews", 50)

