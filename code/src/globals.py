import threading
from utils import constants

CURRENT_MODE = {
    "mode": "Detection",   # default
    "camera_id": -1
}
MODE_LOCK = threading.Lock()

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

NEW_SETTINGS_SAVED = False

SETTINGS_LOCK = threading.Lock()

SEASON = constants.REEFSCAPE