from capture.camera_manager import open_stream, open_all_cameras_and_process
from flask import Flask, send_from_directory, jsonify
from detection.detection_process import run_detection
from slam.sensor_fusion import average_pose3d
from utils.output_formats import data_format
from capture.camera import Camera
from utils import constants
from queue import Queue
from typing import List
import threading
import time

app = Flask(__name__, static_folder="networking/dist", static_url_path="")
data_lock = threading.Lock()
output = {}


def data_fusion(cameras: List[Camera]):

    global output

    while(True):

        avg_poses = Queue()

        for camera in cameras:
            copy_queue = camera.robot_pose_queue
            avg_poses.put(average_pose3d(copy_queue)) # need to replace with weighted avg

        avg_pose = average_pose3d(avg_poses)

        with data_lock:
            output = data_format(cameras, {}, avg_pose)
    
        time.sleep(constants.UPDATE_INTERVAL)


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
        return jsonify(output)
    

if __name__ == '__main__':
    
    camera_1 = Camera(id=0)
    camera_list = [camera_1]
    threading.Thread(target=open_all_cameras_and_process, args=(data_fusion, run_detection, camera_list, constants.REEFSCAPE), daemon=True).start()
    app.run(debug=False, port=constants.DASHBOARD_PORT)