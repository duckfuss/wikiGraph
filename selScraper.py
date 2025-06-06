from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Scraper():
    def __init__(self, language) -> None:
        options = webdriver.FirefoxOptions()
        options.set_preference('permissions.default.image', 2) # disable images
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        options.add_argument("-headless") # comment out to see the scraping window
        self.browser = webdriver.Firefox(options=options)
        self.language = language
        #ignore list (manual and mainly english)
        self.ignoreList = ["Old French", "Latin", "Greek", "Ancient Greek", "Grec ancien", "Simplified Chinese characters", "Chinese characters", "Traditional Chinese characters", "Pinyin", "Help:Pronunciation respelling key", "American English", "Espagnol", "Grec (langue)", "language", "langue", "lengua", "言語", "語言"]

    def setGraph(self,graph):
        self.graph = graph

    def findNode(self, n=1):
        for i in range(1,10):
            path = "//main/div[3]/div[3]/div[1]/p[" + str(i) + "]/a[" + str(n) + "]"
            try:    return self.browser.find_element(By.XPATH, path)
            except NoSuchElementException:  pass

    def getRandomPage(self):
        langDict = {"English":  "https://en.wikipedia.org/wiki/Special:Random",
                    "French":   "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard",
                    "Japanese": "https://ja.wikipedia.org/wiki/特別:おまかせ表示",
                    "Spanish":  "https://es.wikipedia.org/wiki/Especial:Aleatoria",
                    "Chinese":  "https://zh.wikipedia.org/wiki/Special:随机页面", # Taiwan style ;)
                    "Latin":    "https://la.wikipedia.org/wiki/Specialis:Pagina_fortuita",
                    "Scots":    "https://sco.wikipedia.org/wiki/Special:Random"} # funny sounding
        self.browser.get(langDict[self.language])
        return self.browser.current_url

    def collectLinks(self, site, breadth=2):
        self.browser.get(site)
        linkList = []
        linkNo = 1
        while len(linkList) < breadth:
            html = self.findNode(linkNo)
            if html is None or html.get_attribute("href") is None: 
                return linkList
            if not any(ig in html.get_attribute("title") for ig in self.ignoreList): # type: ignore
                link = html.get_attribute("href") # type: ignore
                linkList.append(link)
            linkNo += 1
        return linkList
    
    def exploreLinksAndGraph(self, startSite, breadth, depth):
        pagesVisited = 0
        node = startSite
        self.graph.addNode(node, set())
        print("startSite:", startSite)
        while pagesVisited < depth:
            if self.graph.graphDict[node] == set():  # If node's new
                print(pagesVisited, node[30:])
                links = self.collectLinks(node, breadth=breadth)
                self.graph.addNode(node, links)
                # Abort if cannot find a follow-on link:
                if links:   
                    node = links[0]
                else:       
                    return None
                pagesVisited += 1
            else:  # Skip already visited nodes
                print("Skipping already visited page:", node[30:])
                break
        return pagesVisited