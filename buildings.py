import pygame
import random
import copy
import os

winX = 0
winY = 0
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (winX, winY)

pygame.init()
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((1920 * 2, 1100))
screen.fill((0, 0, 0))
Running = True


class Tile:
    def __init__(self, fileName: str, sideValues: list):
        self.image = pygame.image.load("BuildingTiles/" + fileName)
        self.sides = sideValues
        self.name = fileName


TileImages = [
    Tile("Tile0.png", [0, 0, 0, 0]),
    Tile("Tile1.png", [1, 1, 1, 1]),
    Tile("Tile2.png", [1, 1, 1, 1]),
    Tile("Tile6.png", [4, 1, 4, 0]),
    Tile("Tile7.png", [3, 0, 3, 1]),
    Tile("Tile8.png", [0, 2, 4, 0]),
    Tile("Tile9.png", [0, 0, 3, 2]),
    Tile("Tile10.png", [4, 1, 1, 2]),
    Tile("Tile11.png", [3, 2, 1, 1]),
]

# Tile("Tile8.png", [0,2,3,0]),
# Tile("Tile9.png", [0,0,3,4])

# Tile("Tile8.png", [0,1,1,0]),
# Tile("Tile9.png", [0,0,1,1])

"""
TileImages = [Tile("Tile0.png", [0,0,0,0]),
            Tile("Tile1.png", [1,1,1,1]),
            Tile("Tile2.png", [1,1,1,1]),
            Tile("Tile3.png", [0,2,1,2]),
            Tile("Tile4.png", [0,0,3,2]),
            Tile("Tile5.png", [0,2,4,0]),
            Tile("Tile6.png", [4,1,4,0]),
            Tile("Tile7.png", [3,0,3,1]),
            Tile("Tile8.png", [0,1,1,0]),
            Tile("Tile9.png", [0,0,1,1])]
"""


class Space:
    def __init__(self, xpos: int, ypos: int):
        self.collapsed: bool = False
        self.possibilities: list[Tile] = copy.copy(TileImages)
        self.pos = (xpos, ypos)
        self.entropy = len(TileImages)

    def draw(self):
        if self.collapsed:
            screen.blit(self.tile.image, self.pos)

    def collapse(self):
        if len(self.possibilities) != 0:
            self.collapsed = True
            randomSlot = random.randint(0, len(self.possibilities) - 1)
            self.tile: Tile = self.possibilities[randomSlot]


def determine_possibilities():
    filter = []
    isDone = True
    for i, rows in enumerate(grid):
        for j, tile in enumerate(rows):
            if tile.collapsed == False:
                filter = copy.copy(tile.possibilities)
                isDone = False
                if j + 1 < len(grid[i]):
                    if grid[i][j + 1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j + 1].tile.sides[3] != possibility.sides[1]:
                                filter.remove(possibility)
                if j - 1 >= 0:
                    if grid[i][j - 1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j - 1].tile.sides[1] != possibility.sides[3]:
                                filter.remove(possibility)
                if i + 1 < len(grid):
                    if grid[i + 1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i + 1][j].tile.sides[0] != possibility.sides[2]:
                                filter.remove(possibility)
                if i - 1 >= 0:
                    if grid[i - 1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i - 1][j].tile.sides[2] != possibility.sides[0]:
                                filter.remove(possibility)
            tile.possibilities = copy.copy(filter)
            tile.entropy = len(tile.possibilities)
    return isDone


def collapse():
    lowestEntropy = len(TileImages)
    lowestList: list[Space] = []
    for i, rows in enumerate(grid):
        for j, tile in enumerate(rows):
            if tile.collapsed == False:
                if tile.entropy < lowestEntropy:
                    lowestEntropy = tile.entropy
    for i, rows in enumerate(grid):
        for j, tile in enumerate(rows):
            if tile.collapsed == False:
                if tile.entropy == lowestEntropy:
                    lowestList.append(tile)
    if len(lowestList) != 0:
        randomSlot = random.randint(0, len(lowestList) - 1)
        lowestList[randomSlot].collapse()
        return


def makeGrid():
    global done
    global grid
    done = False
    grid = []
    for i in range(int(screen.get_height() / 100)):
        grid.append([])
        for j in range(int(screen.get_width() / 100)):
            grid[i].append(Space(j * 100, i * 100))


makeGrid()

explainerMode = True
ticker = 0

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        makeGrid()
    if keys[pygame.K_LCTRL]:
        Running = False
    if keys[pygame.K_RCTRL]:
        explainerMode = False

    if explainerMode:

        if keys[pygame.K_SPACE] and ticker % 10000 == 0:
            screen.fill((0, 0, 0))

            if not done:
                done = determine_possibilities()
                collapse()

            for i in range(int(screen.get_height() / 100)):
                for j in range(int(screen.get_width() / 100)):
                    grid[i][j].draw()

            pygame.display.flip()
        ticker += 1

    else:
        screen.fill((0, 0, 0))

        if not done:
            done = determine_possibilities()
            collapse()

        for i in range(int(screen.get_height() / 100)):
            for j in range(int(screen.get_width() / 100)):
                grid[i][j].draw()

        pygame.display.flip()
