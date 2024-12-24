from capture.camera import Camera, Pose3D
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import cv2


def open_stream(input_source):
    cap = cv2.VideoCapture(input_source)
    if not cap.isOpened():
        print(f"Error: Could not open the input source {input_source}.")
        return None
    return cap


def open_all_cameras_and_process(detection_process, camera_list: list, season: int, output_file_path: Path):

    # Start detection process in parallel for each camera
    with ThreadPoolExecutor() as executor:
        futures = []
        for camera in camera_list:
            futures.append(executor.submit(detection_process, camera, season, output_file_path))

        # Wait for all processes to finish
        for future in futures:
            future.result()  # This will raise exceptions if any occurred