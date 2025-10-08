# pylint: disable=C0114
from flask import Flask, jsonify, request # pylint: disable=C0114

app = Flask(__name__)

@app.route("/health", methods=["GET", "POST"])
def health(): # pylint: disable=C0116
    return jsonify({
        'status': "ok"
    }), 200

BASE_API = "/api/v1/"

@app.route(f"{BASE_API}create_table", methods=["POST"])
def create_table(): # pylint: disable=C0116
    data = request.json

    if not data.get("table_name"):
        return jsonify(
            {
                'status': "FAILED",
                'message': "You have to pass table_name when creating a table"
            }
        ), 400

    return jsonify({
        'status': "OK"
    }), 200
