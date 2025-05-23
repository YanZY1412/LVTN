from flask import Blueprint, request, jsonify
from app.services.odl_service import install_block_flow_rule, list_rules, add_forward, arp_flood_service, delete_rule

rules_bp = Blueprint("rules", __name__)

@rules_bp.route("/block", methods=["POST"])
def block_ip_traffic():
    data = request.json
    switch_id = data.get("switch_id")
    src_ip = data.get("src_ip")
    dst_ip = data.get("dst_ip")
    if not switch_id:
        return jsonify({"error": "Missing switch_id"}), 400
    existing_rules = list_rules(switch_id)
    existing_flow_ids = {rule.get("flow_id") for rule in existing_rules}
    result = []
    if src_ip:
        flow_id = f"block-{src_ip.replace('.', '-')}"
        if f"{flow_id}-in" not in existing_flow_ids:
            result.extend(install_block_flow_rule(switch_id, src_ip, f"block-{src_ip.replace('.', '-') }"))
    if dst_ip:
        flow_id = f"block-{dst_ip.replace('.', '-')}"
        if f"{flow_id}-in" not in existing_flow_ids:
            result.extend(install_block_flow_rule(switch_id, dst_ip, f"block-{dst_ip.replace('.', '-') }"))
    return jsonify(result)

@rules_bp.route("/list_node_rules", methods=["GET"])
def list_node_rules():
    switch_id = request.args.get("switch_id")
    if not switch_id:
        return jsonify({"error": "Missing switch_id"}), 400
    return jsonify(list_rules(switch_id))

@rules_bp.route("/add_forwarding_rule", methods=["POST"])
def add_forwarding_rule():
    data = request.json
    switch_id = data.get("switch_id")
    dst_ip = data.get("dst_ip")
    fw_port = data.get("fw_port")
    result = []
    if not switch_id or not dst_ip or not fw_port:
        return jsonify({"error": "Missing switch_id or dst_ip or fw_port"}), 400
    result.extend(add_forward(switch_id, dst_ip, f"add-forward-{dst_ip.replace('.', '-') }", fw_port))
    return jsonify(result)

@rules_bp.route("/arp_flood", methods=["POST"])
def arp_flood():
    data = request.json
    switch_id = data.get("switch_id")
    if not switch_id:
        return jsonify({"error": "Missing switch_id"}), 400
    return jsonify(arp_flood_service(switch_id, "arp"))

@rules_bp.route("/delete_rule", methods=["DELETE"])
def delete_flow_rule():
    switch_id = request.args.get("switch_id")
    flow_id = request.args.get("flow_id")
    if not switch_id or not flow_id:
        return jsonify({"error": "Missing switch_id or flow_id"}), 400
    return jsonify(delete_rule(switch_id, flow_id))