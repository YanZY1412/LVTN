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
                    severity = alert_data.get("alert", {}).get("severity", 5)
                    src_ip = alert_data.get("src_ip")
                    dest_ip = alert_data.get("dest_ip")
                    if severity == 1 and src_ip and dest_ip:
                        print(f"[+] High severity alert detected (Severity {severity}). Installing block rule for {src_ip} -> {dest_ip}")              
                        yield f'event: notify\ndata: {{"message": "Blocking rule installing for {src_ip} -> {dest_ip}"}}\n\n'
                    yield f"data: {json.dumps(alert_data)}\n\n"
            except json.JSONDecodeError:
                print("Invalid JSON received from Redis.")
        else:
            time.sleep(1)
