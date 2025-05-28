import threading

CURRENT_MODE = {
    "mode": "detection",   # default
    "camera_id": -1
}
MODE_LOCK = threading.Lock()