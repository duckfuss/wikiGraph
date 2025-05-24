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
        self.active_shape = None
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0,0
        self.bodyDict = {}
        self.circleList = []
        self.joingList = []

    def createBodyIfNew(self, name):
        if name not in self.bodyDict.keys():
            body = pymunk.Body(mass=1, moment=10)
            body.position = (random.randrange(400,700),
                             random.randrange(100,600))
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
                200, 2, 10
            )
            self.space.add(joint)
    
    def updateGraphics(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p = pymunk.pygame_util.from_pygame(event.pos, self.screen)
                self.active_shape = None
                for s in self.space.shapes:
                    dist = s.point_query(p)[2]
                    if dist < 0:
                        self.active_shape = s
                        self.pulling = True
                        s.body.angle = (p - s.body.position).angle

            elif event.type == pygame.MOUSEMOTION:
                self.p = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.pulling:
                    self.pulling = False
                    b = self.active_shape.body # type: ignore
                    p0 = b.position
                    p1 = pymunk.pygame_util.from_pygame(event.pos, self.screen)
                    impulse = 0.1 * (p1 - p0).rotated(b.angle)
                    b.apply_impulse_at_local_point(impulse)


        self.screen.fill("GRAY")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        self.space.step(0.25)
        self.clock.tick(240)
        return True
        
    def printout(self):
        for i in self.bodyDict:
            print(self.bodyDict[i].position)