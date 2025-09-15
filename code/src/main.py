from flask import Flask, Response, send_from_directory, jsonify, request, send_file
from waitress import serve
import numpy as np
from queue import Queue
import threading
import time
import cv2
import os
from pathlib import Path
import json
import socket
import struct

from capture.camera_manager import open_threads, count_connected_cameras
from capture.camera import Camera
from capture.camera_calibration import calibrate_camera, delete_image, save_image
from slam.sensor_fusion import average_pose3d
from utils.output_formats import data_format
from utils import constants
import globals

app = Flask(__name__, static_folder="networking/dist", static_url_path="")

HOST = "192.168.0.224"
PORT = 5000

data_lock = threading.Lock()
output = {}
camera_list = []
CALIBRATION_BASE_PATH = "src/capture/calibration_images"


def load_camera_settings():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'capture', 'cameras_settings.json')
    with open(json_path) as f:
        return json.load(f), json_path


def save_camera_settings(settings, path):
    def convert(o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return o  # let json handle everything else

    with open(path, 'w') as f:
        json.dump(settings, f, indent=4, default=convert)


def validate_camera_id(camera_id, settings):
    return 0 <= camera_id < len(settings)


def stream_generator(camera):
    while True:
        frame = camera.display_frame
        if frame is None:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


def update_output(cameras, avg_pose):
    global output
    with data_lock:
        output = data_format(cameras, {}, avg_pose)


import json

def data_fusion(cameras):
    global output
    sock = None
    last_socket_attempt = 0

    while True:
        start_time = time.time()
        avg_poses = Queue()

        for camera in cameras:
            avg_poses.put(average_pose3d(camera.robot_pose_queue))

        avg_pose = average_pose3d(avg_poses)
        update_output(cameras, avg_pose)

        if sock:
            try:
                # Example: generate some dummy corals (replace with real detections later)
                corals = [{"x": 1.0, "y": 2.0}, {"x": 2.5, "y": 3.5}]

                message = {
                    "pose": {
                        "x": avg_pose.x,
                        "y": avg_pose.y,
                        "z": avg_pose.z,
                        "roll": avg_pose.roll,
                        "pitch": avg_pose.pitch,
                        "yaw": avg_pose.yaw
                    },
                    "corals": corals
                }

                data = json.dumps(message).encode("utf-8") + b"\n"  # newline-delimited JSON
                sock.sendall(data)

            except (socket.error, ConnectionResetError, BrokenPipeError):
                print("Lost connection to the server. Closing socket.")
                sock.close()
                sock = None

        if not sock and (time.time() - last_socket_attempt) > 3:
            last_socket_attempt = time.time()
            try:
                print("Attempting to connect to the server...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.05)
                sock.connect((HOST, PORT))
                print("Connected to the server.")
            except (socket.error, ConnectionResetError):
                print("Connection failed. Will retry in 3 seconds.")
                sock = None

        print((time.time() - start_time))
        time.sleep(max(0, constants.UPDATE_INTERVAL - (time.time() - start_time)))


def start_system():
    global camera_list

    num_of_cams = count_connected_cameras()
    camera_settings, json_path = load_camera_settings()
    num_of_cams_in_file = len(camera_settings)
    
    camera_list = [Camera(cam_id) for cam_id in range(min(num_of_cams_in_file, num_of_cams))]
    
    if num_of_cams < num_of_cams_in_file:
        camera_settings = camera_settings[:num_of_cams]
        save_camera_settings(camera_settings, json_path)
    elif num_of_cams > num_of_cams_in_file:
        for cam_id in range(num_of_cams_in_file, num_of_cams):
            camera_settings.append(constants.DEFAULT_CAMERA)
            save_camera_settings(camera_settings, json_path)
            camera_list.append(Camera(cam_id))

    threading.Thread(
        target=open_threads,
        args=(data_fusion, camera_list, constants.REEFSCAPE),
        daemon=True
    ).start()


@app.route("/")
def serve_static():
    return send_from_directory(app.static_folder, "index.html")


@app.errorhandler(404)
def not_found(_):
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/data", methods=["GET"])
def get_data():
    with data_lock:
        return jsonify(output)


@app.route("/api/device", methods=["GET"])
def get_device_data():
    with data_lock:
        return jsonify({"cameras": output["cameras"]})


@app.route("/api/detection", methods=["GET"])
def get_fused_detection():
    with data_lock:
        return jsonify(output["fused_data"])


@app.route("/api/mode", methods=["GET", "POST"])
def handle_mode():
    if request.method == "GET":
        with globals.MODE_LOCK:
            return jsonify(globals.CURRENT_MODE)

    mode_data = request.get_json()
    mode = mode_data.get("mode")
    camera_id = mode_data.get("camera_id", None)

    if mode not in {"Detection", "Calibration", "Lighting", "Settings"}:
        return jsonify({"error": "Invalid mode"}), 400

    with globals.MODE_LOCK:
        globals.CURRENT_MODE["mode"] = mode
        globals.CURRENT_MODE["camera_id"] = camera_id

    return jsonify({"status": "ok", "mode": mode, "camera_id": camera_id})


@app.route('/api/settings_<int:camera_id>', methods=['GET', 'POST'])
def handle_camera_settings(camera_id):
    camera_settings, json_path = load_camera_settings()

    if request.method == "GET":
        if validate_camera_id(camera_id, camera_settings):
            return jsonify(camera_settings[camera_id]["settings"])
        return jsonify({"error": "Invalid camera ID"}), 404

    new_settings = request.get_json()
    if not new_settings:
        return jsonify({"error": "Missing settings data"}), 400

    required_keys = {"fps", "name", "pitch", "roll", "x", "y", "yaw", "z"}
    if not required_keys.issubset(new_settings):
        return jsonify({"error": "Missing required fields"}), 400

    with globals.SETTINGS_LOCK:
        if validate_camera_id(camera_id, camera_settings):
            camera_settings[camera_id]["settings"] = new_settings
            save_camera_settings(camera_settings, json_path)
            globals.SETTINGS_CHANGED = True
            return jsonify({"status": "ok", "camera_id": camera_id, "updated_settings": new_settings})

        return jsonify({"error": "Invalid camera ID"}), 404


@app.route('/api/calibration_settings', methods=['GET', 'POST'])
def handle_calibration_settings():
    camera_settings, json_path = load_camera_settings()

    with globals.MODE_LOCK:
        camera_id = globals.CURRENT_MODE["camera_id"]

    if request.method == "GET":
            return jsonify(camera_settings[camera_id]["calibration"])

    new_calibration = request.get_json()
    if not new_calibration:
        return jsonify({"error": "Missing calibration data"}), 400

    required_keys = {'rows', 'columns', 'sideLength', 'imageSize'}
    if not required_keys.issubset(new_calibration):
        return jsonify({"error": "Missing required fields"}), 400

    with globals.SETTINGS_LOCK:
        if validate_camera_id(camera_id, camera_settings):
            camera_settings[camera_id]["calibration"] = new_calibration
            save_camera_settings(camera_settings, json_path)
            globals.SETTINGS_CHANGED = True
            return jsonify({"status": "ok", "camera_id": camera_id, "updated_calibration_settings": new_calibration})

        return jsonify({"error": "Invalid camera ID"}), 404


@app.route("/api/stream_<int:camera_id>")
def stream(camera_id):
    camera = next((cam for cam in camera_list if cam.id == camera_id), None)
    if not camera:
        return "Camera not found", 404
    return Response(stream_generator(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/api/calibration/operation", methods=["POST"])
def handle_calibration_operation():
    operation = request.get_json().get("operation")
    index = -1
    camera_id = -1

    with globals.MODE_LOCK:
        camera_id = globals.CURRENT_MODE["camera_id"]

    frame = camera_list[camera_id].frame
    display_frame = camera_list[camera_id].display_frame

    if operation == "Delete":
        index = request.get_json().get("index")
        delete_image(index, "calibration_images")
        delete_image(index, "display_images")
        return jsonify({"status": "ok"})

    if operation == "Snapshot":
        index = save_image(frame, "calibration_images")
        _ = save_image(display_frame, 'display_images')
        return jsonify({"status": "ok", "index": index})

    if operation == "Calibration":
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'capture', 'calibration_images')
        calibration_settings = camera_list[camera_id].calibration
        result = calibrate_camera(image_dir=dir_path, calibration_settings=calibration_settings)
        num_files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
        for i in range (0, num_files):
            delete_image(0, "calibration_images")
            delete_image(0, "display_images")
        
        with globals.SETTINGS_LOCK:
            camera_settings, json_path = load_camera_settings()
            camera_settings[camera_id]["matrix"] = result["matrix"]
            camera_settings[camera_id]["distortion"] = result["distortion"]
            save_camera_settings(camera_settings, json_path)
            globals.SETTINGS_CHANGED = True
        return jsonify({"status": "ok"})
    
    return jsonify({"error": "Invalid Operation"}), 404


@app.route("/api/calibration_amount", methods=["GET"])
def get_calibration_amount():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'capture', 'calibration_images')
    num_files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    return jsonify(num_files)

@app.route('/api/calibration/snapshot_<int:index>')
def serve_calibration_image(index):
    image_dir = Path(__file__).resolve().parent / 'capture' / 'display_images'
    file_path = image_dir / f'image_{index}.png'

    if not file_path.exists():
        return jsonify({"error": "Image not found"}), 404

    return send_file(file_path, mimetype='image/png')

if __name__ == '__main__':
    start_system()
    serve(app, host='0.0.0.0', port=constants.DASHBOARD_PORT)
