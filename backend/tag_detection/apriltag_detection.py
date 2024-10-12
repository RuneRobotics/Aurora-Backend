import cv2
import numpy as np
import pyapriltags as apriltag
import json
import os

def load_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json')
world_data = load_json(json_file_path)

# Function to convert quaternion to rotation matrix
def quaternion_to_rotation_matrix(q):
    w, x, y, z = q['W'], q['X'], q['Y'], q['Z']
    rot_matrix = np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
        [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y]
    ], dtype=np.float32)
    return rot_matrix

# Define the camera matrix (example values, replace with actual calibration values)
camera_matrix = np.array([[600, 0, 320],  # fx, 0, cx
                          [0, 600, 240],  # 0, fy, cy
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

# Initialize the AprilTag detector
detector = apriltag.Detector(families='tag36h11')

# Capture from camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the image
    detections = detector.detect(gray)

    world_points = []
    image_points = []

    for detection in detections:
        tag_id = detection.tag_id
        image_corners = np.array(detection.corners, dtype=np.float32)

        # Draw green square around detected AprilTags
        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the frame
    cv2.imshow("Detected AprilTags", frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()