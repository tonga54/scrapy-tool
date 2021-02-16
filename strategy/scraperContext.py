from .scraper import Scraper
from services.tool import Tool
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from .googleSearch import GoogleSearch

class ScraperContext:
    strategy: Scraper = None
    driver = None

    def setDriver(self, driver = "chrome"):
        if driver == "chrome":
            GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
            CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver' 

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.binary_location = GOOGLE_CHROME_PATH
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path= CHROMEDRIVER_PATH)

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

