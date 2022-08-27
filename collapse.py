import pygame
import random
import copy
import numpy as np

pygame.init()
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((1000, 1000))
screen.fill((0,0,0))
Running = True


class Tile:
    def __init__(self, fileName: str, sideValues: list):
        self.image = pygame.image.load("Tiles/"+fileName)
        self.sides = sideValues

TileImages = [Tile("Tile0.png", [0,0,0,0]), 
            Tile("Tile1.png", [1,1,0,1]),
            Tile("Tile2.png", [1,1,1,0]),
            Tile("Tile3.png", [0,1,1,1]),
            Tile("Tile4.png", [1,0,1,1]),
            Tile("Tile5.png", [0,1,0,1]),
            Tile("Tile6.png", [1,0,1,0]),
            Tile("Tile7.png", [1,1,0,0]),
            Tile("Tile8.png", [0,1,1,0]),
            Tile("Tile9.png", [0,0,1,1]),
            Tile("Tile10.png", [1,0,0,1]),
            Tile("Tile11.png", [1,0,0,0]),
            Tile("Tile12.png", [0,1,0,0]),
            Tile("Tile13.png", [0,0,1,0]),
            Tile("Tile14.png", [0,0,0,1]),
            Tile("Tile15.png", [1,1,1,1])]

class Space:
    def __init__(self,xpos,ypos):
        self.collapsed = False
        self.possibilities = copy.copy(TileImages)
        self.pos = (xpos, ypos)
        self.entropy = len(TileImages)
        self.tile: Tile

    def remove_possibility(self,slot):
        self.possibilities.remove(slot)

    def draw(self):
        if self.collapsed:
            screen.blit(self.tile.image, self.pos)

    def collapse(self):
        if len(self.possibilities) != 0:
            self.collapsed = True
            self.tile = self.possibilities[random.randint(0,len(self.possibilities)-1)]
            return
        print("POSSIBILITIES LIST IS 0")

def determine_possibilities():
    isDone = True
    for i,rows in enumerate(grid):
        for j,tile in enumerate(rows):
            if tile.collapsed == False:
                isDone = False
                if j+1 < len(grid[i]):
                    if grid[i][j+1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j+1].tile.sides[3] != possibility.sides[1]:
                                tile.remove_possibility(possibility)
                if j-1 >= 0:
                    if grid[i][j-1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j-1].tile.sides[1] != possibility.sides[3]:
                                tile.remove_possibility(possibility)
                if i+1 < len(grid):
                    if grid[i+1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i+1][j].tile.sides[0] != possibility.sides[2]:
                                tile.remove_possibility(possibility)
                if i-1 >= 0:
                    if grid[i-1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i-1][j].tile.sides[2] != possibility.sides[0]:
                                tile.remove_possibility(possibility)
            tile.entropy = len(tile.possibilities)
    return isDone

def collapse():
    lowestEntropy = len(TileImages)
    lowestList = []
    for i,rows in enumerate(grid):
            for j,tile in enumerate(rows):
                if tile.collapsed == False:
                    if tile.entropy < lowestEntropy:
                        lowestEntropy = tile.entropy
    for i,rows in enumerate(grid):
            for j,tile in enumerate(rows):
                if tile.collapsed == False:
                    if tile.entropy == lowestEntropy:
                        lowestList.append(tile)
    if len(lowestList) != 0:
        lowestList[random.randint(0,len(lowestList)-1)].collapse()
        return
    print("LOWEST LIST IS 0")

def makeGrid():
    global done
    global grid
    done = False
    grid = []
    for i in range(int(screen.get_height()/100)):
        grid.append([])
        for j in range(int(screen.get_width()/100)):
            grid[i].append(Space(j*100,i*100))

makeGrid()

framerate = 0
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL]:
        makeGrid()

    if framerate % 600000 == 0:
        screen.fill((0,0,0))
        
        if not done:
            done = determine_possibilities()
            collapse()

        for i in range(int(screen.get_height()/100)):
            for j in range(int(screen.get_width()/100)):
                grid[i][j].draw()

        pygame.display.flip()
    framerate += 1