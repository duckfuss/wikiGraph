import pygame
import random
import time

class Graph():
    def __init__(self) -> None:
        # directed graph
        self.graphDict = {}
        # pygame boilerplate
        self.xMax, self.yMax = 1280, 720
        self.screen = pygame.display.set_mode((self.xMax,self.yMax))
        self.rects = {}

    def addNode(self, node:str, links:set):
        self.graphDict[node] = links
        xCoord = random.randrange(0,self.xMax)
        yCoord = random.randrange(0,self.yMax)
        self.rects[node] = pygame.Rect(xCoord, yCoord, 10, 10)

    def draw(self):
        for node in self.rects:
            nodeRect = self.rects[node]
            pygame.draw.rect(self.screen, "red", nodeRect)
            for link in self.graphDict[node]:
                linkRect = self.rects[link]
                pygame.draw.line(self.screen, "red", (nodeRect.x, nodeRect.y), (linkRect.x, linkRect.y))
        pygame.event.pump()
        pygame.display.flip()

# test code:
pygame.init()
graphy = Graph()
running = True

graphy.addNode("A", {"B", "C"})
graphy.addNode("B", {"C"})
graphy.addNode("C", {"B", "C"})
graphy.draw()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False