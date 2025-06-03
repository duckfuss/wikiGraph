import grapher
import scraper
import springSim
import time

duck = scraper.Scraper()
graph = grapher.Graph()
sim = springSim.Sim()
sim.setGraph(graph)

# don't change:
running = True
start = time.time()
pagesVisited, SLIndex = 0, 0

# change at will:
#------------------------------------#
maxSeeds = 50
pageDepth = 10  # doesn't really matter if noOrphans is set to True
pageBreadth = 1
noOrphans = True
lanugage = "English" # Supported: English, French, Chinese, Japanese, Spanish, Latin, Scots
# Note: Non-Latin characters have weird urls so don't display nicely
#------------------------------------#

def exploreLinksAndGraph(startSite, breadth, depth):
    pagesVisited = 0
    node = startSite
    graph.addNode(node, set())
    print("startSite:", startSite)
    while pagesVisited < depth:
        if graph.graphDict[node] == set():  # If node's new
            print(pagesVisited, node[30:])
            links = duck.collectLinks(node, breadth=breadth)
            graph.addNode(node, links) # type: ignore
             # abort if cannot find a follow-on link:
            if links:   node = links[0] 
            else:       return None
            pagesVisited += 1
        else:  # Skip already visited nodes
            print("Skipping already visited page:", node[30:])
            return pagesVisited
    return pagesVisited # never used, but could be useful for debugging

# traverse wikipedia
for seed in range(maxSeeds):
    print("\nTRAVERSING---------------", seed)
    exploreLinksAndGraph(duck.getRandomPage(language=lanugage), pageBreadth, pageDepth)

if noOrphans:
    for i in range(500): # functionally while True
        print("\n\n\nPROCESSING DEAD END NODES", i)
        orphanNodeList = [node for node, links in graph.graphDict.items() if links == set()]
        deadNodes = 0
        for node in orphanNodeList:
            print("\nDEAD END---------------", node[30:], i)
            if exploreLinksAndGraph(node, 1, 10) is None:   deadNodes += 1
        if len(orphanNodeList) == 0 or len(orphanNodeList) <= deadNodes:
            print("No more orphan nodes to process.", orphanNodeList)
            break

duck.browser.quit()
graph.generateParentDict()
print("DONE - generated", len(graph.graphDict), "nodes")

# Generate graph visualizationx
for node, links in graph.graphDict.items():
    sim.introduceNode(node, links)

# Keep the graphics running in loop
localSelected = "bob" # ensures update highlight on first loop
while running:
    running = sim.handleEvents()
    sim.updateGraphics()