from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health", methods=["GET", "POST"])
def health():
    return jsonify({
        'status': "ok"
    }), 200

base_api = "/api/v1/"

@app.route(f"{base_api}create_table", methods=["POST"])
def create_table():
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