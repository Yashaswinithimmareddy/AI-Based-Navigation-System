import pygame

def draw_grid(screen, grid, path, start, goal, cell_size):
    for x in range(len(grid)):
        for y in range(len(grid)):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)

            if grid[x][y] == 1:
                pygame.draw.rect(screen, (0,0,0), rect)
            else:
                pygame.draw.rect(screen, (255,255,255), rect, 1)

    for node in path:
        pygame.draw.rect(screen, (0,255,0),
                         (node[0]*cell_size, node[1]*cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (0,0,255),
                     (start[0]*cell_size, start[1]*cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (255,0,0),
                     (goal[0]*cell_size, goal[1]*cell_size, cell_size, cell_size))