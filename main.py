import math
from src.simulation import SimulationEnv
from src.perception import LiDARPerception
from src.path_planning import AStarPlanner
from src.controller import PurePursuitController

def main():
    print("Initializing Simulation Environment...")
    env = SimulationEnv(width=800, height=600, cell_size=20)
    
    print("Initializing Modules...")
    lidar = LiDARPerception(num_rays=36, max_range=150)
    planner = AStarPlanner(env.grid_map, env.cell_size)
    controller = PurePursuitController(lookahead_distance=20.0, linear_velocity=3.0)

    # Initial vehicle state
    vehicle_pos = [40.0, 40.0]
    vehicle_angle = 0.0
    goal_pos = (700.0, 500.0)

    print("Planning initial path...")
    path = planner.plan(vehicle_pos, goal_pos)
    controller.update_path(path)

    print("Starting Main Loop...")
    running = True
    while running:
        running = env.handle_events()
        
        if not running:
            break

        # 1. Perception Step (Scan environment)
        lidar_points = lidar.scan(vehicle_pos, vehicle_angle, env.grid_map, env.cell_size)
        
        # 2. Planning Integration (Dynamic re-planning could be added here if obstacles were moving)
        
        # 3. Control Step (Get v, steering angle)
        v, steering = controller.get_control_commands(vehicle_pos, vehicle_angle)

        # 4. Kinematics Update (Move vehicle)
        vehicle_angle += steering
        vehicle_pos[0] += v * math.cos(vehicle_angle)
        vehicle_pos[1] += v * math.sin(vehicle_angle)

        # 5. Render Scene
        env.render(vehicle_pos, vehicle_angle, path, lidar_points)

        # Check Goal achievement
        dist_to_goal = math.hypot(goal_pos[0] - vehicle_pos[0], goal_pos[1] - vehicle_pos[1])
        if dist_to_goal < env.cell_size:
            print("Goal Reached Successfully!")
            running = False # Exit after reaching
            import time
            time.sleep(2) # Pause briefly to show arrival

    env.close()

if __name__ == "__main__":
    main()