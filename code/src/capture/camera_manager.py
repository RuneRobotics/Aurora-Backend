from concurrent.futures import ThreadPoolExecutor
from capture.camera import Camera
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


def open_all_cameras_and_process(
    data_fusion: callable, 
    detection_process: callable, 
    camera_list: list[Camera], 
    season: int
) -> None:
    """
    Open all cameras and process data using fusion and detection processes.

    Args:
        data_fusion (callable): Function to perform data fusion.
        detection_process (callable): Function to perform detection for each camera.
        camera_list (list[Camera]): List of Camera objects to process.
        season (int): Identifier for the current season.
    """
    fusion_thread = Thread(target=data_fusion, args=(camera_list,))
    fusion_thread.start()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(detection_process, camera, season) for camera in camera_list]
        for future in futures:
            future.result()

    fusion_thread.join()
