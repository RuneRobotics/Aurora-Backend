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
                 id, 
                 position: Pose3D, 
                 matrix = np.array([[600, 0, 320],  # fx, 0, cx
                                    [0, 600, 240],  # 0, fy, cy
                                    [0, 0, 1]], dtype=np.float32),
                dist_coeffs = np.zeros((4, 1))):
        
        self.id = id
        self.position = position
        self.matrix = matrix
        self.dist_coeffs = dist_coeffs

    def undistort_image_point(self, image_point):

        image_points = np.array([[image_point]], dtype='float32')  # Shape (1, 1, 2)

        undistorted_points = cv2.undistortPoints(image_points, self.matrix, self.dist_coeffs)
        
        return undistorted_points[0][0]  # Return the undistorted point

def distance_to_camera(camera: Camera, bbox, object_width):

    camera_matrix = camera.matrix

    xmin, ymin, xmax, ymax = bbox
    object_width_pixel = xmax - xmin

    focal_length = camera_matrix[0, 0]

    distance = (focal_length * object_width) / object_width_pixel

    return distance