import math
import heapq
import numpy as np

class AStarPlanner:
    """
    Implements the A* (A-Star) search algorithm for finding the optimal path
    from start to goal on a 2D grid map avoiding obstacles.
    """
    def __init__(self, grid_map, cell_size):
        self.grid_map = grid_map # 2D array: 0=free, 1=obstacle
        self.cell_size = cell_size
        self.motions = [
            (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), # orthogonal
            (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)), 
            (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))   # diagonal
        ]

    def heuristic(self, a, b):
        """Euclidean distance heuristic for A*"""
        return math.hypot(b[0] - a[0], b[1] - a[1])

    def plan(self, start_pos, goal_pos):
        """
        Calculates the path from start to goal.
        Returns a list of (x, y) pixel coordinates representing the waypoints.
        """
        # Convert pixel to grid coords
        start_node = (int(start_pos[0] / self.cell_size), int(start_pos[1] / self.cell_size))
        goal_node = (int(goal_pos[0] / self.cell_size), int(goal_pos[1] / self.cell_size))
        
        # Check if start or goal is inside an obstacle
        if self.grid_map[start_node[0], start_node[1]] == 1 or self.grid_map[goal_node[0], goal_node[1]] == 1:
            print("Start or Goal is inside an obstacle!")
            return []

        open_set = []
        heapq.heappush(open_set, (0.0, start_node))
        came_from = {}
        
        g_score = {start_node: 0.0}
        f_score = {start_node: self.heuristic(start_node, goal_node)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal_node:
                # Path found!
                path = []
                while current in came_from:
                    # Convert back to pixel center coordinates
                    path.append((current[0] * self.cell_size + self.cell_size/2, 
                                 current[1] * self.cell_size + self.cell_size/2))
                    current = came_from[current]
                path.append((start_node[0] * self.cell_size + self.cell_size/2, 
                             start_node[1] * self.cell_size + self.cell_size/2))
                return path[::-1] # Reverse. Start -> Goal
                
            for dx, dy, cost in self.motions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check grid boundaries
                if 0 <= neighbor[0] < self.grid_map.shape[0] and 0 <= neighbor[1] < self.grid_map.shape[1]:
                    # Check for obstacles
                    if self.grid_map[neighbor[0], neighbor[1]] == 1:
                        continue 
                        
                    tentative_g_score = g_score[current] + cost
                    
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal_node)
                        # Add to open set
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            
        print("No path found!")
        return []
