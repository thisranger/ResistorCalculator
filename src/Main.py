#!/usr/bin/python
# Imports
import pygame
from itertools import product
import Components as C
import Tiles as T

from screen import ScreenData
# Constants
MOUSELEFT = 1
MOUSERIGHT = 3

CIRCLE = 0
LINE = 1

HOR = 0
VER = 1


# Functions
def Background(sd:ScreenData):
    tile = pygame.Surface((sd.scale, sd.scale))
    tile.fill((30, 31, 34))
    pygame.draw.rect(tile, (50, 51, 54), pygame.Rect(int(sd.scale / 2 - sd.scale / 8), int(sd.scale / 2 - sd.scale / 8), int(sd.scale / 4), int(sd.scale / 4)))

    background = pygame.Surface(sd.screen.get_size())
    for x in range(sd.width):
        for y in range(sd.height):
            background.blit(tile, (sd.edge[0] + x * sd.scale, sd.edge[1] + y * sd.scale))
    return background


def Draw():
    screen.blit(background, (0, 0))
    middelground.fill(pygame.Color(0, 0, 0, 0))
    for i in objects:
        i = i.draw()
        if LINE:
            pygame.draw.line(middelground, i[1], T.TilesToCords(i[2]), T.TilesToCords(i[3]), i[4])
        elif CIRCLE:
            pygame.draw.circle(middelground, i[1], T.TilesToCords(i[2]), i[3])
    screen.blit(middelground, (0, 0))


def CheckComponents(pos):
    temp = []
    for i in objects:
        if i.checkFootprint(pos):
            temp.append(i)
    return temp


def RemoveNeigbours(remove):
    for i in objects:
        if isinstance(i, C.Cross):
            i.removeNeighbour(remove)


def DrawExampleLine():
    if validLine[1]:
        color = (20, 20, 20)
    else:
        color = (40, 0, 0)
    pygame.draw.line(screen, color, T.TilesToCords(tempPos), T.TilesToCords(validLine[0]), 7)


def ValidLineTile():
    # returns a sugestion and if the line is valid and which componenten is clicked
    if abs(mousePos[0] - tempPos[0]) <= abs(mousePos[1] - tempPos[1]):
        newPos = tempPos[0], mousePos[1]
    else:
        newPos = mousePos[0], tempPos[1]

    collision = 1000, 10000
    collisionObject = None
    a, b = T.OrganizeTiles(tempPos, (newPos[0], newPos[1]))
    footprint = Footprint(a, b)
    if newPos[0] in footprint[0]:
        footprint[1].append(newPos[1])
    else:
        footprint[0].append(newPos[0])

    for component, x, y in product(objects, footprint[0], footprint[1]):
        if component.checkFootprint((x, y)):
            if isinstance(component, C.Cross):
                if len(footprint[0]) == 1:
                    if abs(tempPos[1] - y) < abs(tempPos[1] - collision[1]):
                        collision = x, y
                        collisionObject = component
                else:
                    if abs(tempPos[0] - x) < abs(tempPos[0] - collision[0]):
                        collision = x, y
                        collisionObject = component
            else:
                if tempPos[0] > x:
                    if component.checkFootprint((x - 1, y)):
                        return (newPos[0], newPos[1]), False, component
                elif tempPos[0] < x:
                    if component.checkFootprint((x + 1, y)):
                        return (newPos[0], newPos[1]), False, component
                elif tempPos[1] > y:
                    if component.checkFootprint((x, y - 1)):
                        return (newPos[0], newPos[1]), False, component
                elif tempPos[1] < y:
                    if component.checkFootprint((x, y + 1)):
                        return (newPos[0], newPos[1]), False, component

    if collisionObject is not None:
        return collision, True, collisionObject
    return (newPos[0], newPos[1]), True, None


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

def GetTileSize():
    return tileSize

def GetEdge():
    return edge


# Classes
class Resistor:
    footPrint = [[(-1, 0), (0, 0), (0, 1)], [(0, -1), (0, 0), (0, 1)]]

    def __init__(self):
        pass



def main():
    # Execute
    pygame.init()
    
    # Set up the drawing window
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    scale = 30

    width = int(screen.get_width() / scale)
    height = int(screen.get_height() / scale)
    edge = (screen.get_width() - scale * width) / 2, (screen.get_height() - scale * height) / 2

    sd = ScreenData(scale, screen, width, height, edge)
    
    background :pygame.Surface = Background(sd) 

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


if __name__ == '__main__':
    main()
