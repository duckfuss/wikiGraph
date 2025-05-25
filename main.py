import grapher
import scraper
import springSim
import time

duck = scraper.Scraper()
graph = grapher.Graph()
sim = springSim.Sim()

# don't change:
running = True
start = time.time()
pagesVisited, SLIndex = 0, 0
# change at will:
maxSeeds = 15
pageDepth = 20
pageBreadth = 2

# initialise start node
node = duck.getRandomPage()
graph.addNode(node, set())

while SLIndex < maxSeeds:
    if pagesVisited >= pageDepth:
        SLIndex += 1
        if SLIndex < maxSeeds:
            node = duck.getRandomPage()
            graph.addNode(node, set())
            pagesVisited = 0
            print("-----------------", SLIndex)
    if graph.graphDict[node] == set():  # If node's new
        print(pagesVisited, node)
        links = duck.collectLinks(node, breadth=pageBreadth)
        graph.addNode(node, links) #type: ignore
        if links:   node = links[0]
        else:       pagesVisited += pageDepth
        pagesVisited += 1
    else:  # Skip already visited nodes
        print(f"Skipping already visited page: {node}")
        pagesVisited += pageDepth  # Ensure program moves on to the next start word

duck.browser.quit()
print("DONE - generated", len(graph.graphDict), "nodes")
# Generate graph visualization
for node, links in graph.graphDict.items():
    sim.introduceNode(node, links)

# Keep the graphics running in loop
while running:
    running = sim.updateGraphics()
