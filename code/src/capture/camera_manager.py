from concurrent.futures import ThreadPoolExecutor
from globals import CURRENT_MODE, MODE_LOCK
from threading import Thread
import cv2


def open_stream(input_source: str | int) -> cv2.VideoCapture | None:
    """
    Open a video stream from an input source.

    Args:
        input_source (str | int): Path to the video file or camera index.

    Returns:
        cv2.VideoCapture | None: Opened video capture object if successful, or None if failed.
    """
    cap = cv2.VideoCapture(input_source)
    if not cap.isOpened():
        print(f"Error: Could not open the input source {input_source}.")
        return None
    return cap


def open_threads(data_fusion, camera_list, season):
    fusion_thread = Thread(target=data_fusion, args=(camera_list,))
    fusion_thread.start()

    def camera_worker(camera):

        cap = open_stream(camera.id)
        if cap is None:
            # log that?
            return
        
        while True:

            ret, frame = cap.read()
            camera.frame = frame

            if not ret:
                #logging.error(f"Error: Failed to capture image from camera {camera.id}.")
                continue

            with MODE_LOCK:
                mode = CURRENT_MODE["mode"]
                target_id = CURRENT_MODE["camera_id"]

            if mode == "detection":
                camera.run_detection()

            elif mode in {"calibration", "lighting", "settings"}:
                if camera.id == target_id:
                    select_mode(camera, mode)
                else:
                    camera.run_stream()
            else:
                camera.run_stream()

    with ThreadPoolExecutor() as executor:
        executor.map(camera_worker, camera_list)

    fusion_thread.join()

def select_mode(camera, mode):
    if mode == "calibration":
        camera.run_calibration()
    elif mode == "lighting":
        camera.run_lighting()
    elif mode == "settings":
        camera.run_settings()

