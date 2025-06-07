import grapher
import graphics
import time
print("hi")
# change at will:
#------------------------------------#
maxSeeds = 10
pageDepth = 50  # doesn't really matter if noOrphans is set to True
pageBreadth = 1
noOrphans = True
scraper = "BeautifulSoup" # Supported: Selenium, BeautifulSoup
language = "English" # Supported: English, French, Chinese, Japanese, Spanish, Latin, Scots
# Note: Non-Latin characters have weird urls so don't display nicely
#------------------------------------#

# initialise stuff
graph = grapher.Graph()
if scraper == "Selenium":
    import selScraper
    duck = selScraper.Scraper(language=language)
else:
    import soupyScraper
    duck = soupyScraper.Scraper(language=language)
sim = graphics.Sim()
sim.setGraph(graph)
duck.setGraph(graph)

# don't change:
running = True
start = time.time()
pagesVisited, SLIndex = 0, 0

# traverse wikipedia
for seed in range(maxSeeds):
    print("\nTRAVERSING---------------", seed)
    duck.exploreLinksAndGraph(duck.getRandomPage(), pageBreadth, pageDepth)

if noOrphans:
    for i in range(500):  # functionally while True
        print("\n\n\nPROCESSING DEAD END NODES", i)
        orphanNodeList = [node for node, links in graph.graphDict.items() if links == set()]
        deadNodes = 0
        for node in orphanNodeList:
            print("\nDEAD END---------------", node[30:], i)
            if duck.exploreLinksAndGraph(node, 1, 10) is None:
                deadNodes += 1
        if len(orphanNodeList) == 0 or len(orphanNodeList) <= deadNodes:
            print("No more orphan nodes to process.", orphanNodeList)
            break

if scraper == "Selenium":
    duck.browser.quit()
graph.generateParentDict()
print("\n\nDONE - generated", len(graph.graphDict), "nodes")
print("Done in", round(time.time() - start, 3), "seconds")
print(round((time.time() - start)/len(graph.graphDict), 3), "seconds per node")
# Generate graph visualization
for node, links in graph.graphDict.items():
    sim.introduceNode(node, links)


# Keep the graphics running in loop
localSelected = "bob"  # ensures update highlight on first loop
while running:
    running = sim.handleEvents()
    sim.updateGraphics()