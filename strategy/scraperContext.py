from .scraper import Scraper
from services.tool import Tool
from selenium import webdriver
from .googleSearch import GoogleSearch
import os

class ScraperContext:
    strategy: Scraper = None
    driver = None

    def setDriver(self, driver = "chrome"):
        if driver == "chrome":
            # PROD
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            # chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument("--no-sandbox")
            # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            
            # DEV
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("disable-gpu")
            self.driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options= options)

    def setEngine(self, engine = "google"):
        if engine == "google":
            self.strategy = GoogleSearch()

        # Default engine
        # if req['engine'] == "yahoo":
            # engine = YahooSearch()

    def setStrategy(self, strategy: Scraper):
        self.strategy = strategy

    def doSearch(self, searchInput, keywords, min_popularity, max_popularity, ignore = [], file = None, location = {}):
        fileData = []
        if file is not None:
            fileData = Tool.readFile(file)
        self.strategy.setDriver(driver= self.driver)
        self.strategy.setSearchInputKeywords(searchInput= searchInput, keywords= keywords)
        self.strategy.setLocation(location)
        data = self.strategy.doSearch(fileData, ignore= ignore)
        data = Tool.getAlexaRank(data, min_popularity, max_popularity)
        return data

