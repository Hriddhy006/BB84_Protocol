from flask import Flask, request, jsonify

app = Flask(__name__)

# Initial network state
network_state = {
    "noise_map": {},  # Stores granular noise for every specific link
    "eves": [],       # List of compromised links
    "bob_results": {"correct": 0, "efficiency": 0.33},
    "active_route": ["London", "Paris", "Berlin", "Vienna"],
    "delivery_status": "WAITING_FOR_ALICE",
    "qubit_buffer": None
}

@app.route('/update_evil', methods=['POST'])
def update_evil():
    data = request.json
    network_state["noise_map"] = data.get("noise_map", {})
    network_state["eves"] = data.get("eves", [])
    return jsonify({"status": "synchronized"})

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify(network_state)

@app.route('/update_route', methods=['POST'])
def update_route():
    network_state["active_route"] = request.json.get("route")
    return jsonify({"status": "route_updated"})

@app.route('/send_qubits', methods=['POST'])
def send_qubits():
    network_state["qubit_buffer"] = request.json
    network_state["delivery_status"] = "PENDING_BOB"
    return jsonify({"status": "data_received"})

@app.route('/report_bob', methods=['POST'])
def report_bob():
    network_state["bob_results"] = request.json
    network_state["delivery_status"] = "RECEIVED"
    return jsonify({"status": "report_logged"})

if __name__ == '__main__':
    app.run(port=5000, debug=False)