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
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", location)

    def doSearch(self, urlList, ignore):
        self.driver.get("https://google.com")
        search = self.driver.find_element_by_name("q")
        search.send_keys(self.searchInput)
        search.submit()
        return self.searchEngine(urlList= urlList, ignore= ignore)


    def searchEngine(self, urlList, ignore, data = {}):
        try:
            results = self.driver.find_elements_by_css_selector("div.g")
            i = 0
            while i < len(results):
                if results[i].get_attribute("class") == "g":
                    url = results[i].find_elements_by_css_selector("a")[0].get_attribute("href")
                    n = 0
                    ignoreSite = False
                    while n < len(ignore) and ignoreSite is False:
                        if ignore[n] in url:
                            ignoreSite = True
                        n += 1

                    if url not in urlList and ignoreSite is False:
                        self.driver.execute_script("window.open('');")
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.get(url)
                        bodyText = self.driver.find_element_by_tag_name('body').text.lower()
                        data[url] = Tool.analyzeSite(bodyText, self.keywords)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                if i == (len(results) - 1):
                    nextLink = self.driver.find_elements_by_id("pnnext")
                    print(nextLink)
                    if len(nextLink) > 0:
                        nextLink[0].click()
                        self.searchEngine(urlList, ignore, data)
                
                i += 1
            return data
        except Exception as e:
            print(str(e))