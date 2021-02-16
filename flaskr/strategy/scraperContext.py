from .scraper import Scraper
from services.tool import Tool
from selenium import webdriver
from .googleSearch import GoogleSearch

class ScraperContext:
    strategy: Scraper = None
    driver = None

    def setDriver(self, driver = "chrome"):
        if driver == "chrome":
            self.driver = webdriver.Chrome(executable_path="flaskr/chromedriver")

    def setEngine(self, engine = "google"):
        if engine == "google":
            self.strategy = GoogleSearch()

        # Default engine
        # if req['engine'] == "yahoo":
            # engine = YahooSearch()

    def setStrategy(self, strategy: Scraper):
        self.strategy = strategy

    def doSearch(self, searchInput, keywords, min_popularity, max_popularity, file = None, location = {}):
        # Tool.createCsv()
        fileData = []
        if file is not None:
            fileData = Tool.readFile(file)
        self.strategy.setDriver(driver= self.driver)
        self.strategy.setSearchInputKeywords(searchInput= searchInput, keywords= keywords)
        self.strategy.setLocation(location)
        data = self.strategy.doSearch(fileData)
        data = Tool.getAlexaRank(data, min_popularity, max_popularity)
        return data

