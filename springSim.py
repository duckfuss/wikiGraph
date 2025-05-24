import pymunk
import pymunk.pygame_util
import pygame
import random

class Sim():
    def __init__(self) -> None:
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

pygame.init()
clock = pygame.time.Clock()
size = 1280, 720
screen = pygame.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)
sim = Sim()


sim.introduceNode("A", {"B", "C"})
sim.introduceNode("B", {"C"})
sim.introduceNode("C", {"B", "A"})
sim.introduceNode("D", {})
sim.introduceNode("E", {"D", "F"})
sim.introduceNode("F", {"E", "G"})
sim.introduceNode("G", {"D", "F"})



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("GRAY")
    sim.space.debug_draw(draw_options)
    pygame.display.update()
    clock.tick(60)
    sim.space.step(0.01)

pygame.quit()