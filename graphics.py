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
        self.screen = pygame.display.set_mode((self.xMax, self.yMax), pygame.RESIZABLE)
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
        
        self.selected = None            # Currently selected node
        self.renderAllText = False      # Flag to control text rendering
        self.frameCount = 0             # Frame counter for repulsion application
        self.simulation = True          # Flag to control simulation step
        self.collisionsEnabled = False  # Flag to control collision detection
        self.highlightMode = 0          # 0=OFF, 1=weightCol, 2=descendantHighlight

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
            circle.filter = pymunk.ShapeFilter(group=1) # Default to collisions disabled
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
        maxForce = 5000     # maximum repulsion force
        cellSize = 150      # adjust for graph density (optimisation)
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
            if event.type == pygame.VIDEORESIZE:
                self.xMax, self.yMax = event.w, event.h
                self.screen = pygame.display.set_mode((self.xMax, self.yMax), pygame.RESIZABLE)
                self.drawOptions = pymunk.pygame_util.DrawOptions(self.screen)
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.zoom *= 1.1
                elif event.y < 0:
                    self.zoom /= 1.1
            if event.type == pygame.MOUSEBUTTONDOWN:
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
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = None
                elif event.button == 3:
                    self.panStart = None
            if event.type == pygame.MOUSEMOTION:
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
                    self.simulation = not self.simulation
                elif event.key == pygame.K_b: # toggle text rendering
                    self.renderAllText = not self.renderAllText
                elif event.key == pygame.K_c:
                    self.highlightMode = (self.highlightMode + 1) % 3
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
        if name == self.selected:
            return "YELLOW"
        elif name in dataList:
            depth = depthMap.get(name, 0)  # Use .get() to avoid KeyError
            intensity = int((depth / maxDepth) * 255)
            return (255, intensity, intensity)
        else:
            return defaultCol
        
    def computeDescendantCounts(self):
        descendantCounts = {}
        for node in self.bodyDict:
            children = self.graph.getChildren(node)
            descendantCounts[node] = max(0, len(children) - 1)
        return descendantCounts


    def updateGraphics(self):
        self.screen.fill("slategray3")
        self.frameCount += 1
        if self.frameCount % 3 == 0:
            self.applyRepulsion()
        mpX, mpY = self.xMax / 2, self.yMax / 2
        depthMap = {}
        highlightList = []
        if self.highlightMode == 1:  # Direct Parent-based
            parentDict = self.graph.parentDict
            # Reverse the parent count: maxCount - count
            parentCounts = {name: len(parentDict.get(name, set())) for name in self.bodyDict.keys()}
            maxCount = max(parentCounts.values(), default=1)
            depthMap = {name: maxCount - count for name, count in parentCounts.items()}
            highlightList = [name for name, depth in sorted(depthMap.items(), key=lambda item: item[1], reverse=True)]
        elif self.highlightMode == 2:  # ALL Descendant-based
            # Reverse the descendant count: maxCount - count
            descendantCounts = self.computeDescendantCounts()
            maxCount = max(descendantCounts.values(), default=1)
            depthMap = {name: maxCount - count for name, count in descendantCounts.items()}
            highlightList = [name for name, count in sorted(depthMap.items(), key=lambda item: item[1], reverse=True)]
        elif self.highlightMode == 0:  # OFF (selection only)
            if self.selected is not None:
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
            if self.highlightMode == 1: # highlighting arrows doesn't make sense for mode 1
                lineColour = "slategray2"
            else:
                lineColour = self.getColour(sourceName, depthMap, highlightList, defaultCol="slategray2")
            pygame.draw.line(self.screen, lineColour, coords1, coords2, 2)

        # 2. Draw all circles and text
        fontSize = max(10, int(18 * self.zoom))  # Ensure font size is at least 1
        if not hasattr(self, "_cachedFontSize") or self._cachedFontSize != fontSize:
            self.font = pygame.freetype.SysFont(None, fontSize)
            self._cachedFontSize = fontSize
        for name, body in self.bodyDict.items():
            coords = (((body.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            colour = self.getColour(name, depthMap, highlightList)
            pygame.draw.circle(self.screen, colour, coords, int(20 * self.zoom))
            # decide whether node needs to render text
            if self.renderAllText or (self.highlightMode == 0 and (name in highlightList or name == self.selected)) or (self.highlightMode in (1, 2) and (name == self.selected or name in self.graph.getChildren(self.selected))):
                textSurface, rect = self.font.render(name[30:], "BLACK")
                self.screen.blit(textSurface, (coords[0] + 22, coords[1] - 10))
                textSurface, rect = self.font.render(name[30:], "BLACK")
                self.screen.blit(textSurface, (coords[0] + 22, coords[1] - 10))

        # 3. Draw all arrowheads
        for joint in self.jointList:
            coords1 = (((joint.a.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            coords2 = (((joint.b.position - self.offset) - (mpX, mpY)) * self.zoom) + (mpX, mpY)
            sourceName = next((name for name, body in self.bodyDict.items() if body == joint.a), None)
            if self.highlightMode == 1: # arrows don't scale when zooming out - so highlighting arrows by destination mattres more for mode 1
                toName = next((name for name, body in self.bodyDict.items() if body == joint.b), None)
                lineColour = self.getColour(toName, depthMap, highlightList, defaultCol="slategray2")
            else:
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

