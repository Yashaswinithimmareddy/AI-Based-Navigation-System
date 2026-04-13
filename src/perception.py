import pygame
import math
import numpy as np

class LiDARPerception:
    """
    Simulates a 2D LiDAR (Light Detection and Ranging) using Raycasting.
    It shoots rays in 360 degrees around the vehicle and detects the distance
    to the nearest obstacles.
    """
    def __init__(self, num_rays=36, max_range=150, fov=360):
        self.num_rays = num_rays
        self.max_range = max_range
        self.fov = fov
        self.points_detected = []

    def scan(self, start_pos, vehicle_angle, grid_map, cell_size):
        """
        Scans the environment using raycasting.
        start_pos: (x, y) of the vehicle.
        vehicle_angle: current heading of the vehicle (radians).
        grid_map: 2D numpy array representing the map (0 = free, 1 = obstacle).
        cell_size: pixel size of each grid cell.
        """
        self.points_detected = []
        angle_step = math.radians(self.fov / self.num_rays)
        start_angle = vehicle_angle - math.radians(self.fov / 2)
        
        # Shoot rays
        for i in range(self.num_rays):
            angle = start_angle + (i * angle_step)
            hit_dist = self.max_range
            hit_pos = None
            
            # Simple raycasting: step along the ray until collision
            for dist in range(1, self.max_range, 2):
                ray_x = start_pos[0] + math.cos(angle) * dist
                ray_y = start_pos[1] + math.sin(angle) * dist
                
                # Check grid bounds
                grid_x = int(ray_x / cell_size)
                grid_y = int(ray_y / cell_size)
                
                if grid_x < 0 or grid_x >= grid_map.shape[0] or grid_y < 0 or grid_y >= grid_map.shape[1]:
                    break # Out of map
                
                # If hit obstacle
                if grid_map[grid_x, grid_y] == 1:
                    hit_dist = dist
                    hit_pos = (ray_x, ray_y)
                    break
            
            if hit_pos:
                self.points_detected.append(hit_pos)
                
        return self.points_detected
