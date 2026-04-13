import pygame
import numpy as np
import math

class SimulationEnv:
    """
    Handles the 2D visual simulation using Pygame.
    Draws the map, obstacles, vehicle, path, and lidar rays.
    """
    def __init__(self, width=800, height=600, cell_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Autonomous Navigation System")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BG_COLOR = (30, 30, 40)
        self.GRID_COLOR = (50, 50, 60)
        self.OBS_COLOR = (200, 50, 50)
        self.CAR_COLOR = (50, 200, 100)
        self.PATH_COLOR = (255, 200, 50)
        self.LIDAR_COLOR = (100, 200, 255, 100) # RGBA with alpha doesn't work simply on main surface, need surf

        # Map: 0 = Free, 1 = Obstacle
        self.grid_map = np.zeros((self.grid_width, self.grid_height), dtype=int)
        self._build_obstacles()

    def _build_obstacles(self):
        """Creates some static obstacles on the map for testing."""
        # Boundaries
        self.grid_map[0, :] = 1
        self.grid_map[-1, :] = 1
        self.grid_map[:, 0] = 1
        self.grid_map[:, -1] = 1

        # Central walls
        for i in range(10, 30):
            self.grid_map[i, 10] = 1
        for i in range(10, 20):
            self.grid_map[20, i] = 1
            
        # Add random blocks
        self.grid_map[30:35, 20:25] = 1
        self.grid_map[5:10, 25:28] = 1

    def handle_events(self):
        """Checks for quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def render(self, vehicle_pos, vehicle_angle, path, lidar_points):
        """Draws everything onto the screen."""
        self.screen.fill(self.BG_COLOR)
        
        # Draw Map
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                # pygame.draw.rect(self.screen, self.GRID_COLOR, rect, 1) # Optional grid
                if self.grid_map[x, y] == 1:
                    pygame.draw.rect(self.screen, self.OBS_COLOR, rect)
                    
        # Draw Path
        if path:
            if len(path) > 1:
                pygame.draw.lines(self.screen, self.PATH_COLOR, False, path, 3)

        # Draw Lidar Rays
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for pt in lidar_points:
            pygame.draw.line(surface, self.LIDAR_COLOR, vehicle_pos, pt, 1)
            pygame.draw.circle(surface, self.LIDAR_COLOR, (int(pt[0]), int(pt[1])), 2)
        self.screen.blit(surface, (0,0))

        # Draw Vehicle
        car_radius = 8
        pygame.draw.circle(self.screen, self.CAR_COLOR, (int(vehicle_pos[0]), int(vehicle_pos[1])), car_radius)
        # Heading marker
        dx = car_radius * 2 * math.cos(vehicle_angle)
        dy = car_radius * 2 * math.sin(vehicle_angle)
        pygame.draw.line(self.screen, (255,255,255), vehicle_pos, (vehicle_pos[0]+dx, vehicle_pos[1]+dy), 2)

        pygame.display.flip()
        self.clock.tick(60) # 60 FPS

    def close(self):
        pygame.quit()
