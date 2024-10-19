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

def open_stream(camera: Camera):

    cap = cv2.VideoCapture(camera.port)

    if not cap.isOpened():
        print("Error: Could not open video stream from webcam.")
        exit()
    
    return cap

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def detection_process(camera: Camera, output_file_path: str):
    object_detector = ObjectDetector(os.path.join(os.path.dirname(__file__), '..', 'data', 'yolo_weights', 'model.pt'), camera=camera, valid_ids=[3] , conf_limit=0.6)
    cap = open_stream(camera)
    output_file = output_file_path

    field_data = load_json(os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json'))
    at_detector = apriltag.Detector(families='tag36h11')
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image from webcam.")
            break

        at_detection_data = detect_ats(frame=frame, detector=at_detector, field_data=field_data, camera=camera)
        object_detection_data, output_frame = detect_objects(camera, object_detector=object_detector, frame=frame)
        
        cv2.imshow('YOLOv8 Webcam Detection', output_frame)

        save_data(output_file, object_detection_data | at_detection_data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    pose = Pose3D()
    camera = Camera(port=0, position=pose)
    detection_process(camera=camera, output_file_path=os.path.join(os.path.dirname(__file__), '..', 'output', 'output.json'))
