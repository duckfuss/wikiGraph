from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class Scraper():
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        self.browser = webdriver.Firefox(options=options)

    def findNode(self, n=1):
        for i in range(1,10):
            path = "//main/div[3]/div[3]/div[1]/p[" + str(i) + "]/a[" + str(n) + "]"
            try:    return self.browser.find_element(By.XPATH, path)
            except NoSuchElementException:  pass

    def collectLinks(self, site, depth=2):
        self.browser.get(site)
        linkList = []
        for i in range(1, depth+1):
            html = self.findNode(i)
            link = html.get_attribute("href") # type: ignore
            linkList.append(link)
        return linkList

    def scrape(self, startSite, depth=3): # unused - main.py controls scraping
        self.browser.get(startSite)
        for i in range(depth):
            node = self.findNode()
            link = node.get_attribute("href") # type: ignore
            print(i, link.replace("https://en.wikipedia.org/wiki/", "")) # type: ignore
            node.click() # type: ignore
            time.sleep(0.1)