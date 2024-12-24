import cv2
import os
import logging
from pathlib import Path
from utils import constants
from capture.camera import Camera
from utils import constants
from utils.json_utils import json_to_dict, dict_to_json
from detection.apriltag_detector import AprilTagDetector
from capture.camera_manager import open_stream, open_all_cameras_and_process

def detection_process(camera: Camera, season: int, output_file_path: Path):
    
    cap = open_stream(camera.id)
    if cap is None:
        return

    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        camera_position, detected_apriltags = apriltag_detector.get_camera_and_tags_data(frame=frame)
        cv2.imshow(f'Camera {camera.id} Detection', frame)

        #####################################################
        # HERE WE NEED TO PUSH THE DATA WE GATHERED AND LET THE FUSION FUNCTION TAKE CARE OF IT
        # THE FOLLOWING CODE IS JUST FOR TESTING TILL THAT FUNCTION IS READY

        try:
            robot_position = {"x": camera_position["x"],
                            "y": camera_position["y"],
                            "yaw": camera_position["yaw"]}
        except Exception as e:
            robot_position = constants.UNKOWN

        fused = {"targets": {"notes": [],
                             "robots": [],
                             "apriltags": detected_apriltags},
                 "position": robot_position}
        
        #####################################################

        dict_to_json(output_file_path, {"devices": [], "fused_data": fused})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    output_file_path = Path(__file__).parent / Path("../output/output.json")
    camera_list = [Camera(id=0)]#, Camera(id=1)] # should be replaced with loading the cameras from the config file
    open_all_cameras_and_process(detection_process, camera_list, constants.CRESCENDO ,output_file_path)
