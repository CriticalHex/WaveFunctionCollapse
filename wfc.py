import pygame
import random
from copy import copy


class Wave:
    class Image:
        def __init__(self, fileName: str, sideValues: list[int]):
            self.image = pygame.image.load("BuildingTiles/" + fileName)
            self.sides = sideValues
            self.name = fileName

    class Tile:
        def __init__(self, xpos: int, ypos: int, TileImages: list["Wave.Image"]):
            self.collapsed: bool = False
            self.possibilities: list[Wave.Image] = copy(TileImages)
            self.pos = (xpos, ypos)
            self.entropy = len(self.possibilities)
            self.image: Wave.Image

        def draw(self, screen: pygame.Surface):
            if self.collapsed:
                screen.blit(self.image.image, self.pos)

        def collapse(self):
            self.collapsed = True
            random_index = random.randrange(self.entropy)
            self.image = self.possibilities[random_index]

    def __init__(self, screen_size: pygame.Vector2) -> None:
        self.tile_images = [
            Wave.Image("Tile0.png", [0, 0, 0, 0]),
            Wave.Image("Tile1.png", [1, 1, 1, 1]),
            Wave.Image("Tile2.png", [1, 1, 1, 1]),
            Wave.Image("Tile6.png", [4, 1, 4, 0]),
            Wave.Image("Tile7.png", [3, 0, 3, 1]),
            Wave.Image("Tile8.png", [0, 2, 4, 0]),
            Wave.Image("Tile9.png", [0, 0, 3, 2]),
            Wave.Image("Tile10.png", [4, 1, 1, 2]),
            Wave.Image("Tile11.png", [3, 2, 1, 1]),
        ]  # contemplating making this a create_grid argument explicitly
        self.tile_size = 100
        self.grid: list[list[Wave.Tile]]
        self.lowest_entropy: int
        self.done: bool
        self.last_y: int
        self.last_x: int
        self.last_collapsed: Wave.Tile
        self.create_grid(screen_size)

    def create_grid(self, screen_size: pygame.Vector2):
        self.done = False
        grid: list[list[Wave.Tile]] = []
        for i in range(int(screen_size.y / self.tile_size)):
            grid.append([])
            for j in range(int(screen_size.x / self.tile_size)):
                grid[i].append(
                    Wave.Tile(j * self.tile_size, i * self.tile_size, self.tile_images)
                )
        self.grid = grid
        self.lowest_entropy: int = len(self.tile_images)
        self.last_y = random.randrange(len(self.grid))
        self.last_x = random.randrange(len(self.grid[0]))
        self.last_collapsed = self.grid[self.last_y][self.last_x]
        self.last_collapsed.collapse()
        self.update_possibilities()

    def update_possibilities(self):
        x, y = self.last_x, self.last_y
        self.lowest_entropy = len(self.tile_images)
        self.done = True
        if y - 1 >= 0:
            up = self.grid[y - 1][x]
            if not up.collapsed:
                self.done = False
                new_possibilities: list[Wave.Image] = []
                for possibility in up.possibilities:
                    if possibility.sides[2] == self.last_collapsed.image.sides[0]:
                        new_possibilities.append(possibility)
                up.possibilities = new_possibilities
                up.entropy = len(up.possibilities)
                self.lowest_entropy = min(self.lowest_entropy, up.entropy)
        if y + 1 < len(self.grid):
            down = self.grid[y + 1][x]
            if not down.collapsed:
                self.done = False
                new_possibilities: list[Wave.Image] = []
                for possibility in down.possibilities:
                    if possibility.sides[0] == self.last_collapsed.image.sides[2]:
                        new_possibilities.append(possibility)
                down.possibilities = new_possibilities
                down.entropy = len(down.possibilities)
                self.lowest_entropy = min(self.lowest_entropy, down.entropy)
        if x - 1 >= 0:
            left = self.grid[y][x - 1]
            if not left.collapsed:
                self.done = False
                new_possibilities: list[Wave.Image] = []
                for possibility in left.possibilities:
                    if possibility.sides[1] == self.last_collapsed.image.sides[3]:
                        new_possibilities.append(possibility)
                left.possibilities = new_possibilities
                left.entropy = len(left.possibilities)
                self.lowest_entropy = min(self.lowest_entropy, left.entropy)
        if x + 1 < len(self.grid[y]):
            right = self.grid[y][x + 1]
            if not right.collapsed:
                self.done = False
                new_possibilities: list[Wave.Image] = []
                for possibility in right.possibilities:
                    if possibility.sides[3] == self.last_collapsed.image.sides[1]:
                        new_possibilities.append(possibility)
                right.possibilities = new_possibilities
                right.entropy = len(right.possibilities)
                self.lowest_entropy = min(self.lowest_entropy, right.entropy)
        if self.lowest_entropy == 0:
            for row in self.grid:
                for tile in row:
                    if tile.entropy == 0:
                        print("HERE")

    def collapse(self):
        lowest_entropy_tiles: list[Wave.Tile] = []
        # for row in self.grid:
        #     for tile in row:
        #         print(tile.entropy, end=" ")
        #     print()
        # print()
        for row in self.grid:
            for tile in row:
                if not tile.collapsed and tile.entropy == self.lowest_entropy:
                    lowest_entropy_tiles.append(tile)
        random_index = random.randrange(len(lowest_entropy_tiles))
        lowest_entropy_tiles[random_index].collapse()
        self.last_collapsed = lowest_entropy_tiles[random_index]
        self.last_x = int(lowest_entropy_tiles[random_index].pos[0] / self.tile_size)
        self.last_y = int(lowest_entropy_tiles[random_index].pos[1] / self.tile_size)
        self.update_possibilities()

    def update(self, screen: pygame.Surface):
        if not self.done:
            if self.collapse():
                print("Done")
        for row in self.grid:
            for tile in row:
                tile.draw(screen)


def main():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
    pygame.display.set_caption("Wave Function Collapse")
    running = True
    wave = Wave(pygame.Vector2(screen.get_size()))
    done = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False

        screen.fill((0, 0, 0))

        if not done:
            done = wave.update(screen)

        pygame.display.flip()

    pygame.quit()


main()
