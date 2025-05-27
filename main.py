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
maxSeeds = 1
pageDepth = 20
pageBreadth = 2

# initialise start node
node = duck.getRandomPage()
graph.addNode(node, set())

def exploreLinksAndGraph(startSite, breadth, depth):
    pagesVisited = 0
    node = startSite
    graph.addNode(node, set())
    while pagesVisited < depth:
        if graph.graphDict[node] == set():  # If node's new
            print(pagesVisited, node)
            links = duck.collectLinks(node, breadth=breadth)
            graph.addNode(node, links) #type: ignore
             # abort if cannot find a follow-on link:
            if links:   node = links[0] 
            else:       return
            pagesVisited += 1
        else:  # Skip already visited nodes
            print(f"Skipping already visited page: {node}")
            pagesVisited += pageDepth  # Ensure program moves on to the next start word

# traverse wikipedia
for seed in range(maxSeeds):
    print("TRAVERSING---------------", seed)
    exploreLinksAndGraph(duck.getRandomPage(), pageBreadth, pageDepth)

print("PROCESSING DEAD END NODES")
# complete dead ends
dead_end_nodes = [node for node, links in graph.graphDict.items() if links == set()]
for node in dead_end_nodes:
    print("DEAD_END---------------", node)
    exploreLinksAndGraph(node, 1, 10)

print("PROCESSING DEAD END NODES again")
# complete dead ends
dead_end_nodes = [node for node, links in graph.graphDict.items() if links == set()]
for node in dead_end_nodes:
    print("DEAD_END2---------------", node)
    exploreLinksAndGraph(node, 1, 10)

duck.browser.quit()
print("DONE - generated", len(graph.graphDict), "nodes")
# Generate graph visualization
for node, links in graph.graphDict.items():
    sim.introduceNode(node, links)

# Keep the graphics running in loop
while running:
    running = sim.handleEvents()
    if sim.selected is not None:
        highlight = graph.getChildren(sim.selected)
    else:
        highlight = set()
    sim.updateGraphics(highlight)