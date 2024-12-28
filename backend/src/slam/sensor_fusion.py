from queue import Queue
from typing import List
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
import time
import json

def fuse_data(cameras: List[Camera], fused_output_file: Path):
    while(True):

        queues = []

        for camera in cameras:
            queues.append(camera.robot_pose_queue)

        # send the queues to the ekf function

        print(pose3d_format(queues[0].get()))

        # update final output here

        time.sleep(constants.UPDATE_INTERVAL*25)
