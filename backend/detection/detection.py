import cv2
import os
import json
import logging
import pyapriltags as apriltag
from concurrent.futures import ThreadPoolExecutor
from apriltag_detection.apriltag_detection import detect_apriltags
from camera import Camera, Pose3D


def load_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def open_stream(input_source):
    cap = cv2.VideoCapture(input_source)
    if not cap.isOpened():
        print(f"Error: Could not open the input source {input_source}.")
        return None
    return cap


def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def detection_process(input_source, output_file_path: str, camera: Camera):
    cap = open_stream(input_source)
    if cap is None:
        return

    field_data = load_json(os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json'))
    at_detector = apriltag.Detector(families='tag36h11')

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to capture image from camera {camera.id}.")
            break

        camera_position, detected_apriltags = detect_apriltags(frame=frame, detector=at_detector, field_data=field_data, camera=camera)
        cv2.imshow(f'Camera {camera.id} Detection', frame)


        try:
            robot_position = {"x": camera_position["x"],
                            "y": camera_position["y"],
                            "yaw": camera_position["yaw"]}
        except Exception as e:
            robot_position = "unkown"

        fused = {"targets": {"notes": [],
                             "robots": [],
                             "apriltags": detected_apriltags},
                 "position": robot_position}
        
        save_data(output_file_path, {"devices": [], "fused_data": fused})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def open_all_cameras_and_process(output_file_path: str, camera_positions):
    max_cameras = 1
    input_sources = []
    camera_list = []

    for i in range(max_cameras):
        cap = open_stream(i)
        if cap:
            input_sources.append(i)
            # Create camera metadata
            pose = camera_positions[i]  # You can set specific pose data here
            camera = Camera(id=i, position=pose)  # You can add more metadata to the Camera class as needed
            camera_list.append(camera)
            cap.release()  # Immediately release as we just check availability

    # Start detection process in parallel for each camera
    with ThreadPoolExecutor() as executor:
        futures = []
        for camera in camera_list:
            futures.append(executor.submit(detection_process, camera.id, output_file_path, camera))

        # Wait for all processes to finish
        for future in futures:
            future.result()  # This will raise exceptions if any occurred


if __name__ == '__main__':
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'output.json')
    camera_positions = [Pose3D(), Pose3D()]
    open_all_cameras_and_process(output_file_path, camera_positions=camera_positions)
