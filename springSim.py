import pymunk
import pymunk.pygame_util
import pygame
import pygame.freetype
import random

class Sim():
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.xMax, self.yMax = 1280, 720
        self.screen = pygame.display.set_mode((self.xMax, self.yMax))
        self.zoom = 1
        self.offset = pygame.Vector2(0, 0)
        self.dragging = None
        self.drag_offset = pygame.Vector2(0, 0)
        self.selected = None
        self.pan_start = None
        self.pan_offset_start = pygame.Vector2(0, 0)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0, 0
        self.bodyDict = {}
        self.jointList = []

        self.font = pygame.freetype.SysFont(None, 18)

        self.collisions_enabled = True  # Flag to track collision state

    def createBodyIfNew(self, name, linked_to=None):
        if name not in self.bodyDict.keys():
            body = pymunk.Body(mass=1, moment=100)
            body.position = (random.randrange(300, 800), random.randrange(50, 650))
            self.bodyDict[name] = body
            circle = pymunk.Circle(body, radius=20)
            circle.elasticity = 0.9
            circle.friction = 0.5
            circle.filter = pymunk.ShapeFilter(group=0)  # Default to collisions enabled
            circle.colour = pygame.Color("red")
            self.space.add(body, circle)
            self.simulation = True
            # If body is linked to another, place near the linked body
            if linked_to and linked_to in self.bodyDict:
                linked_body = self.bodyDict[linked_to]
                offset = pymunk.Vec2d(random.uniform(-500, 500), random.uniform(-500, 500))
                body.position = linked_body.position + offset

    def introduceNode(self, node, links):
        self.createBodyIfNew(node)
        for link in links:
            self.createBodyIfNew(link, linked_to=node)
            joint = pymunk.constraints.DampedSpring(
                self.bodyDict[node],
                self.bodyDict[link],
                (0, 0), (0, 0),
                100, 4, 0.3
            )
            self.jointList.append(joint)
            self.space.add(joint)

    def apply_repulsion(self):
        k = 100000  # repulsion constant
        bodies = list(self.bodyDict.values())
        for i, body1 in enumerate(bodies):
            for body2 in bodies[i+1:]:
                delta = body1.position - body2.position
                dist = max(delta.length, 1)
                direction = delta.normalized() if dist > 0 else pymunk.Vec2d(1, 0)
                force = k / (dist ** 2)
                repulse = direction * force
                # Apply equal and opposite forces
                body1.apply_force_at_world_point(repulse, body1.position)
                body2.apply_force_at_world_point(-repulse, body2.position)

    def get_body_at_pos(self, pos):
        # pos is screen coordinates
        mpX, mpY = self.xMax/2, self.yMax/2
        for name, body in self.bodyDict.items():
            screen_pos = ((body.position - self.offset) - (mpX, mpY)) * self.zoom + (mpX, mpY)
            if (pygame.Vector2(screen_pos) - pygame.Vector2(pos)).length() < 20 * self.zoom:
                return name
        return None

    def handleEvents(self):
        mpX, mpY = self.xMax/2, self.yMax/2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.zoom *= 1.1
                elif event.y < 0:
                    self.zoom /= 1.1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    name = self.get_body_at_pos(event.pos)
                    if name:
                        self.dragging = name
                        body = self.bodyDict[name]
                        screen_pos = (((body.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
                        self.drag_offset = pygame.Vector2(screen_pos) - pygame.Vector2(event.pos)
                        self.selected = name
                    else:
                        self.selected = None
                elif event.button == 3:  # Right click for panning
                    self.pan_start = pygame.Vector2(event.pos)
                    self.pan_offset_start = self.offset
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = None
                elif event.button == 3:
                    self.pan_start = None
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_pos = pygame.Vector2(event.pos)
                    new_pos = (mouse_pos + self.drag_offset-(mpX, mpY)) / self.zoom + self.offset + (mpX, mpY)
                    self.bodyDict[self.dragging].position = tuple(new_pos)
                    self.bodyDict[self.dragging].velocity = (0, 0)
                elif self.pan_start is not None:
                    mouse_pos = pygame.Vector2(event.pos)
                    delta = (self.pan_start - mouse_pos) / self.zoom
                    self.offset = self.pan_offset_start + delta
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # kill momentum of all bodies
                    for name, body in self.bodyDict.items():
                        body.velocity = (0, 0)
                elif event.key == pygame.K_m: # stop collisions
                    self.collisions_enabled = not self.collisions_enabled
                    self.update_collision_filters()
                elif event.key == pygame.K_n: # freeze simulation
                    if self.simulation:
                        self.simulation = False
                    else:
                        self.simulation = True
        return True

    def update_collision_filters(self):
        for body in self.bodyDict.values():
            for shape in body.shapes:
                if self.collisions_enabled:
                    shape.filter = pymunk.ShapeFilter(group=0)  # Enable collisions
                else:
                    shape.filter = pymunk.ShapeFilter(group=1)  # Disable collisions

    def getColour(self, name, depth_map, max_depth, highlightList, defaultCol = "slateblue3"):
        if name == self.selected:
            return "YELLOW"
        elif name in highlightList:
            depth = depth_map[name]
            intensity = int((depth / max_depth) * 255)  # Lower depth = lower intensity
            return (255, intensity, intensity)  # Gradient red color
        else:
            return defaultCol

    def updateGraphics(self, highlightList=[]):
        self.screen.fill("slategray3")
        self.apply_repulsion()
        mpX, mpY = self.xMax / 2, self.yMax / 2

        # Create a depth map for the highlight list
        depth_map = {name: depth for depth, name in enumerate(highlightList)}
        max_depth = max(depth_map.values(), default=1)

        for name, body in self.bodyDict.items():
            coords = (((body.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)

            # Get the node color using the helper function
            colour = self.getColour(name, depth_map, max_depth, highlightList)

            # Draw the node
            pygame.draw.circle(self.screen, colour, coords, int(20 * self.zoom))

            # Render the label
            font_size = int(18 * self.zoom)
            self.font.size = font_size
            text_surface, rect = self.font.render(
                name.replace("https://en.wikipedia.org/wiki/", ""), "BLACK"
            )
            self.screen.blit(text_surface, (coords[0] + 22, coords[1] - 10))

        # Draw connections (lines and arrowheads)
        for joint in self.jointList:
            coords1 = (((joint.a.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            coords2 = (((joint.b.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)

            # Get the line color using the helper function
            source_name = next((name for name, body in self.bodyDict.items() if body == joint.a), None)
            line_colour = self.getColour(source_name, depth_map, max_depth, highlightList, defaultCol="slategray2")

            # Draw the line
            pygame.draw.line(self.screen, line_colour, coords1, coords2, 2)

            # Draw the arrowhead
            direction = pygame.Vector2(coords2) - pygame.Vector2(coords1)
            direction.scale_to_length(10)  # Length of the arrowhead
            left = pygame.Vector2(-direction.y, direction.x) * 0.5
            right = pygame.Vector2(direction.y, -direction.x) * 0.5
            arrow_tip = pygame.Vector2(coords2)
            pygame.draw.polygon(
                self.screen,
                line_colour,
                [arrow_tip, arrow_tip - direction + left, arrow_tip - direction + right],
            )

        pygame.display.update()
        if self.simulation:
            self.space.step(1 / 60)
            self.clock.tick(240)