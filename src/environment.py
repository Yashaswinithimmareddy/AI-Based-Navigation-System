import numpy as np

class GridEnvironment:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))

    def add_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.grid[x][y] = 1  # obstacle

    def is_obstacle(self, node):
        return self.grid[node[0]][node[1]] == 1