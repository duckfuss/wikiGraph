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

node = "https://en.wikipedia.org/wiki/Duck"
running = True
start = time.time()
while running:
    if time.time() - start > 1:
        start = time.time()
        links = duck.collectLinks(node)
        addNode(node, links)
        print(links)
        node = links[0] # type: ignore
    running = sim.updateGraphics()
    