import grapher
import scraper
import springSim
import time

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
    "https://en.wikipedia.org/wiki/Sausage",
    "https://en.wikipedia.org/wiki/Special:Random"
]
#for i in range(50):
#    startList.append("https://en.wikipedia.org/wiki/Special:Random")
running = True
start = time.time()
pageDepth, pagesVisited, SLIndex = 20, 0, 0
node = startList[SLIndex]
graph.addNode(node, set())


while SLIndex < len(startList):
    if pagesVisited >= pageDepth:
        SLIndex += 1
        if SLIndex < len(startList):
            node = startList[SLIndex]
            graph.addNode(node, set())
            pagesVisited = 0
            print("-----------------", len(startList), SLIndex)

    if graph.graphDict[node] == set():  # If the node hasn't been visited
        links = duck.collectLinks(node, breadth=1)
        graph.addNode(node, links)  # type: ignore
        node = links[0]
        print(pagesVisited, node)
        pagesVisited += 1
    else:  # Skip already visited nodes
        print(f"Skipping already visited page: {node}")
        pagesVisited += pageDepth  # Ensure program moves on to the next start word

duck.browser.quit()

# Generate graph visualization
for node, links in graph.graphDict.items():
    sim.introduceNode(node, links)

# Keep the graphics running in a loop
while running:
    running = sim.updateGraphics()