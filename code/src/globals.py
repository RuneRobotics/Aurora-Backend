import threading
from utils import constants

MODE_LOCK = threading.Lock()
CURRENT_MODE = {
    "mode": "Detection",   # default
    "camera_id": -1
}

SETTINGS_LOCK = threading.Lock()

CALIBRATION_SETTINGS = constants.DEFAULT_CALIBRATION

CAMERA_SETTINGS = {
    "fps": 60,
    "name": "Default",
    "pitch": 0,
    "roll": 0,
    "x": 0,
    "y": 0,
    "yaw": 0,
    "z": 0
}

SETTINGS_CHANGED = False

SEASON = constants.REEFSCAPE