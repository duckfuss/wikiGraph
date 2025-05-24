import pymunk
import pymunk.pygame_util
import pygame
import random

class Sim():
    def __init__(self) -> None:
        # pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.xMax, self.yMax = 1280, 720
        self.screen = pygame.display.set_mode((self.xMax,self.yMax))
        # pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0,0
        self.bodyDict = {}
        self.circleList = []
        self.joingList = []

    def createBodyIfNew(self, name):
        if name not in self.bodyDict.keys():
            body = pymunk.Body(mass=1, moment=10)
            body.position = (random.randrange(500,600),
                             random.randrange(250,350))
            self.bodyDict[name] = body
            circle = pymunk.Circle(body, radius = 20)
            self.circleList.append(circle)
            self.space.add(body, circle)

    def introduceNode(self, node, links):
        self.createBodyIfNew(node)
        for link in links:
            self.createBodyIfNew(link)
            joint = pymunk.constraints.DampedSpring(
                self.bodyDict[node],
                self.bodyDict[link],
                (0,0),(0,0),
                200, 100, 10
            )
            self.space.add(joint)
    
    def updateGraphics(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.screen.fill("GRAY")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        self.space.step(0.1)
        self.clock.tick(60)
        return True
        
    def printout(self):
        for i in self.bodyDict:
            print(self.bodyDict[i].position)
