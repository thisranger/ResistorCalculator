#!/usr/bin/python
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
    if validLine[1]:
        color = (20, 20, 20)
    else:
        color = (40, 0, 0)
    pygame.draw.line(screen, color, TilesToCords(tempPos), TilesToCords(validLine[0]), 7)


def ValidLineTile():
    # returns a sugestion and if the line is valid and which componenten is clicked
    if abs(mousePos[0] - tempPos[0]) <= abs(mousePos[1] - tempPos[1]):
        X = tempPos[0]
        Y = mousePos[1]
    else:
        X = mousePos[0]
        Y = tempPos[1]

    collision = 1000, 10000
    collisionObject = None
    a, b = OrganizeTiles(tempPos, (X, Y))
    footprint = Footprint(a, b)
    if X in footprint[0]:
        footprint[1].append(Y)
    else:
        footprint[0].append(X)

    for p in components:
        for x in footprint[0]:
            for y in footprint[1]:
                if p.checkFootprint((x, y)):
                    if isinstance(p, Cross):
                        if len(footprint[0]) == 1:
                            if abs(tempPos[1] - y) < abs(tempPos[1] - collision[1]):
                                collision = x, y
                                collisionObject = p
                        else:
                            if abs(tempPos[0] - x) < abs(tempPos[0] - collision[0]):
                                collision = x, y
                                collisionObject = p
                    else:
                        if tempPos[0] > x:
                            print(X, Y, x, y)
                            if p.checkFootprint((x - 1, y)):
                                return (X, Y), False, p
                        elif tempPos[0] < x:
                            if p.checkFootprint((x + 1, y)):
                                return (X, Y), False, p
                        elif tempPos[1] > y:
                            if p.checkFootprint((x, y - 1)):
                                return (X, Y), False, p
                        elif tempPos[1] < y:
                            if p.checkFootprint((x, y + 1)):
                                return (X, Y), False, p

    if collisionObject is not None:
        return collision, True, collisionObject
    return (X, Y), True, None


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
    footprint = [[], []]
    for x in range(1, posB[0] - posA[0]):
        footprint[0].append(posA[0] + x)
    if posA[0] == posB[0]:
        footprint[0].append(posA[0])

    for y in range(1, posB[1] - posA[1]):
        footprint[1].append(posA[1] + y)
    if posA[1] == posB[1]:
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
validLine = None

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
                        if validLine is not None and validLine[1] is True:
                            if tempCrossB is None:
                                components.append(tempCrossA)

                            tempCrossB = Cross(validLine[0])
                            components.append(Line(tempPos, validLine[0], tempCrossA, tempCrossB))
                            tempCrossA.addNeighbour(components[-1])
                            tempCrossB.addNeighbour(components[-1])
                            components.append(tempCrossB)
                            prvPos = tempPos[0], tempPos[1]
                            tempPos = validLine[0]
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
        validLine = ValidLineTile()
        DrawExampleLine()

    else:
        validLine = None

    pygame.draw.circle(screen, (0, 0, 0), TilesToCords(mousePos), 5)

    pygame.display.flip()

pygame.quit()
