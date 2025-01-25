from capture.camera import Camera, Pose3D
from utils import constants
from typing import List
import math

def data_format(cameras: List[Camera], targets_dict, robot_position):

    targets_dict["april_tags"] = cameras[0].detected_apriltags # patch - fix later

    return {"cameras": [camera_format(camera) for camera in cameras],
            "fused_data": fused_format(targets_dict, robot_position)}


def camera_format(camera: Camera):

    return {"camera_id": camera.id,
            "targets": {"april_tags": apriltags_format(camera.detected_apriltags)},
            "camera_position": pose3d_format(camera.field_pose, degrees=True)}


def fused_format(targets_dict, robot_position):

    return {"targets": {"april_tags": apriltags_format(targets_dict["april_tags"])},
            "robot_position": pose3d_format(robot_position)}


def pose3d_format(pose: Pose3D, degrees=False):

    try:

        if degrees:
            roll = math.degrees(pose.roll)
            pitch = math.degrees(pose.pitch)
            yaw = math.degrees(pose.yaw)
        else:
            roll = pose.roll
            pitch = pose.pitch
            yaw = pose.yaw
        
        return {"x": pose.x,
                "y": pose.y,
                "z": pose.z,
                "roll": roll,
                "pitch": pitch,
                "yaw": yaw}
    except:

        return constants.UNKNOWN
    

def apriltags_format(apriltag_ids: list):
    return [{"id": tag_id, "distance": 0} 
             for tag_id in apriltag_ids]
