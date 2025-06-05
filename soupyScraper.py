import requests
from bs4 import BeautifulSoup
# remember pip3 install lxml

class Scraper():
    def __init__(self, language = "English") -> None:
        self.language = language
        self.langDict = {"English":  "https://en.wikipedia.org/wiki/Special:Random",
                         "French":   "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard",
                         "Japanese": "https://ja.wikipedia.org/wiki/特別:おまかせ表示",
                         "Spanish":  "https://es.wikipedia.org/wiki/Especial:Aleatoria",
                         "Chinese":  "https://zh.wikipedia.org/wiki/Special:随机页面", # Taiwan style ;)
                         "Latin":    "https://la.wikipedia.org/wiki/Specialis:Pagina_fortuita",
                         "Scots":    "https://sco.wikipedia.org/wiki/Special:Random"} # funny sounding

        #ignore list (manual and mainly english)
        self.ignoreList = ["Old French", "Latin", "Greek", "Ancient Greek", "Grec ancien", "Simplified Chinese characters", "Chinese characters", "Traditional Chinese characters", "Pinyin", "Help:Pronunciation respelling key", "American English", "Espagnol", "Grec (langue)", "language", "langue", "lengua", "言語", "語言"]

    def getRandomPage(self):
        r = requests.get(self.langDict[self.language])
        return r.url

    def getAllLinks(self, site):
        linkStarter = self.langDict[self.language].split("/wiki")[0]
        linkList = []
        r = requests.get(site)
        soup = BeautifulSoup(r.text, "lxml")
        for paragraph in soup.find_all("p"):
            for link in paragraph.find_all("a"): # type: ignore
                if link.get("href") is None or link.find_parent("sup"): # type: ignore
                    continue
                linkList.append(linkStarter + link.get("href")) # type: ignore
        return linkList

    def collectLinks(self, site, breadth=1):
        linkStarter = self.langDict[self.language].split("/wiki")[0]
        linkList = []
        r = requests.get(site)
        soup = BeautifulSoup(r.text, "lxml")
        
        # Iterate through paragraphs and find links
        for paragraph in soup.find_all("p"):
            for link in paragraph.find_all("a"): # type: ignore
                if link.get("href") is None or link.find_parent("sup"): # type: ignore
                    continue
                linkList.append(linkStarter + link.get("href"))  # type: ignore
                if len(linkList) >= breadth:  # Stop once we have enough links
                    return linkList
        return linkList  # Return collected links (may be fewer than breadth if not enough links found)