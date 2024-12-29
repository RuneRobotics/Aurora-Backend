from capture.camera import Camera, Pose3D
from utils import constants

def data_format(cameras: list, targets_dict, robot_position):

    return {"cameras": [camera_format(camera) for camera in cameras],
            "fused_data": fused_format(targets_dict, robot_position)}


def camera_format(camera: Camera):

    return {"camera_id": camera.id,
            "targets": {"april_tags": camera.deteceted_apriltags},
            "camera_position": pose3d_format(camera.field_position)}


def fused_format(targets_dict, robot_position):

    return {"targets": {"april_tags": []},
            "robot_position": pose3d_format(robot_position)}


def pose3d_format(pose: Pose3D):

    try:
        
        return {"x": pose.x,
                "y": pose.y,
                "z": pose.z,
                "roll": pose.roll,
                "pitch": pose.pitch,
                "yaw": pose.yaw}
    except:

        return constants.UNKOWN
