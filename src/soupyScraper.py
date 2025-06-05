import requests
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, language="English") -> None:
        self.language = language
        self.langDict = {
            "English":  "https://en.wikipedia.org/wiki/Special:Random",
            "French":   "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard",
            "Japanese": "https://ja.wikipedia.org/wiki/特別:おまかせ表示",
            "Spanish":  "https://es.wikipedia.org/wiki/Especial:Aleatoria",
            "Chinese":  "https://zh.wikipedia.org/wiki/Special:随机页面",
            "Latin":    "https://la.wikipedia.org/wiki/Specialis:Pagina_fortuita",
            "Scots":    "https://sco.wikipedia.org/wiki/Special:Random"
        }
        self.ignoreList = [
            "Old French", "Latin", "Greek", "Ancient Greek", "Grec ancien",
            "Simplified Chinese characters", "Chinese characters", "Traditional Chinese characters",
            "Pinyin", "Help:Pronunciation respelling key", "American English", "Espagnol",
            "Grec (langue)", "language", "langue", "lengua", "言語", "語言", "wikt", "Help:", "Play audio"
        ]

    def setGraph(self, graph):
        self.graph = graph

    def getRandomPage(self):
        r = requests.get(self.langDict[self.language])
        return r.url

    def collectLinks(self, site, breadth=1):
        linkStarter = self.langDict[self.language].split("/wiki")[0]
        linkList = []
        r = requests.get(site)
        soup = BeautifulSoup(r.text, "lxml")
        for paragraph in soup.find_all("p"):
            for link in paragraph.find_all("a"): # type: ignore
                if link.get("href") is None or link.find_parent("sup") or link.find_parent("tr") or link.find_parent("span"): # type: ignore
                    # ignore None and superscript (citations)
                    continue
                if link.get("class") and "external" in link.get("class"): # type: ignore
                    # ignore external links
                    continue
                if link.get("title") and any(ig in link.get("title") for ig in self.ignoreList): # type: ignore
                    continue
                linkList.append(linkStarter + link.get("href")) # type: ignore
                if len(linkList) >= breadth:
                    return linkList
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
                if links:   node = links[0]
                else:       return None
                pagesVisited += 1
            else:  # Skip already visited nodes
                print("Skipping already visited page:", node[30:])
                break
        return pagesVisited