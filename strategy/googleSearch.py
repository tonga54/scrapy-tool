from .scraper import Scraper
from services.tool import Tool

class GoogleSearch(Scraper):
    driver = None
    searchInput = ""
    keywords = ""

    def setDriver(self, driver):
        self.driver = driver

    def setSearchInputKeywords(self, searchInput, keywords):
        self.searchInput = searchInput
        self.keywords = keywords

    def setLocation(self, location = {}):
        pass
        # self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", location)

    def doSearch(self, urlList):
        self.driver.get("https://google.com")
        search = self.driver.find_element_by_name("q")
        search.send_keys(self.searchInput)
        search.submit()
        return self.searchEngine(urlList= urlList)


    def searchEngine(self, urlList, data = {}):
        try:
            results = self.driver.find_elements_by_css_selector("div.g")
            i = 0
            while i < len(results):
                if results[i].get_attribute("class") == "g":
                    url = results[i].find_elements_by_css_selector("a")[0].get_attribute("href")
                    if url not in urlList:
                        self.driver.get(url)
                        bodyText = self.driver.find_element_by_tag_name('body').text.lower()
                        data[url] = Tool.analyzeSite(url, bodyText, self.keywords)
                        Tool.goToPreviousPage(self.driver)
                        results = self.driver.find_elements_by_css_selector("div.g")

                if (i+1) == len(results):
                    nextLink = self.driver.find_elements_by_id("pnnext")
                    if len(nextLink) > 0:
                        nextLink[0].click()
                        self.searchEngine(urlList, data)
                
                i += 1
            return data
        except Exception as e:
            print(str(e))