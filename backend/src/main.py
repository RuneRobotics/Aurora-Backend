from detection.apriltag_detector import AprilTagDetector
from flask import Flask, send_from_directory, jsonify
from concurrent.futures import ThreadPoolExecutor
from capture.camera_manager import open_stream
from utils.data_formats import data_format
from capture.camera import Camera, Pose3D
from threading import Thread
from queue import Queue
from utils import constants
from typing import List
import threading
import logging
import time
import cv2

app = Flask(__name__, static_folder="networking/dist", static_url_path="")
data_lock = threading.Lock()
output = {}


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


def average_pose3d(pose_queue):
    total_x = total_y = total_z = 0.0
    total_roll = total_pitch = total_yaw = 0.0
    count = 0

    # Create a copy of the queue to iterate without removing elements
    queue_list = list(pose_queue.queue)

    for pose in queue_list:
        total_x += pose.x
        total_y += pose.y
        total_z += pose.z
        total_roll += pose.roll
        total_pitch += pose.pitch
        total_yaw += pose.yaw
        count += 1

    if count == 0:
        return Pose3D()  # Return a default Pose3D if queue is empty

    avg_pose = Pose3D(
        x=total_x / count,
        y=total_y / count,
        z=total_z / count,
        roll=total_roll / count,
        pitch=total_pitch / count,
        yaw=total_yaw / count
    )

    return avg_pose


def data_fusion(cameras: List[Camera]):

    global output

    while(True):

        queues = []

        avg_poses = Queue()

        for camera in cameras:
            copy_queue = camera.robot_pose_queue
            avg_poses.put(average_pose3d(copy_queue)) # need to replace with weighted avg

        avg_pose = average_pose3d(avg_poses)

        with data_lock:
            output = data_format(cameras, {}, avg_pose)
    
        time.sleep(constants.UPDATE_INTERVAL)


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
    
    camera_1 = Camera(id=0)
    camera_list = [camera_1]
    threading.Thread(target=open_all_cameras_and_process, args=(detection_process, camera_list, constants.CRESCENDO), daemon=True).start()
    app.run(debug=False, port=constants.DASHBOARD_PORT)