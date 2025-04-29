import os
import sys
from pathlib import Path

# Get the absolute path to the src directory
src_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(src_dir))

try:
    from detection.apriltag_detector import AprilTagDetector
    from capture.camera import Camera, Pose3D
    from utils import constants
except ImportError as e:
    print(f"Import error: {e}")
    print("Current Python path:")
    for path in sys.path:
        print(f"  {path}")
    print("\nProject structure:")
    print(f"Source directory: {src_dir}")
    if src_dir.exists():
        for root, dirs, files in os.walk(src_dir):
            level = root.replace(str(src_dir), '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f.endswith('.py'):
                    print(f"{subindent}{f}")
    sys.exit(1)

import cv2

def test_static_image(image_path: str):
    camera = Camera(id=0)
    season = constants.REEFSCAPE

    apriltag_detector = AprilTagDetector(camera=camera, families='tag36h11', season=season)
    
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Image could not be loaded from {image_path}")
        return
    
    print("Image shape:", frame.shape)
    print("Image dtype:", frame.dtype)
    
    robot_pose = apriltag_detector.get_camera_and_tags_data(frame=frame)
    if isinstance(robot_pose, Pose3D):
        print("Robot Pose:", robot_pose.to_string())
    else:
        print("Not Pose3D!")

if __name__ == '__main__':
    # Use a path relative to the src directory
    image_path = src_dir / "test_image_0.jpg"
    if not image_path.exists():
        print(f"Error: Image not found at {image_path.resolve()}")
    else:
        test_static_image(str(image_path)) 