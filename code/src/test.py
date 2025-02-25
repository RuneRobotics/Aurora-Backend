from detection.apriltag_detector import AprilTagDetector
from capture.camera import Camera
from utils import constants
import cv2
from pathlib import Path
import cv2



def test_robot_pose(frame):

    camera = Camera(id=0)
    season = constants.REEFSCAPE

    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)
    robot_pose = apriltag_detector.get_camera_and_tags_data(frame=frame)

    return robot_pose

image_path = Path("code/src/test_image_0.jpg")

if not image_path.exists():
    print(f"Error: Image not found at {image_path.resolve()}")
else:
    frame = cv2.imread(str(image_path))
    if frame is None:
        print("Error: Image could not be loaded")
    else:
        pose = test_robot_pose(frame)
        print(f"x: {pose.x}, y: {pose.y}, z: {pose.z}, roll: {pose.roll}, pitch: {pose.pitch}, yaw: {pose.yaw}")
