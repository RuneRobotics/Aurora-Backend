import logging
import threading
from flask import Flask, send_from_directory, jsonify
from utils import constants
from utils.data_formats import pose3d_format, data_format
import cv2
import os
import numpy as np
import logging
from queue import Queue
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils import constants
from detection.apriltag_detector import AprilTagDetector
from capture.camera_manager import open_stream
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time
from typing import List

output = {}
data_lock = threading.Lock()


def detection_process(camera: Camera, season: int):
    
    cap = open_stream(camera.id)
    if cap is None:
        return
    
    print(f"created detector for camera {camera.id}")
    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)

    
    print(f"starting detection loop for camera {camera.id}")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error(f"Error: Failed to capture image from camera {camera.id}.")
            continue

        apriltag_detector.get_camera_and_tags_data(frame=frame)
        cv2.imshow(f'Camera {camera.id} Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def data_fusion(cameras: List[Camera]):

    global output

    while(True):

        queues = []

        for camera in cameras:
            queues.append(camera.robot_pose_queue)

        with data_lock:
            output = data_format(cameras, {}, queues[0].get())
    
        time.sleep(constants.UPDATE_INTERVAL * 25)


def open_all_cameras_and_process(detection_process, camera_list: list, season: int):

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


app = Flask(__name__, static_folder="networking/dist", static_url_path="")


# Serve React static files
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")


# Serve the React app for all frontend routes
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")


# Example API route
@app.route("/api/data", methods=["GET"]) 
def get_data():

    global output

    with data_lock:
        return jsonify(output) # update the output dict here
    

if __name__ == '__main__':
    
    camera_1 = Camera(id=0, pose_on_robot=Pose3D(x=1, y=1, yaw=np.pi/4))
    camera_list = [camera_1]
    threading.Thread(target=open_all_cameras_and_process, args=(detection_process, camera_list, constants.CRESCENDO), daemon=True).start()
    app.run(debug=False, port=constants.DASHBOARD_PORT)