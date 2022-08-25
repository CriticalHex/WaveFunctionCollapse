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

TileImages = [Tile("Tile0.png", [0,0,0,0]), 
            Tile("Tile1.png", [1,1,0,1]),
            Tile("Tile2.png", [1,1,1,0]),
            Tile("Tile3.png", [0,1,1,1]),
            Tile("Tile4.png", [1,0,1,1])]

class Space:
    def __init__(self):
        self.collapsed = False
        self.possibilities = TileImages.copy()
        self.tile = self.possibilities[0]

    def test(self,slot):
        self.possibilities.pop(slot)
        print(len(TileImages))

    def draw(self):
        if self.collapsed:
            screen.blit(self.tile.image)

    def collapse(self):
        self.collapsed = True

    def determine_possible(self):
        pass

grid = []
for i in range(10):
    grid.append([])
    for j in range(10):
        grid[i].append(Space())


while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    for i in range(10):
        for j in range(10):
            grid[i][j].draw()

