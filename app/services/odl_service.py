import requests
from flask import current_app
from requests.auth import HTTPBasicAuth
from app.utils.api_utils import FlowRule

def get_topology():
    try: 
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        url = f"{current_app.config['ODL_BASE_URL']}/rests/data/network-topology:network-topology"
        resp = requests.get(url, auth=auth)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching topology: {str(e)}"}

def get_state_port(switch_id, port_number):
    try: 
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/node-connector={port_number}/flow-node-inventory:state"
        resp = requests.get(url, auth=auth)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching port state: {str(e)}"}
    

def get_traffic_stats(switch_id, port_number):
    try: 
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/node-connector={port_number}/opendaylight-port-statistics:flow-capable-node-connector-statistics"
        resp = requests.get(url, auth=auth)
        return resp.json()   
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching traffic state: {str(e)}"}
    
def install_block_flow_rule(switch_id, ip_block, flow_id_prefix):
    try: 
        headers = {"Content-Type": "application/json"}
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        base_url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/flow-node-inventory:table=0/flow="

        rules = [
            FlowRule(
                flow_id = f"{flow_id_prefix}-out",
                table_id = 0,
                priority = 200,
                src_ip = ip_block,
                flow_name = f"block-{flow_id_prefix}-out"
            ),
            FlowRule(
                flow_id = f"{flow_id_prefix}-in",
                table_id = 0,
                priority = 200,
                dst_ip = ip_block,
                flow_name = f"block-{flow_id_prefix}-in"
            )
        ]

        results = []
        for rule in rules:
            url = base_url + rule.flow_id
            body = rule.to_dict()
            resp = requests.put(url, json=body, auth=auth, headers=headers)
            results.append({
                "flow_id": rule.flow_id,
                "status": resp.status_code,
                "response": resp.text
            })
        return results

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while installing block flow rule: {str(e)}"}

def add_forward(switch_id, ip_forward_dst, flow_id, fw_port):
    try: 
        headers = {"Content-Type": "application/json"}
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/flow-node-inventory:table=0/flow={flow_id}"

        rule = FlowRule(
                flow_id = f"{flow_id}",
                table_id = 0,
                priority = 100,
                dst_ip = ip_forward_dst,
                flow_name = f"{flow_id}",
                fw_port= fw_port
            )

        results = []
        body = rule.to_dict()
        resp = requests.put(url, json=body, auth=auth, headers=headers)
        results.append({
            "flow_id": rule.flow_id,
            "status": resp.status_code,
            "response": resp.text
        })
        return results

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while installing block flow rule: {str(e)}"}
    

def list_rules(switch_id):
    auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
    url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/flow-node-inventory:table=0"
    resp = requests.get(url, auth=auth)
    if resp.status_code == 200:
        data = resp.json()
        flows = data.get("flow-node-inventory:table", [])[0].get("flow", [])
        result = []
        for f in flows:
            flow_id = f.get("id")
            priority = f.get("priority")
            output_connector = None
            for instruction in f.get("instructions", {}).get("instruction", []):
                for action in instruction.get("apply-actions", {}).get("action", []):
                    if "output-action" in action:
                        output_connector = action["output-action"].get("output-node-connector")
                        break

            result.append({
                "flow_id": flow_id,
                "priority": priority,
                "output-node-connector": output_connector
            })
        return result
    else:
        return {"error": f"Failed to fetch rules: {resp.status_code} {resp.reason}"}

def delete_rule(switch_id, flow_id):
    try:
        headers = {"Content-Type": "application/json"}
        auth = HTTPBasicAuth(current_app.config['ODL_USERNAME'], current_app.config['ODL_PASSWORD'])
        url = f"{current_app.config['ODL_BASE_URL']}/rests/data/opendaylight-inventory:nodes/node={switch_id}/flow-node-inventory:table=0/flow={flow_id}"
        resp = requests.delete(url, auth=auth, headers=headers)
        if resp.status_code in [200, 204]:
            return {"message": f"Flow {flow_id} deleted successfully from {switch_id}."}
        else:
            return {
                "error": f"Failed to delete flow {flow_id} from {switch_id}. Status code: {resp.status_code}",
                "details": resp.text
            }
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while deleting the rule: {str(e)}"}
