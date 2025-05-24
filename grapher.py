import pygame
import random

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
    def draw(self):
        for node in self.graphDict:
            xCoord = random.randrange(0,self.xMax)
            yCoord = random.randrange(0,self.yMax)
            pygame.draw.circle(self.screen, "red", (xCoord, yCoord), 10)

# test code:
pygame.init()
graphy = Graph()
running = True

graphy.addNode("A", {"B", "C"})
graphy.addNode("B", {"B", "C"})

graphy.draw()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    