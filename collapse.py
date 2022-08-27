import pygame
import random
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
        self.name = fileName[0:5]

TileImages = [Tile("Tile0.png", [0,0,0,0]), 
            Tile("Tile1.png", [1,1,0,1]),
            Tile("Tile2.png", [1,1,1,0]),
            Tile("Tile3.png", [0,1,1,1]),
            Tile("Tile4.png", [1,0,1,1])]

class Space:
    def __init__(self,xpos,ypos):
        self.collapsed = False
        self.possibilities = TileImages.copy()
        self.pos = (xpos,ypos)
        self.entropy = 5
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

def determine_possibilities():
    isDone = True
    for i,rows in enumerate(grid):
        for j,tile in enumerate(rows):
            if not tile.collapsed:
                isDone = False
                if j+1 < len(grid[i]):
                    if grid[i][j+1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j+1].tile.sides[3] is not possibility.sides[1]:
                                tile.remove_possibility(possibility)
                if j-1 >= 0:
                    if grid[i][j-1].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i][j-1].tile.sides[1] is not possibility.sides[3]:
                                tile.remove_possibility(possibility)
                if i+1 < len(grid):
                    if grid[i+1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i+1][j].tile.sides[0] is not possibility.sides[2]:
                                tile.remove_possibility(possibility)
                if i-1 >= 0:
                    if grid[i-1][j].collapsed:
                        for possibility in tile.possibilities:
                            if grid[i-1][j].tile.sides[2] is not possibility.sides[0]:
                                tile.remove_possibility(possibility)
            tile.entropy = len(tile.possibilities)
    return isDone

def collapse():
    lowestEntropy = 5
    lowestList = []
    for i,rows in enumerate(grid):
            for j,tile in enumerate(rows):
                if tile.entropy < lowestEntropy:
                    lowestEntropy = tile.entropy
                    print(lowestEntropy,end=", ")
    for i,rows in enumerate(grid):
            for j,tile in enumerate(rows):
                if tile.entropy == lowestEntropy:
                    lowestList.append(tile)
    if len(lowestList) != 0:
        print(len(lowestList))
        lowestList[random.randint(0,len(lowestList)-1)].collapse()
        return
    print("NO LOWEST ENTROPY??")

done = False

grid = []
for i in range(int(screen.get_height()/100)):
    grid.append([])
    for j in range(int(screen.get_width()/100)):
        grid[i].append(Space(j*100,i*100))

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    screen.fill((0,0,0))
    
    if not done:
        done = determine_possibilities()
        collapse()

    for i in range(int(screen.get_height()/100)):
        for j in range(int(screen.get_width()/100)):
            grid[i][j].draw()

    pygame.display.flip()