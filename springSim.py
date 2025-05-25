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
        self.zoom = 1
        self.xAdj, self.yAdj = 0, 0
        # pymunk
        self.active_shape = None
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0,0
        self.bodyDict = {}
        self.jointList = []

    def createBodyIfNew(self, name):
        if name not in self.bodyDict.keys():
            body = pymunk.Body(mass=1, moment=10)
            body.position = (random.randrange(400,700),
                             random.randrange(100,600))
            self.bodyDict[name] = body
            circle = pymunk.Circle(body, radius = 20)
            self.space.add(body, circle)

    def introduceNode(self, node, links):
        self.createBodyIfNew(node)
        for link in links:
            self.createBodyIfNew(link)
            joint = pymunk.constraints.DampedSpring(
                self.bodyDict[node],
                self.bodyDict[link],
                (0,0),(0,0),
                200, 2, 10
            )
            self.jointList.append(joint)
            self.space.add(joint)
    
    def pygameDraw(self):
        pass

    def updateGraphics(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.zoom += 1
                elif event.y < 0:
                    self.zoom -= 1

        self.screen.fill("GRAY")
        # self.space.debug_draw(self.draw_options)

        for name in self.bodyDict:
            body = self.bodyDict[name]
            pygame.draw.circle(self.screen, "RED", body.position, 10)
        for joint in self.jointList:
            pygame.draw.line(self.screen,
                             "RED",
                             joint.a.position,
                             joint.b.position,
                             )

        pygame.display.update()
        self.space.step(0.25)
        self.clock.tick(240)
        return True
        
    def printout(self):
        for i in self.bodyDict:
            print(self.bodyDict[i].position)