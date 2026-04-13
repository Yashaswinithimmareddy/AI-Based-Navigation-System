import numpy as np
import matplotlib.pyplot as plt
from src.path_planning import AStarPlanner

def generate_output_image():
    print("Generating simulation grid...")
    grid_map = np.zeros((40, 30), dtype=int)
    
    # Add boundaries
    grid_map[0, :] = 1
    grid_map[-1, :] = 1
    grid_map[:, 0] = 1
    grid_map[:, -1] = 1
    
    # Add obstacles (maze walls)
    grid_map[10:30, 10] = 1
    grid_map[20, 10:20] = 1
    grid_map[30:35, 20:25] = 1
    grid_map[5:15, 22:25] = 1

    planner = AStarPlanner(grid_map, cell_size=20)

    start_pos = [40.0, 40.0]
    goal_pos = [700.0, 500.0]

    print("Running A* Path Planning...")
    path = planner.plan(start_pos, goal_pos)

    print("Plotting results...")
    plt.figure(figsize=(10, 8))
    
    # Plot Map
    plt.imshow(grid_map.T, cmap='Greys', origin='lower', extent=[0, 800, 0, 600])
    
    # Plot obstacles visually stronger
    for x in range(grid_map.shape[0]):
        for y in range(grid_map.shape[1]):
            if grid_map[x, y] == 1:
                plt.gca().add_patch(plt.Rectangle((x*20, y*20), 20, 20, color='red', alpha=0.5))

    # Plot Path
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, '-o', color='gold', markersize=4, label='A* Optimal Path')

    # Start and Goal points
    plt.plot(start_pos[0], start_pos[1], 'bo', markersize=10, label='Start Node')
    plt.plot(goal_pos[0], goal_pos[1], 'go', markersize=12, label='Goal Node (Target)')

    plt.title("AI Autonomous Navigation System: Perception & Planning Result")
    plt.xlabel("X Position (Pixels)")
    plt.ylabel("Y Position (Pixels)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save output
    try:
        import os
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        plt.savefig("outputs/final_simulation_run.png", dpi=200, bbox_inches='tight')
        print("Successfully saved output image to outputs/final_simulation_run.png")
    except Exception as e:
        print(f"Error saving image: {e}")

if __name__ == "__main__":
    generate_output_image()
