from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class Scraper():
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.set_preference('permissions.default.image', 2) # disable images
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        options.add_argument("-headless") 
        self.browser = webdriver.Firefox(options=options)
        self.ignoreList = ["Old French", "Latin", "Greek", "Ancient Greek", "Simplified Chinese characters", "Chinese characters", "Traditional Chinese characters", "Pinyin", "Help:Pronunciation respelling key"]

    def findNode(self, n=1):
        for i in range(1,10):
            path = "//main/div[3]/div[3]/div[1]/p[" + str(i) + "]/a[" + str(n) + "]"
            try:    return self.browser.find_element(By.XPATH, path)
            except NoSuchElementException:  pass

    def getRandomPage(self):
        self.browser.get("https://en.wikipedia.org/wiki/Special:Random")
        return self.browser.current_url


    def collectLinks(self, site, breadth=2):
        self.browser.get(site)
        linkList = []
        linkNo = 1
        while len(linkList) < breadth:
            html = self.findNode(linkNo)
            if html is None: 
                return linkList
            if html.get_attribute("title") not in self.ignoreList:
                if "language" not in html.get_attribute("title"): # type: ignore
                    link = html.get_attribute("href") # type: ignore
                    linkList.append(link)
            linkNo += 1
        return linkList

    def scrape(self, startSite, depth=3): # unused - main.py controls scraping now
        self.browser.get(startSite)
        for i in range(depth):
            node = self.findNode()
            link = node.get_attribute("href") # type: ignore
            print(i, link.replace("https://en.wikipedia.org/wiki/", "")) # type: ignore
            node.click() # type: ignore
            time.sleep(0.1)
