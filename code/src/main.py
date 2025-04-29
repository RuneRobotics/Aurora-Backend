from capture.camera_manager import open_stream, open_all_cameras_and_process
from flask import Flask, Response, send_from_directory, jsonify
from detection.detection_process import run_detection
from slam.sensor_fusion import average_pose3d
from utils.output_formats import data_format
from capture.camera import Camera
from utils import constants
from waitress import serve
from queue import Queue
from typing import List
import threading
import time
import cv2
import socket
import struct

app = Flask(__name__, static_folder="networking/dist", static_url_path="")
data_lock = threading.Lock()
output = {}
HOST = "192.168.0.224"
PORT = 5000

def data_fusion(cameras: List[Camera]):
    global output
    sock = None  # Initialize socket as None
    last_socket_attempt = 0  # Track last connection attempt time

    while True:
        start_time = time.time()

        # Compute avg_pose
        avg_poses = Queue()
        for camera in cameras:
            copy_queue = camera.robot_pose_queue
            avg_poses.put(average_pose3d(copy_queue))  # Replace with weighted avg if needed

        avg_pose = average_pose3d(avg_poses)

        # Update JSON output (fast updates for the frontend)
        with data_lock:
            output = data_format(cameras, {}, avg_pose)

        # Attempt to send data if connected
        if sock:
            try:
                data = struct.pack('!6f', avg_pose.x, avg_pose.y, avg_pose.z, avg_pose.roll, avg_pose.pitch, avg_pose.yaw)
                sock.sendall(data)
            except (socket.error, ConnectionResetError):
                print("Lost connection to the server. Closing socket.")
                sock.close()
                sock = None  # Reset socket to trigger reconnection

        # Handle reconnection attempts (every 3 seconds)
        if sock is None and (time.time() - last_socket_attempt) > 3:
            last_socket_attempt = time.time()  # Update attempt timestamp
            try:
                print("Attempting to connect to the server...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.05)  # Prevent long blocking
                sock.connect((HOST, PORT))
                print("Connected to the server.")
            except (socket.error, ConnectionResetError):
                print("Connection failed. Will retry in 3 seconds.")
                sock = None  # Keep it None until successful

        # Sleep only for the remaining update interval time
        elapsed_time = time.time() - start_time
        sleep_time = max(0, constants.UPDATE_INTERVAL - elapsed_time)
        time.sleep(sleep_time * 100)

# Serve React static files
@app.route("/")
def serve_static():
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

@app.route("/stream_<int:camera_id>")
def stream(camera_id):
    # Find the camera by ID
    camera = next((cam for cam in camera_list if cam.id == camera_id), None)
    if camera is None:
        return "Camera not found", 404

    # Create a generator to stream frames
    def generate():
        while True:
            # Get the latest frame from the camera (assuming the camera has a method like get_frame())
            frame = camera.frame  # You need to implement this method in the Camera class
            if frame is None:
                break  # Stop if no frame is available

            # Convert the frame to JPEG format for streaming
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break

            # Yield the frame as a multipart response (MJPEG format)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera_0 = Camera(id=0)
    camera_list = [camera_0]
    threading.Thread(target=open_all_cameras_and_process, args=(data_fusion, run_detection, camera_list, constants.REEFSCAPE), daemon=True).start()

    # Use Waitress to serve the Flask app (this replaces app.run)
    serve(app, host='0.0.0.0', port=constants.DASHBOARD_PORT)
