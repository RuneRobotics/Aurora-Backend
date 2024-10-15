import numpy as np
import cv2

class Pose3D:
    def __init__(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

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

    def undistort_image_point(self, image_point):

        image_points = np.array([[image_point]], dtype='float32')  # Shape (1, 1, 2)

        undistorted_points = cv2.undistortPoints(image_points, self.matrix, self.dist_coeffs)
        
        return undistorted_points[0][0]  # Return the undistorted point

import numpy as np

def position_relative_to_camera(camera: Camera, xyxy, known_y):
    pixel_coords = ((xyxy[0][0] + xyxy[0][2]) / 2, (xyxy[0][1] + xyxy[0][3]) / 2)
    np.array([[pixel_coords]], dtype=np.float32)

    undistorted_point = cv2.undistortPoints(pixel_coords, camera.matrix, camera.dist_coeffs)

    camera_matrix_inv = np.linalg.inv(camera.matrix)
    undistorted_point_homog = np.array([undistorted_point[0][0][0], undistorted_point[0][0][1], 1])
    
    s = known_y / undistorted_point_homog[1]
    
    # Step 3: Compute the world coordinates
    world_coords = s * camera_matrix_inv.dot(undistorted_point_homog)
    
    # Set the y-value in the result to the known y_world
    return (world_coords[0], world_coords[2])


