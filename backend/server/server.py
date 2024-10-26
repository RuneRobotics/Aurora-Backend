from flask import Flask, jsonify
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/data', methods=['GET'])
def get_data():
    # Replace 'data.json' with the path to your JSON file

    with open(os.path.join(os.path.dirname(__file__), '..', 'output', 'output.json')) as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
