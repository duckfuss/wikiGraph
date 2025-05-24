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
while running:
    running = sim.updateGraphics()
    links = duck.collectLinks(node)
    addNode(node, links)
    print(links)
    node = links[0] # type: ignore