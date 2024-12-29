from queue import Queue
from typing import List
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils.data_formats import pose3d_format
from slam.kalman_filter import KalmanFilter
import time
from math import radians, degrees, pi
import numpy as np

def fuse_data(cameras: List[Camera], fused_output_file: Path):

    num_cameras = len(cameras)
    kf = KalmanFilter(process_noise=0.01, measurement_noise=0.1, num_cameras=num_cameras)

    while(True):

        queues = []

        for camera in cameras:
            queues.append(camera.robot_pose_queue)

        print(pose3d_format(queues[0].get()))

        time.sleep(constants.UPDATE_INTERVAL*25)
