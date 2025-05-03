from flask import Blueprint, jsonify
from app.models.mininet_info import get_fixed_net_info

netinfor_bp = Blueprint("netinfor", __name__)

@netinfor_bp.route('/fetch_netinfor', methods = ['GET'])
def fetch_network_info():
    return jsonify(get_fixed_net_info())