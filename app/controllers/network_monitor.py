from flask import Blueprint, jsonify, request
from app.services.odl_service import get_topology, get_state_port, get_traffic_stats

network_bp = Blueprint('network',__name__)

#tested: http://127.0.0.1:5000/api/network/topology
@network_bp.route('/topology', methods = ['GET'])
def topology():
    return jsonify(get_topology())

#tested: http://127.0.0.1:5000/api/network/topology/port_state?switch_id=openflow:2&port_number=openflow:2:2
@network_bp.route('/topology/port_state', methods=['GET'])
def state_port():
    switch_id = request.args.get('switch_id')
    port_number = request.args.get('port_number')
    if not switch_id or not port_number:
        return jsonify({"error": "Missing switch_id or port_number"}), 400
    return jsonify(get_state_port(switch_id, port_number))

@network_bp.route('/topology/traffic_stastistic', methods = ['GET'])
def traffic_statistic():
    switch_id = request.args.get('switch_id')
    port_number = request.args.get('port_number')
    if not switch_id or not port_number:
        return jsonify({"error": "Missing switch_id or port_number"}), 400
    return jsonify(get_traffic_stats(switch_id, port_number))
