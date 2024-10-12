from apriltag_detection.apriltag_detection import load_json, get_camera_dist_coeffs, get_camera_matrix, detect_ats
from object_detection.object_detection import YOLOv8Detector, detect_objects
import os
import cv2
import json
import pyapriltags as apriltag

def open_stream(port: int):

    cap = cv2.VideoCapture(port)

    if not cap.isOpened():
        print("Error: Could not open video stream from webcam.")
        exit()
    
    return cap

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def detection_process(port, output_file_path: str):
    object_detector = YOLOv8Detector(os.path.join(os.path.dirname(__file__), '..', 'data', 'yolo_weights', 'model.pt'))
    cap = open_stream(port)
    output_file = output_file_path

    field_data = load_json(os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json'))
    camera_matrix = get_camera_matrix()
    dist_coeffs = get_camera_dist_coeffs()
    at_detector = apriltag.Detector(families='tag36h11')
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image from webcam.")
            break

        at_detection_data = detect_ats(frame=frame, detector=at_detector)
        object_detection_data, output_frame = detect_objects(yolo_detector=object_detector, frame=frame)
        

        cv2.imshow('YOLOv8 Webcam Detection', output_frame)

        save_data(output_file, object_detection_data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detection_process(0, os.path.join(os.path.dirname(__file__), '..', 'output', 'output.json'))
