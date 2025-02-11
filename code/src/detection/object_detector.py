from capture.camera import Camera, Pose3D
from ultralytics import YOLO
from utils import constants
import numpy as np
import logging
import torch
import cv2


class ObjectDetector:
    """
    Detects objects using YOLOv8 and estimates their positions in the robot's coordinate system.
    """
    
    def __init__(self, camera: Camera, model_path: str = "yolov8n.pt"):
        """
        Initialize the object detector.
        
        Args:
            camera (Camera): The camera instance associated with the detector.
            model_path (str): Path to the YOLOv8 model file.
        """
        self.camera = camera
        self.camera_matrix = camera.matrix
        self.dist_coeffs = camera.dist_coeffs
        
        # Check for CUDA availability and use GPU if possible
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path).to(self.device)
        self.object_sizes = constants.OBJECT_SIZES  # Dictionary of real-world object sizes
        
    def detect_objects(self, frame: np.ndarray):
        """
        Detect objects in a frame and estimate their positions.
        
        Args:
            frame (np.ndarray): The input video frame.
        
        Returns:
            list: Detected objects with positions in real-world coordinates.
        """
        frame_tensor = torch.from_numpy(frame).to(self.device)
        results = self.model(frame_tensor)
        detected_objects = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                object_name = result.names[class_id]
                bbox = box.xyxy[0].cpu().numpy()  # Bounding box (x_min, y_min, x_max, y_max)
                
                if object_name not in self.object_sizes:
                    logging.warning(f"Unknown object '{object_name}', skipping.")
                    continue
                
                object_position = self.__estimate_object_position(bbox, object_name)
                real_world_position = self.__transform_to_world_coords(object_position)
                
                detected_objects.append({
                    "name": object_name,
                    "position": real_world_position
                })
                
                # Draw bounding box
                x_min, y_min, x_max, y_max = bbox.astype(int)
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), constants.PURPLE, 2)
                cv2.putText(frame, object_name, (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, constants.PURPLE, 2)
        
        return detected_objects
    
    def __estimate_object_position(self, bbox: np.ndarray, object_name: str) -> Pose3D:
        """
        Estimate the camera-relative position of an object using SolvePnP.
        
        Args:
            bbox (np.ndarray): Bounding box (x_min, y_min, x_max, y_max).
            object_name (str): Name of the detected object.
        
        Returns:
            Pose3D: Estimated position of the object in the camera's coordinate system.
        """
        x_min, y_min, x_max, y_max = bbox
        object_width, object_height = self.object_sizes[object_name]
        
        object_world_corners = np.array([
            [-object_width / 2, -object_height / 2, 0],
            [object_width / 2, -object_height / 2, 0],
            [object_width / 2, object_height / 2, 0],
            [-object_width / 2, object_height / 2, 0]
        ], dtype=np.float32)
        
        image_corners = np.array([
            [x_min, y_min],
            [x_max, y_min],
            [x_max, y_max],
            [x_min, y_max]
        ], dtype=np.float32)
        
        success, rvec, tvec = cv2.solvePnP(object_world_corners, image_corners, 
                                           self.camera_matrix, self.dist_coeffs)
        
        if not success:
            raise Exception(f"SolvePnP failed for object: {object_name}")
        
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        camera_position = -rotation_matrix.T @ tvec
        
        return Pose3D(
            x=camera_position[0, 0],
            y=camera_position[1, 0],
            z=camera_position[2, 0],
            roll=rvec[0, 0],
            pitch=rvec[1, 0],
            yaw=rvec[2, 0]
        )
    
    def __transform_to_world_coords(self, object_pose: Pose3D) -> Pose3D:
        """
        Transform object coordinates from the camera frame to the real-world frame.
        
        Args:
            object_pose (Pose3D): Object position relative to the camera.
        
        Returns:
            Pose3D: Object position in the real-world coordinate system.
        """
        camera_pose = self.camera.field_pose
        
        object_position_camera = np.array([object_pose.x, object_pose.y, object_pose.z, 1])
        
        # Convert camera pose to transformation matrix
        camera_rotation = camera_pose.get_rotation_matrix()
        camera_translation = np.array([camera_pose.x, camera_pose.y, camera_pose.z]).reshape((3, 1))
        
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = camera_rotation
        transformation_matrix[:3, 3] = camera_translation.flatten()
        
        # Transform object position
        object_position_world = transformation_matrix @ object_position_camera
        
        return Pose3D(
            x=object_position_world[0],
            y=object_position_world[1],
            z=object_position_world[2],
            roll=object_pose.roll,
            pitch=object_pose.pitch,
            yaw=object_pose.yaw
        )
