import cv2
import os
import logging
from queue import Queue
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils import constants
from utils.json_utils import json_to_dict, dict_to_json
from detection.apriltag_detector import AprilTagDetector
from capture.camera_manager import open_stream, open_all_cameras_and_process
import numpy as np


def detection_process(camera: Camera, season: int):
    
    cap = open_stream(camera.id)
    if cap is None:
        return
    
    print(f"created detector for camera {camera.id}")
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    
    print(f"starting loop for camera {camera.id}")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        apriltag_detector.get_camera_and_tags_data(frame=frame)
        cv2.imshow(f'Camera {camera.id} Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    camera_1 = Camera(id=0, pose_on_robot=Pose3D(yaw=-np.pi/6, pitch = np.pi/4))

    output_file_path = Path(__file__).parent / Path("../output/output.json")
    camera_list = [camera_1]
    open_all_cameras_and_process(detection_process, camera_list, constants.CRESCENDO ,output_file_path)
