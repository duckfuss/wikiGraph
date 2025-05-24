import grapher
import scraper
import springSim

graph = grapher.Graph()
sim = springSim.Sim()
sim.introduceNode("A", {"B", "C"})

running = True
while running:
    running = sim.updateGraphics()