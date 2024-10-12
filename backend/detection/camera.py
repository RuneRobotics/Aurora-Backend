import numpy as np

class Pose3D:
    def __init__(self, x, y, z, roll, pitch, yaw):
        pass

class Camera:
    def __init__(self,
                 port, 
                 position: Pose3D, 
                 matrix = np.array([[600, 0, 320],  # fx, 0, cx
                                    [0, 600, 240],  # 0, fy, cy
                                    [0, 0, 1]], dtype=np.float32),
                dist_coeffs = np.zeros((4, 1))):
        
        self.port = port
        self.position = position
        self.matrix = matrix
        self.dist_coeffs = dist_coeffs