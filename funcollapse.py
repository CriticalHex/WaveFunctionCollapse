import pygame

class Tile:
    def __init__(self, fileName: str, sideValues: list):
        self.image = pygame.image.load(fileName)
        self.sides = sideValues
        
    
pygame.init() 
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((1000, 1000))
screen.fill((0,0,0))
Running = True

imageWidth = 100
imageHeight = 100

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    pygame.display.
    pygame.display.flip()