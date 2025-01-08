from capture.camera import Camera, Pose3D
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Thread
from utils import constants
from queue import Queue
import cv2
from multiprocessing import Process
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def open_stream(input_source):
    cap = cv2.VideoCapture(input_source)
    if not cap.isOpened():
        print(f"Error: Could not open the input source {input_source}.")
        return None
    return cap


def open_all_cameras_and_process(data_fusion, detection_process, camera_list: list, season: int):

    # Start the fusion process in a separate thread
    fusion_thread = Thread(target=data_fusion, args=(camera_list, ))
    fusion_thread.start()

    # Start detection process in parallel for each camera
    with ThreadPoolExecutor() as executor:
        futures = []
        for camera in camera_list:
            futures.append(executor.submit(detection_process, camera, season))

        # Wait for all processes to finish
        for future in futures:
            future.result()  # This will raise exceptions if any occurred

    fusion_thread.join()
    