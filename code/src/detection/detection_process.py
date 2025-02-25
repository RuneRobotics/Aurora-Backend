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
    
    print(f"created detector for camera {camera.id}")
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    
    print(f"starting detection loop for camera {camera.id}")

    while True:
        ret, frame = cap.read()
        camera.frame = frame
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        apriltag_detector.get_camera_and_tags_data(frame=frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()


def run_slow_detection(camera: Camera, season: int):
    
    cap = open_stream(camera.id)
    if cap is None:
        return
    
    print(f"created detector for camera {camera.id}")
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    
    print(f"starting detection loop for camera {camera.id}")

    while True:
        ret, frame = cap.read()
        camera.frame = frame
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        apriltag_detector.get_camera_and_tags_data(frame=frame)

        time.sleep(800)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()


def run_detection_test(camera: Camera, season: int):
    
    print(f"created detector for camera {camera.id}")
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    
    print(f"starting detection loop for camera {camera.id}")

    while True:

        image_path = Path("code\src\\test_image_0.jpg")

        if not image_path.exists():
            print(f"Error: Image not found at {image_path.resolve()}")
        else:
            frame = cv2.imread(str(image_path))
            if frame is None:
                print("Error: Image could not be loaded")
            else:
                camera.frame = frame
                if not True:
                    logging.error(f"Error: Failed to capture image from camera {camera.id}.")
                    continue

                apriltag_detector.get_camera_and_tags_data(frame=frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()