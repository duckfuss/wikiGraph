import pygame
import springSim
import random
import time

class Graph():
    def __init__(self) -> None:
        # directed graph
        self.graphDict = {}

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