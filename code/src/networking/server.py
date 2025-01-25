from flask import Flask, send_from_directory, jsonify
from pathlib import Path
import json


DASHBOARD_PORT = 5800

def json_to_dict(path: Path) -> dict:

    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data


app = Flask(__name__, static_folder="dist", static_url_path="")

# Serve React static files
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

# Serve the React app for all frontend routes
@app.errorhandler(404)
def not_found(e):
        return send_from_directory(app.static_folder, "index.html")


# Example API route
@app.route("/api/data", methods=["GET"])
def get_data():
    output_file_path = Path(__file__).parent / Path("../../output/output.json")
    return jsonify(json_to_dict(output_file_path))
    
if __name__ == "__main__":
    app.run(debug=False, port=DASHBOARD_PORT)