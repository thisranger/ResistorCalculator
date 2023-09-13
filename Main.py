# Imports
import pygame

# Constants
MOUSELEFT = 1
MOUSERIGHT = 3


# Functions
def Background():
    tile = pygame.Surface((scale, scale))
    tile.fill((30, 31, 34))
    pygame.draw.rect(tile, (50, 51, 54), pygame.Rect(int(scale / 2 - scale / 8), int(scale / 2 - scale / 8), int(scale / 4), int(scale / 4)))

    background = pygame.Surface(screen.get_size())
    for x in range(width):
        for y in range(height):
            background.blit(tile, (edge[0] + x * scale, edge[1] + y * scale))
    return background


def Draw():
    screen.blit(background, (0, 0))
    middelground.fill(pygame.Color(0, 0, 0, 0))
    for i in components:
        i.draw()
    screen.blit(middelground, (0, 0))


def CheckComponents(pos):
    temp = []
    for i in components:
        if i.checkFootprint(pos):
            temp.append(i)
    return temp


def RemoveNeigbours(remove):
    for i in components:
        if isinstance(i, Cross):
            i.removeNeighbour(remove)


def TilesToCords(pos):
    return int(pos[0] * scale + scale / 2 + edge[0] - 1), int(pos[1] * scale + scale / 2 + edge[1] - 1)


def CordsToTiles(pos):
    return int((pos[0] - edge[0]) / scale), int((pos[1] - edge[1]) / scale)


def DrawExampleLine():
    pygame.draw.line(screen, (0, 0, 0), TilesToCords(tempPos), TilesToCords(validLinePos), 7)


def ValidLineTile():
    if abs(mousePos[0] - tempPos[0]) <= abs(mousePos[1] - tempPos[1]):
        X = tempPos[0]
        Y = mousePos[1]
    else:
        X = mousePos[0]
        Y = tempPos[1]

    if prvPos is not None:

        a = tempPos[0] - prvPos[0]
        b = tempPos[0] - X
        c = tempPos[1] - prvPos[1]
        d = tempPos[1] - Y

        # check if the line overlaps itself
        if ((a < 0) != (b < 0) or a == 0 or b == 0) and ((c < 0) != (d < 0) or c == 0 or d == 0):
            pass
        else:
            return None

    a, b = OrganizeTiles(tempPos, (X, Y))
    footprint = Footprint(a, b)
    for x in footprint[0]:
        for y in footprint[1]:
            for p in components:
                if p.checkFootprint((x,y)):
                    return x,y
    return X, Y

def OrganizeTiles(posA, posB):
    # Make sure posA is above and to the left of posB
    if posA[0] < posB[0]:
        A = posA
        B = posB
    elif posA[0] > posB[0]:
        A = posB
        B = posA
    elif posA[1] < posB[1]:
        A = posA
        B = posB
    else:
        A = posB
        B = posA
    return A, B

def Footprint(posA, posB):
    footprint = [[],[]]
    for x in range(1, posB[0] - posA[0]):
        footprint[0].append(posA[0] + x)
    if len(footprint[0]) == 0:
        footprint[0].append(posA[0])

    for y in range(1, posB[1] - posA[1]):
        footprint[1].append(posA[1] + y)
    if len(footprint[1]) == 0:
        footprint[1].append(posA[1])
    return footprint

def UnselectLine():
    global tempPos, prvPos
    tempPos = None
    prvPos = None
    Draw()

# Classes

class Line:

    def __init__(self, posA, posB, neighbourA, neighbourB):
        # Make sure posA is above and to the left of posB
        if posA[0] < posB[0]:
            self.posA = posA
            self.neighbourA = neighbourA
            self.posB = posB
            self.neighbourB = neighbourB
        elif posA[0] > posB[0]:
            self.posA = posB
            self.neighbourA = neighbourB
            self.posB = posA
            self.neighbourB = neighbourA
        elif posA[1] < posB[1]:
            self.posA = posA
            self.neighbourA = neighbourA
            self.posB = posB
            self.neighbourB = neighbourA
        else:
            self.posA = posB
            self.neighbourA = neighbourB
            self.posB = posA
            self.neighbourB = neighbourA

        self.footprint = Footprint(self.posA, self.posB)

    def checkFootprint(self, pos):
        if pos[0] in self.footprint[0] and pos[1] in self.footprint[1]:
            return True
        return False

    def draw(self):
        pygame.draw.line(middelground, (0, 0, 0), TilesToCords(self.posA), TilesToCords(self.posB), 7)

    def splitLine(self, pos, neighbour):
        self.footprint = Footprint(self.posA, pos)

        components.append(Line(pos, self.posB, neighbour, self.neighbourB))
        self.posB = pos
        self.neighbourB = neighbour


class Cross:

    def __init__(self, pos, neighbour=None):
        self.pos = pos
        self.neighbours = []
        if neighbour is not None:
            self.neighbours.append(neighbour)

    def draw(self):
        pygame.draw.circle(middelground, (0, 0, 0), TilesToCords(self.pos), 8)

    def checkFootprint(self, pos):
        if self.pos == pos:
            return True
        return False

    def addNeighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def addNeighbours(self, neighbours):
        for i in neighbours:
            self.neighbours.append(i)

    def removeNeighbour(self, remove):
        if remove in self.neighbours:
            self.neighbours.remove(remove)


class Resistor:
    footPrint = [[(-1, 0), (0, 0), (0, 1)], [(0, -1), (0, 0), (0, 1)]]

    def __init__(self):
        pass


# Execute

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
scale = 30

middelground = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)

width = int(screen.get_width() / scale)
height = int(screen.get_height() / scale)
edge = (screen.get_width() - scale * width) / 2, (screen.get_height() - scale * height) / 2

background = Background()

components = []
tempPos = None
tempCrossA = None
tempCrossB = None
prvPos = None
validLinePos = None

# Run until the user asks to quit
Draw()
running = True
while running:
    mousePos = CordsToTiles(pygame.mouse.get_pos())

    screen.blit(background, (0, 0))
    screen.blit(middelground, (0, 0))

    # Userinput
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                UnselectLine()
            if event.key == pygame.K_q:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSELEFT:  # adds a crosspoint with a new line
                    if tempPos is None:
                        tempPos = mousePos
                        tempCrossA = Cross(tempPos)
                        tempCrossA.draw()
                        tempCrossB = None

                    else:
                        if validLinePos is not None:
                            if tempCrossB is None:
                                components.append(tempCrossA)

                            tempCrossB = Cross(validLinePos)
                            components.append(Line(tempPos, validLinePos, tempCrossA, tempCrossB))
                            tempCrossA.addNeighbour(components[-1])
                            tempCrossB.addNeighbour(components[-1])
                            components.append(tempCrossB)
                            prvPos = tempPos[0], tempPos[1]
                            tempPos = validLinePos
                            tempCrossA = components[-1]
                            Draw()

                elif event.button == MOUSERIGHT:  # removes crosspoints and/or lines
                    remove = CheckComponents(mousePos)

                    for i in remove:
                        if isinstance(i, Cross):
                            for p in i.neighbours:
                                RemoveNeigbours(p)
                                components.remove(p)
                        components.remove(i)

                    UnselectLine()

    if tempPos is not None:
        validLinePos = ValidLineTile()

        if validLinePos is not None:
            DrawExampleLine()
    else:
        validLinePos = None

    pygame.draw.circle(screen, (0, 0, 0), TilesToCords(mousePos), 5)

    pygame.display.flip()

pygame.quit()
