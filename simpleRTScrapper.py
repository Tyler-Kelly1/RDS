from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import re
import time


class simpleRTScraper:
    
    #Constructor
    def __init__(self, url, chromeDirverPath, intialLoadTime = 2, scrapeFullPage = False, depthLevel = 3):
        self.url = url
        self.driverPath = chromeDirverPath
        self.startTime = intialLoadTime
        self.scrapeFullPage = scrapeFullPage
        self.depthLevel = depthLevel
        self.data = None

    def __str__(self):
        output = f"""
Url: {self.url}
Driver Path: {self.driverPath}
Intial Load Time: {self.startTime}
Depth Level: {self.depthLevel}
Scrape Full Page: {self.scrapeFullPage}
"""
        return output

    def setOption(self, option, value):
        if hasattr(self,option):
            print(f'Updated {option} to {value}')
            setattr(self,option,value)
        else:
            print("Invalid option")

        return
    
    def beginScrapping(self):

        # Set up Selenium WebDriver

        service = Service(self.driverPath)
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 10)

        # Open the Rotten Tomatoes reviews page
        url = self.url
        driver.get(url)

        #Load Page
        time.sleep(self.startTime)

        # Find the "Load More" button (Check page source for actual class name)
        load_more_button = driver.find_element(By.XPATH, "//rt-button[@data-qa='load-more-btn']")


        #Beging Scraping either full page or to a certain depth
        if(self.scrapeFullPage):

            while True:
                    try:
                        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//rt-button[@data-qa='load-more-btn']")))
                        load_more_button.click()
                    except Exception:
                        break
        else:

            i = 0
            while(i < self.depthLevel):
                    try:
                        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//rt-button[@data-qa='load-more-btn']")))
                        load_more_button.click()
                    except Exception:
                        break

        #Get the pages data
        html = driver.page_source
        
        #Close the Driver
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
       
        # Example: Extract review quotes
        reviews = soup.find_all("p", class_="audience-reviews__review")
        ratings = soup.find_all("rating-stars-group")


        #Lets zip these bad boys on up togehter
        labeledReviews = [["Review", "Score_0-5"]]

        for review, rating in zip(reviews, ratings):
            labeledReviews.append([review.text.strip(), rating.get_attribute_list("score")[0]])

        print(f'Number of Reviews Mined: {len(labeledReviews)}')

        self.data = labeledReviews

        return
    
    def saveToCSV(self, outputFN = ""):
         
        if(self.data is None):
            print("Scrapper has scrapped no data yet!")
            return False
         
        #knabs movie title for output file name
        titlePattern = r"(?<=/m/)([a-zA-Z0-9_]+)"

        match = re.search(titlePattern, self.url)
        extension = ''

        if match:
            extension = match.group(0)
        else:
            extension = ''

        fn = outputFN + "_" + extension + ".csv"

        # Writing to a CSV file
        with open(fn, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
    
            # Writing the header and rows
            writer.writerows(self.data)

        print("CSV file created successfully!")

        return True
        

    


        




         








    
