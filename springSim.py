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
        self.dragOffset = pygame.Vector2(0, 0)
        self.panStart = None
        self.panOffsetStart = pygame.Vector2(0, 0)

        self.drawOptions = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0, 0
        self.bodyDict = {}
        self.jointList = []

        self.font = pygame.freetype.SysFont(None, 18)
        
        self.selected = None
        self.weightCol = False  # Flag to control weight coloring
        self.collisionsEnabled = True  # Flag to track collision state
        self.renderAllText = True  # Flag to control text rendering
        self.frameCount = 0
        self.simulation = True

    def setGraph(self, graph):
        self.graph = graph

    def createBodyIfNew(self, name, linkedTo=None):
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
            # If body is linked to another, place near the linked body
            if linkedTo and linkedTo in self.bodyDict:
                linkedBody = self.bodyDict[linkedTo]
                offset = pymunk.Vec2d(random.uniform(-500, 500), random.uniform(-500, 500))
                body.position = linkedBody.position + offset

    def introduceNode(self, node, links):
        self.createBodyIfNew(node)
        for link in links:
            self.createBodyIfNew(link, linkedTo=node)
            if node != link:  # Avoid self-loops
                joint = pymunk.constraints.DampedSpring(
                    self.bodyDict[node],
                    self.bodyDict[link],
                    (0, 0), (0, 0),
                    100, 4, 0.3
                )
                self.jointList.append(joint)
                self.space.add(joint)

    def applyRepulsion(self):
        k = 100000          # repulsion constant    
        maxForce = 5000    # maximum repulsion force
        cellSize = 150     # adjust for graph density (optimisation)
        centralK = 20000    # strength of central repulsion
        grid = {}

        # loop 1: assign to grid and compute centre of mass 
        sumPos, count = pymunk.Vec2d(0, 0), 0
        for name, body in self.bodyDict.items():
            cell = (int(body.position.x // cellSize), int(body.position.y // cellSize))
            grid.setdefault(cell, []).append(body)
            sumPos += body.position
            count += 1
        centreOfMass = sumPos / count

        # loop 2: apply repulsion and central force
        for name, body in self.bodyDict.items():
            cell = (int(body.position.x // cellSize), int(body.position.y // cellSize))
            neighborsList = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    neighborCell = (cell[0] + dx, cell[1] + dy)
                    neighborsList.extend(grid.get(neighborCell, []))
            for neighbour in neighborsList:
                if neighbour is body:  # Don't apply repulsion to itself
                    continue
                delta = body.position - neighbour.position
                dist = max(delta.length, 1)
                if dist > cellSize * 2:  # don't bother if node is super far away
                    continue
                direction = delta.normalized() if dist > 0 else pymunk.Vec2d(1, 0)
                force = k / (dist ** 2)
                force = min(force, maxForce)  # Clamp the force
                repulse = direction * force
                body.apply_force_at_world_point(repulse, body.position)
                neighbour.apply_force_at_world_point(-repulse, neighbour.position)

            # Central repulsion
            deltaC = body.position - centreOfMass
            distC = max(deltaC.length, 1)
            directionC = deltaC.normalized() if distC > 0 else pymunk.Vec2d(1, 0)
            forceC = centralK / distC
            repulseC = directionC * forceC
            body.apply_force_at_world_point(repulseC, body.position)

    def getBodyAtPos(self, pos):
        # pos is screen coordinates
        mpX, mpY = self.xMax/2, self.yMax/2
        for name, body in self.bodyDict.items():
            screenPos = ((body.position - self.offset) - (mpX, mpY)) * self.zoom + (mpX, mpY)
            if (pygame.Vector2(screenPos) - pygame.Vector2(pos)).length() < 20 * self.zoom:
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
                    name = self.getBodyAtPos(event.pos)
                    if name:
                        self.dragging = name
                        body = self.bodyDict[name]
                        screenPos = (((body.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
                        self.dragOffset = pygame.Vector2(screenPos) - pygame.Vector2(event.pos)
                        self.selected = name
                    else:
                        self.selected = None
                elif event.button == 3:  # Right click for panning
                    self.panStart = pygame.Vector2(event.pos)
                    self.panOffsetStart = self.offset
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = None
                elif event.button == 3:
                    self.panStart = None
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mousePos = pygame.Vector2(event.pos)
                    newPos = (mousePos + self.dragOffset-(mpX, mpY)) / self.zoom + self.offset + (mpX, mpY)
                    self.bodyDict[self.dragging].position = tuple(newPos)
                    self.bodyDict[self.dragging].velocity = (0, 0)
                elif self.panStart is not None:
                    mousePos = pygame.Vector2(event.pos)
                    delta = (self.panStart - mousePos) / self.zoom
                    self.offset = self.panOffsetStart + delta
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v: # kill momentum of all bodies
                    for name, body in self.bodyDict.items():
                        body.velocity = (0, 0)
                elif event.key == pygame.K_m: # stop collisions
                    self.collisionsEnabled = not self.collisionsEnabled
                    self.updateCollisionFilters()
                elif event.key == pygame.K_n: # freeze simulation
                    if self.simulation: self.simulation = False
                    else:               self.simulation = True
                elif event.key == pygame.K_b: # toggle text rendering
                    if self.renderAllText:  self.renderAllText = False
                    else:                   self.renderAllText = True
                elif event.key == pygame.K_c: # toggle text rendering
                    if self.weightCol:      self.weightCol = False
                    else:                   self.weightCol = True
        return True

    def updateCollisionFilters(self):
        for body in self.bodyDict.values():
            for shape in body.shapes:
                if self.collisionsEnabled:
                    shape.filter = pymunk.ShapeFilter(group=0)  # Enable collisions
                else:
                    shape.filter = pymunk.ShapeFilter(group=1)  # Disable collisions

    def getColour(self, name, depthMap, dataList, defaultCol = "slateblue3"):
        maxDepth = max(depthMap.values(), default=1)
        if self.weightCol:
            depth = depthMap.get(name, 0)
            intensity = int((depth / maxDepth) * 255)
            return (intensity, 100, 255 - intensity)
        if name == self.selected:
            return "YELLOW"
        elif name in dataList:
            depth = depthMap.get(name, 0)  # Use .get() to avoid KeyError
            intensity = int((depth / maxDepth) * 255)
            return (255, intensity, intensity)
        else:
            return defaultCol

    def updateGraphics(self):
        self.screen.fill("slategray3")
        self.frameCount += 1
        if self.frameCount % 3 == 0:
            self.applyRepulsion()
        mpX, mpY = self.xMax / 2, self.yMax / 2

        # Create a depth map for weightCol
        if self.weightCol:
            parentDict = self.graph.parentDict
            depthMap = {name: len(parentDict.get(name, set())) for name in self.bodyDict.keys()}
            highlightList = [name for name, depth in sorted(depthMap.items(), key=lambda item: item[1], reverse=True)]
        elif self.selected is not None:
            highlightList = self.graph.getChildren(self.selected)
            depthMap = {name: depth for depth, name in enumerate(highlightList)}
        else:
            depthMap = {}
            highlightList = []

        # DRAW ORDER:
        # 1. Draw all lines (without arrowheads)
        for joint in self.jointList:
            coords1 = (((joint.a.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            coords2 = (((joint.b.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            sourceName = next((name for name, body in self.bodyDict.items() if body == joint.a), None)
            lineColour = self.getColour(sourceName, depthMap, highlightList, defaultCol="slategray2")
            pygame.draw.line(self.screen, lineColour, coords1, coords2, 2)

        # 2. Draw all circles and text
        fontSize = max(1, int(18 * self.zoom))  # Ensure font size is at least 1
        if not hasattr(self, "_cachedFontSize") or self._cachedFontSize != fontSize:
            self.font = pygame.freetype.SysFont(None, fontSize)
            self._cachedFontSize = fontSize
        for name, body in self.bodyDict.items():
            coords = (((body.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            colour = self.getColour(name, depthMap, highlightList)
            pygame.draw.circle(self.screen, colour, coords, int(20 * self.zoom))
            # decide whether node needs to render text
            if name in highlightList or name == self.selected or self.renderAllText:
                textSurface, rect = self.font.render(name[30:], "BLACK")
                self.screen.blit(textSurface, (coords[0] + 22, coords[1] - 10))

        # 3. Draw all arrowheads
        for joint in self.jointList:
            coords1 = (((joint.a.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            coords2 = (((joint.b.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            sourceName = next((name for name, body in self.bodyDict.items() if body == joint.a), None)
            lineColour = self.getColour(sourceName, depthMap, highlightList, defaultCol="slategray2")
            direction = pygame.Vector2(coords2) - pygame.Vector2(coords1)
            direction.scale_to_length(10)  # Length of the arrowhead
            left = pygame.Vector2(-direction.y, direction.x) * 0.5
            right = pygame.Vector2(direction.y, -direction.x) * 0.5
            arrowTip = pygame.Vector2(coords2)
            pygame.draw.polygon(
                self.screen,
                lineColour,
                [arrowTip, arrowTip - direction + left, arrowTip - direction + right],
            )

        pygame.display.update()
        if self.simulation:
            self.space.step(1 / 60)
            self.clock.tick(60)
