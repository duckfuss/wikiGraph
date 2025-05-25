import grapher
import scraper
import springSim
import time

def addNode(node, links):
    graph.addNode(node, links)
    sim.introduceNode(node,links)

duck = scraper.Scraper()
graph = grapher.Graph()
sim = springSim.Sim()

startList = [
    "https://en.wikipedia.org/wiki/Duck",
    "https://en.wikipedia.org/wiki/Camptophallus",
    "https://en.wikipedia.org/wiki/Quantum_computing",
    "https://en.wikipedia.org/wiki/Train",
    "https://en.wikipedia.org/wiki/Ascot,_Berkshire",
    "https://en.wikipedia.org/wiki/Rhine_campaign_of_1796",
    "https://en.wikipedia.org/wiki/Ivan_the_Terrible_(polar_bear)",
    "https://en.wikipedia.org/wiki/Taipei",
    "https://en.wikipedia.org/wiki/Sausage"
]
running = True
start = time.time()
pageDepth, pagesVisited, SLIndex = 15, 0, 0
node = startList[SLIndex]

while running:
    if SLIndex < len(startList):
        if pagesVisited >= pageDepth:
            SLIndex += 1
            if SLIndex < len(startList):
                node = startList[SLIndex]
                pagesVisited = 0
                print("-----------------", len(startList), SLIndex)
        if SLIndex < len(startList) and (time.time() - start) > 0.1:
            start = time.time()
            pagesVisited += 1
            links = duck.collectLinks(node, breadth=1)
            addNode(node, links)
            node = links[0] # type: ignore
            print(pagesVisited, node)
    running = sim.updateGraphics()
duck.browser.quit()