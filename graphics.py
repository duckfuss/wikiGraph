import pymunk
import pymunk.pygame_util
import pygame


pygame.init()
clock = pygame.time.Clock()
size = 1280, 720
screen = pygame.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)
space = pymunk.Space()

space.gravity = 0,0
b0 = space.static_body
p0 = 100, 200

body1 = pymunk.Body(mass=1, moment=10)
circle1 = pymunk.Circle(body1, radius=30)
body1.position = (400, 350)

body2 = pymunk.Body(mass=1, moment=10)
body2.position = (600, 350)
circle2 = pymunk.Circle(body2, radius=30)
joint = pymunk.constraints.DampedSpring(body1, body2, (0,0), (0, 0), 100, 100, 10)
space.add(body2, circle2, joint, body1, circle1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("GRAY")
    space.debug_draw(draw_options)
    pygame.display.update()
    clock.tick(10)
    space.step(0.01)

pygame.quit()