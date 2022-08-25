import pygame
import random

class Tile:
    def __init__(self, fileName: str, sideValues: list):
        self.image = pygame.image.load("Tiles/"+fileName)
        self.sides = sideValues
        
    
pygame.init()
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((1000, 1000))
screen.fill((0,0,0))
Running = True

grid_size = 10

imageWidth = screen.get_width()/grid_size
imageHeight = screen.get_height()/grid_size

tiles = []
tiles.append(Tile("Tile0.png", [0,0,0,0]))
tiles.append(Tile("Tile1.png", [1,1,0,1]))
tiles.append(Tile("Tile2.png", [1,1,1,0]))
tiles.append(Tile("Tile3.png", [0,1,1,1]))
tiles.append(Tile("Tile4.png", [1,0,1,1]))

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    for i in range(0,int(screen.get_width()),int(imageWidth)):
        for j in range(0,int(screen.get_height()),int(imageHeight)):
            pygame.draw()

    pygame.display.flip()