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
pageDepth, n = 2, 0
while running:
    if (time.time() - start) > 0.1 and n < pageDepth:
        start = time.time()
        n += 1
        links = duck.collectLinks(node)
        addNode(node, links)
        print(links)
        node = links[0] # type: ignore

    running = sim.updateGraphics()
duck.browser.quit()