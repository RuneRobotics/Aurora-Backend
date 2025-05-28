import numpy as np
from math import radians, degrees, pi
from utils.pose3d import Pose3D

class KalmanFilter:
    def __init__(self, process_noise=0.01, measurement_noise=0.1, num_cameras=1):
        self.state_dim = 6  # [x, y, z, roll, pitch, yaw]
        self.num_cameras = num_cameras

        # Initial state and covariance
        self.x = np.zeros((self.state_dim, 1))  # [x, y, z, roll, pitch, yaw]
        self.P = np.eye(self.state_dim)  # Covariance

        # Process and measurement noise
        self.Q = np.eye(self.state_dim) * process_noise
        self.R = np.eye(self.state_dim * num_cameras) * measurement_noise

    def normalize_angles(self):
        # Normalize roll, pitch, yaw to [-pi, pi]
        for i in range(3, 6):  # Indices of roll, pitch, yaw
            self.x[i, 0] = (self.x[i, 0] + pi) % (2 * pi) - pi

    def predict(self):
        # State prediction
        self.x = self.x  # No motion model, state stays the same
        self.P = self.P + self.Q

    def update(self, measurements):
        # Stack measurements and build H matrix
        Z = np.vstack(measurements)  # [z1, z2, ..., zN]
        H = np.eye(self.state_dim * self.num_cameras, self.state_dim)

        # Kalman gain
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state and covariance
        self.x = self.x + K @ (Z - H @ self.x)
        self.P = (np.eye(self.state_dim) - K @ H) @ self.P

        # Normalize angles after update
        self.normalize_angles()

    def get_state(self):
        # Convert state to Pose3D
        x, y, z, roll, pitch, yaw = self.x.flatten()
        return Pose3D(x, y, z, degrees(roll), degrees(pitch), degrees(yaw))
