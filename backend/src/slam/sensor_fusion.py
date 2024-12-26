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


def camera_dict_format(camera: Camera):

    return {"camera_id": camera.id,
            "targets": {camera.deteceted_apriltags},
            "camera_position": pose3d_format(camera.field_position)}


def pose3d_format(pose: Pose3D):

    return {"x": pose.x,
            "y": pose.y,
            "z": pose.z,
            "roll": pose.roll,
            "pitch": pose.pitch,
            "yaw": pose.yaw}


def fused_format(targets_dict, robot_position):

    return {"targets": targets_dict,
            "robot_position": robot_position}


def data_format():

    return {}
