from utils import constants
from pathlib import Path
import json

def json_to_dict(path: Path) -> dict:

    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data


def dict_to_json(path: Path, data):

    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=constants.TAB)


def load_field(season: int):
    path = Path(__file__).parent / Path(f"../../data/apriltag_data/{season}_field.json")
    return json_to_dict(path)