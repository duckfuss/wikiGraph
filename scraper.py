from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class scraperBot():
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=2560")
        options.add_argument("--height=1440")
        self.browser = webdriver.Firefox(options=options)

    def findNode(self, n=1):
        for i in range(1,10):
            path = "//main/div[3]/div[3]/div[1]/p[" + str(i) + "]/a[" +str(n) + "]"
            try:    return self.browser.find_element(By.XPATH, path)
            except NoSuchElementException:  pass

    def scrape(self, startSite, depth=3):
        self.browser.get(startSite)
        for i in range(depth):
            node = self.findNode()
            link = node.get_attribute("href") # type: ignore
            print(i, link.replace("https://en.wikipedia.org/wiki/", "")) # type: ignore
            node.click() # type: ignore
            time.sleep(0.1)

duck = scraperBot()
duck.scrape("https://en.wikipedia.org/wiki/Duck",10)
