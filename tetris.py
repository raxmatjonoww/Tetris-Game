import pygame
import random

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  
    (0, 0, 255),    
    (255, 165, 0),  
    (255, 255, 0),  
    (0, 255, 0),    
    (128, 0, 128),  
    (255, 0, 0)     
]

SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]]   
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def image(self):
        return self.shape

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def valid_space(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, value in enumerate(row):
            if value:
                if j + piece.x < 0 or j + piece.x >= WIDTH // BLOCK_SIZE or i + piece.y >= HEIGHT // BLOCK_SIZE:
                    return False
                if grid[i + piece.y][j + piece.x] != BLACK:
                    return False
    return True

def check_lost(positions):
    for (x, y) in positions:
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(WIDTH // BLOCK_SIZE // 2 - 2, 0, random.choice(SHAPES))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for y in range(len(grid)):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
    for x in range(len(grid[0])):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))

def clear_rows(grid, locked):
    cleared = 0
    for y in range(len(grid)-1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            del_row = y
            for x in range(len(grid[0])):
                try:
                    del locked[(x, y)]
                except:
                    continue
    if cleared > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < del_row:
                locked[(x, y + cleared)] = locked.pop(key)
    return cleared

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    current_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    run = True

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.3
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                for i, row in enumerate(current_piece.shape):
                    for j, value in enumerate(row):
                        if value:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
                current_piece = get_shape()
                if not valid_space(current_piece, grid):
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        for i, row in enumerate(current_piece.shape):
            for j, value in enumerate(row):
                if value:
                    grid[current_piece.y + i][current_piece.x + j] = current_piece.color

        clear_rows(grid, locked_positions)
        draw_grid(win, grid)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
