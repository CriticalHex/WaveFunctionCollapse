import pygame
import random
import copy
import numpy as np

pygame.init()
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0,0,0))
Running = True


class Tile:
    def __init__(self, fileName: str, sideValues: list):
        self.image = pygame.image.load("BuildingTiles/"+fileName)
        self.sides = sideValues
        self.name = fileName

TileImages = [Tile("Tile0.png", [0,0,0,0]),
            Tile("Tile1.png", [1,1,1,1]),
            Tile("Tile2.png", [1,1,1,1]),
            Tile("Tile3.png", [0,2,1,2]),
            Tile("Tile6.png", [4,1,4,0]),
            Tile("Tile7.png", [3,0,3,1]),
            Tile("Tile8.png", [0,2,4,0]),
            Tile("Tile9.png", [0,0,3,2]),
            Tile("Tile10.png", [4,1,1,2]),
            Tile("Tile11.png", [3,2,1,1])]

#Tile("Tile8.png", [0,2,3,0]),
#Tile("Tile9.png", [0,0,3,4])

#Tile("Tile8.png", [0,1,1,0]),
#Tile("Tile9.png", [0,0,1,1])

'''
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
'''

class Space:
    def __init__(self,xpos,ypos):
        self.collapsed = False
        self.possibilities = copy.copy(TileImages)
        self.pos = (xpos, ypos)
        self.entropy = len(TileImages)
        self.tile: Tile

    def draw(self):
        if self.collapsed:
            screen.blit(self.tile.image, self.pos)

    def collapse(self):
        if len(self.possibilities) != 0:
            #print(len(self.possibilities))
            self.collapsed = True
            randomSlot = random.randint(0,len(self.possibilities)-1)
            self.tile = self.possibilities[randomSlot]
            return
        #print("POSSIBILITIES LIST IS 0")

def determine_possibilities():
    filter = []
    isDone = True
    for i,rows in enumerate(grid):
        for j,tile in enumerate(rows):
            if tile.collapsed == False:
                filter = copy.copy(tile.possibilities)
                isDone = False
                if j+1 < len(grid[i]):
                    if grid[i][j+1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j+1].tile.sides[3] != possibility.sides[1]:
                                #print(grid[i][j+1].tile.name, "LEFT DOES NOT MATCH", possibility.name, "RIGHT")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i][j+1].tile.name, "LEFT MATCHES", possibility.name, "RIGHT")
                if j-1 >= 0:
                    if grid[i][j-1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j-1].tile.sides[1] != possibility.sides[3]:
                                #print(grid[i][j-1].tile.name, "RIGHT DOES NOT MATCH", possibility.name, "LEFT")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i][j-1].tile.name, "RIGHT MATCHES", possibility.name, "LEFT")
                if i+1 < len(grid):
                    if grid[i+1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i+1][j].tile.sides[0] != possibility.sides[2]:
                                #print(grid[i+1][j].tile.name, "TOP DOES NOT MATCH", possibility.name, "BOTTOM")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i+1][j].tile.name, "TOP MATCHES", possibility.name, "BOTTOM")
                if i-1 >= 0:
                    if grid[i-1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i-1][j].tile.sides[2] != possibility.sides[0]:
                                #print(grid[i-1][j].tile.name, "BOTTOM DOES NOT MATCH", possibility.name, "TOP")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i-1][j].tile.name, "BOTTOM MATCHES", possibility.name, "TOP")
            tile.possibilities = copy.copy(filter)
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
        randomSlot = random.randint(0,len(lowestList)-1)
        lowestList[randomSlot].collapse()
        return
    #print("LOWEST LIST IS 0")

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

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        makeGrid()
    if keys[pygame.K_LCTRL]:
        Running = False

    screen.fill((0,0,0))
    
    if not done:
        done = determine_possibilities()
        collapse()

    for i in range(int(screen.get_height()/100)):
        for j in range(int(screen.get_width()/100)):
            grid[i][j].draw()

    pygame.display.flip()