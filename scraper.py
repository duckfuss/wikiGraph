from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

class scraperBot():
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=2560")
        options.add_argument("--height=1440")
        self.browser = webdriver.Firefox(options=options)

    def scrape(self, site, depth=3):
        self.browser.get(site)
        for i in range(depth):
            print("----------depth:", i)
            link = self.findLink()
            link.click() # type: ignore
            time.sleep(1)

    def findLink(self, n=1):
        for i in range(1,10):
            path = "//main/div[3]/div[3]/div[1]/p[" + str(i) + "]/a[" +str(n) + "]"
            try:
                return self.browser.find_element(By.XPATH, path)
            except NoSuchElementException:
                print("it wasn't i =", i)


duck = scraperBot()
duck.scrape("https://en.wikipedia.org/wiki/Duck",10)

#.mw-content-ltr > p:nth-child(9) > a:nth-child(2)
#.mw-content-ltr > p:nth-child(5) > a:nth-child(2)
#/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]/a[1]
#/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[3]/a[1]
#/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]/a[1]