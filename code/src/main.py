from flask import Flask, Response, send_from_directory, jsonify, request
from waitress import serve
from queue import Queue
import threading
import time
import cv2
import os
import socket
import struct
from capture.camera_manager import open_threads
from capture.camera import Camera
from slam.sensor_fusion import average_pose3d
from utils.output_formats import data_format
from utils import constants
from capture.calibration_utils import run_directory_calibration
from globals import CURRENT_MODE, MODE_LOCK

app = Flask(__name__, static_folder="networking/dist", static_url_path="")

HOST = "192.168.0.224"
PORT = 5000
data_lock = threading.Lock()
output = {}
CALIBRATION_BASE_PATH = "src/capture/calibration_images"

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

@app.route("/api/mode", methods=["GET"])
def get_mode():
    with MODE_LOCK:
        return jsonify(CURRENT_MODE)

@app.route("/api/mode", methods=["POST"])
def set_mode():
    mode_data = request.get_json()
    mode = mode_data.get("mode")
    camera_id = mode_data.get("camera_id", None)

    if mode not in {"detection", "calibration", "lighting", "settings"}:
        return jsonify({"error": "Invalid mode"}), 400

    with MODE_LOCK:
        CURRENT_MODE["mode"] = mode
        CURRENT_MODE["camera_id"] = camera_id

    return jsonify({"status": "ok", "mode": mode, "camera_id": camera_id})

@app.route("/api/stream_<int:camera_id>")
def stream(camera_id):
    camera = next((cam for cam in camera_list if cam.id == camera_id), None)
    if not camera:
        return "Camera not found", 404

    def generate():
        while True:
            frame = camera.frame
            if frame is None:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def start_system():
    global camera_list
    camera_0 = Camera(id=0)
    camera_1 = Camera(id=1)
    camera_list = [camera_0, camera_1]
    threading.Thread(
        target=open_threads,
        args=(data_fusion, camera_list, constants.REEFSCAPE),
        daemon=True
    ).start()

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

        with data_lock:
            output = data_format(cameras, {}, avg_pose)

        if sock:
            try:
                data = struct.pack('!6f', avg_pose.x, avg_pose.y, avg_pose.z,
                                   avg_pose.roll, avg_pose.pitch, avg_pose.yaw)
                sock.sendall(data)
            except (socket.error, ConnectionResetError):
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

        time.sleep(max(0, constants.UPDATE_INTERVAL - (time.time() - start_time)))

if __name__ == '__main__':
    start_system()
    serve(app, host='0.0.0.0', port=constants.DASHBOARD_PORT)