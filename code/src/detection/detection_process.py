from capture.camera import Camera
from capture.camera_manager import open_stream
from detection.apriltag_detector import AprilTagDetector
import logging
import cv2
from pathlib import Path
import time

def run_detection(camera: Camera, season: int):
    
    cap = open_stream(camera.id)
    if cap is None:
        return
    
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    while True:
        ret, frame = cap.read()
        camera.frame = frame
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        apriltag_detector.get_camera_and_tags_data(frame=frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()