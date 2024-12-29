from flask import Flask, send_from_directory, jsonify
from utils import constants

def run_server():

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
        return jsonify({"message": "Hello from Flask!"})
    
    app.run(debug=True, port=constants.DASHBOARD_PORT)