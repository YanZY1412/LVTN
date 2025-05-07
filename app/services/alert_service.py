import redis
import json
import time
from .odl_service import install_block_flow_rule


def get_alerts():
    r = redis.Redis(host='192.168.1.53', port=6379, db=0)

    if not r.ping():
        yield 'event: error\ndata: {"message": "Cannot connect to Redis"}\n\n'
        return

    while True:
        alert = r.lpop('suricata')
        if alert:
            try:
                alert_data = json.loads(alert)
                if alert_data.get("event_type") == "alert": 
                    category = alert_data.get("alert", {}).get("category", "Unknown")
                    signature = alert_data.get("alert", {}).get("signature", "Unknown")
                    src_ip = alert_data.get("src_ip")
                    dest_ip = alert_data.get("dest_ip")
                    if "A Network Trojan" in category and src_ip and dest_ip:
                        yield f'event: notify\ndata: {{"message": "Network Trojan alert detected. Blocking rule installing for {src_ip} -> {dest_ip}"}}\n\n'
                    elif "ET SCAN" in signature and src_ip and dest_ip:
                        yield f'event: notify\ndata: {{"message": "ET SCAN alert detected. Blocking rule installing for {src_ip}"}}\n\n'
                    elif "ET DOS" in signature and src_ip and dest_ip:
                        yield f'event: notify\ndata: {{"message": "ET DOS alert detected. Blocking rule installing for {src_ip}"}}\n\n'
                    yield f"data: {json.dumps(alert_data)}\n\n"
            except json.JSONDecodeError:
                print("Invalid JSON received from Redis.")
        else:
            time.sleep(1)
