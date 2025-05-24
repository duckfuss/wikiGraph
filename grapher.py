import pygame
import springSim
import random
import time

class Graph():
    def __init__(self) -> None:
        # directed graph
        self.graphDict = {}
        # graphics boilerplate
        self.sim = springSim.Sim()
        self.xMax, self.yMax = 1280, 720
        self.screen = pygame.display.set_mode((self.xMax,self.yMax))

    def addNode(self, node:str, links:set):
        # add links to node if node is new
        if node not in self.graphDict.keys():
            self.graphDict[node] = links
        # updates a seen node's links
        else:
            self.graphDict[node].update(links)
        # add any implicit linked nodes that aren't in graph dict
        for link in links:
            if link not in self.graphDict.keys():
                self.graphDict[link] = set()

    def draw(self):
        
            for link in self.graphDict[node]:
                linkRect = self.rects[link]
                pygame.draw.line(
                    self.screen, "red", 
                    (nodeRect.x, nodeRect.y), 
                    (linkRect.x, linkRect.y))
            pygame.event.pump()
            pygame.display.flip()
    
    
'''
# test code:
pygame.init()
graphy = Graph()
running = True

graphy.addNode("A", {"B", "C"})
graphy.addNode("C", {"B", "C"})
graphy.addNode("D", {"B", "A"})

graphy.draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
'''