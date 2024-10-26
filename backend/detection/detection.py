from apriltag_detection.apriltag_detection import detect_ats
from object_detection.object_detection import ObjectDetector, detect_objects
import os
import cv2
import json
import pyapriltags as apriltag
import logging
from camera import Camera, Pose3D

logging.getLogger("ultralytics").setLevel(logging.WARNING)

def load_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def open_stream(input_source):
    if isinstance(input_source, int):  # Camera port
        cap = cv2.VideoCapture(input_source)
    elif os.path.exists(input_source):  # Local video file
        cap = cv2.VideoCapture(input_source)
    else:
        print("Error: Invalid input source. Must be a camera port (int) or a valid video file path.")
        exit()

    if not cap.isOpened():
        print("Error: Could not open the input source.")
        exit()

    return cap

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def detection_process(input_source, output_file_path: str):
    object_detector = ObjectDetector(os.path.join(os.path.dirname(__file__), '..', 'data', 'yolo_weights', 'model.pt'), camera=camera, valid_ids=[3], conf_limit=0.6)
    cap = open_stream(input_source)  # Can be a video file path or camera port
    output_file = output_file_path

    field_data = load_json(os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json'))
    at_detector = apriltag.Detector(families='tag36h11')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image from input source.")
            break

        at_detection_data = detect_ats(frame=frame, detector=at_detector, field_data=field_data, camera=camera)
        object_detection_data, output_frame = detect_objects(camera, object_detector=object_detector, frame=frame)
        
        cv2.imshow('YOLOv8 Detection', output_frame)

        save_data(output_file, object_detection_data | at_detection_data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    input_type = input("Enter 'video' to use a video file or 'camera' to use webcam: ").strip().lower()

    if input_type == 'video':
        video_path = input("Enter the path to the video file: ").strip()
        input_source = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'video1080p.mp4')
    elif input_type == 'camera':
        input_source = 0  # Default webcam port
    else:
        print("Invalid input. Exiting.")
        exit()

    pose = Pose3D()
    camera = Camera(port=input_source if isinstance(input_source, int) else 0, position=pose)  # Camera object needs port even if input is video
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'output.json')

    detection_process(input_source=input_source, output_file_path=output_file_path)