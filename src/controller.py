import math

class PurePursuitController:
    """
    Implements the Pure Pursuit path tracking algorithm.
    It computes the steering angle required for the vehicle to follow a desired path.
    """
    def __init__(self, lookahead_distance=20.0, linear_velocity=2.0):
        self.ld = lookahead_distance
        self.v = linear_velocity
        self.path = []
        self.target_idx = 0

    def update_path(self, new_path):
        self.path = new_path
        self.target_idx = 0

    def calculate_distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def get_control_commands(self, vehicle_pos, vehicle_angle):
        """
        Returns (velocity, steering_angle) to reach the next target node.
        """
        if not self.path or self.target_idx >= len(self.path):
            return 0.0, 0.0 # Stop

        # Find the appropriate lookahead point
        target_point = self.path[self.target_idx]
        dist = self.calculate_distance(vehicle_pos, target_point)
        
        if dist < self.ld:
            self.target_idx += 1
            if self.target_idx >= len(self.path):
                self.target_idx = len(self.path) - 1 # Stay at goal
                target_point = self.path[self.target_idx]
                return 0.0, 0.0 # Arrived
            target_point = self.path[self.target_idx]

        # Calculate Heading Error (Alpha)
        # alpha = target_angle - vehicle_angle
        target_angle = math.atan2(target_point[1] - vehicle_pos[1], target_point[0] - vehicle_pos[0])
        alpha = target_angle - vehicle_angle
        
        # Normalize alpha to [-pi, pi]
        alpha = math.atan2(math.sin(alpha), math.cos(alpha))
        
        # Steering command (simple P controller basically)
        steering_command = alpha * 0.1 # Soft scaling gain
        
        return self.v, steering_command
