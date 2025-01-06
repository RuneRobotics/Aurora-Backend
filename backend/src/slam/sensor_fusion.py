from queue import Queue
from typing import List
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils.output_formats import pose3d_format, data_format
from slam.kalman_filter import KalmanFilter
import time
from math import radians, degrees, pi
import numpy as np
from utils.json_utils import dict_to_json

def data_fusion(cameras: List[Camera], output: Path):

    while(True):

        queues = []

        for camera in cameras:
            queues.append(camera.robot_pose_queue)

        dict_to_json(output, data_format(cameras, {}, queues[0].get()))
    
        time.sleep(constants.UPDATE_INTERVAL)