# seasons
CRESCENDO = 2024
REEFSCAPE = 2025

# other constants
UNKNOWN = 'unknown'
TAB = 4
PURPLE = (255, 110, 200)

# networking
DASHBOARD_PORT = 5800

# metrics
QUEUE_SIZE = 15
TAG_HALF_SIZE = 0.5 * ((6.5 * 2.54) / 100)
UPDATE_INTERVAL = 0.015

# default values
DEFAULT_CALIBRATION = {
                        "columns": -1,
                        "imageSize": {
                            "height": 480,
                            "width": 640
                        },
                        "rows": -1,
                        "sideLength": -1
                    }

DEFAULT_CAMERA = {
                    "settings": {
                        "fps": 60,
                        "name": "Default Camera",
                        "pitch": 0,
                        "roll": 0,
                        "x": 0,
                        "y": 0,
                        "yaw": 0,
                        "z": 0
                    },
                    "lighting": {},
                    "calibration": DEFAULT_CALIBRATION,
                    "matrix": [],
                    "distortion": []
                }

