from flask import Blueprint, Response
import json
import requests
import re
from app.services.alert_service import get_alerts
from app.services.odl_service import install_block_flow_rule

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/get_all_alert', methods = ['GET'])
def all_alert():
    def event_stream():
        for alert in get_alerts():
            if 'event: notify' in alert:
                match = re.search(r'data: (.+)\n\n', alert)
                if match:
                    try:
                        data_json = json.loads(match.group(1))
                        message = data_json.get("message", "")
                        ip_match = re.search(r'Network Trojan alert detected. Blocking rule installing for ([\d\.]+) -> ([\d\.]+)', message)
                        if ip_match:
                            src_ip = ip_match.group(1)
                            dest_ip = ip_match.group(2)
                            print(f"Calling block API for {src_ip} -> {dest_ip}")

                            payload = {
                                "switch_id": "openflow:2",
                                "src_ip": src_ip,
                                "dst_ip": dest_ip
                            }
                            try:
                                resp = requests.post(
                                    "http://localhost:5000/api/rules/block",
                                    json=payload
                                )
                                print(f"[+] Block API response: {resp.status_code} {resp.text}")
                            except Exception as e:
                                print(f"[!] Error calling block API: {e}")
                        elif "ET SCAN" in message:
                            ip_match = re.search(r'ET SCAN alert detected. Blocking rule installing for ([\d\.]+)', message)
                            if ip_match:
                                src_ip = ip_match.group(1)
                                print(f"Calling block API for {src_ip}")

                                payload = {
                                    "switch_id": "openflow:2",
                                    "src_ip": src_ip
                                }
                                try:
                                    resp = requests.post(
                                        "http://localhost:5000/api/rules/block",
                                        json=payload
                                    )
                                    print(f"[+] Block API response: {resp.status_code} {resp.text}")
                                except Exception as e:
                                    print(f"[!] Error calling block API: {e}")
                        elif "ET DOS" in message:
                            ip_match = re.search(r'ET DOS alert detected. Blocking rule installing for ([\d\.]+)', message)
                            if ip_match:
                                src_ip = ip_match.group(1)
                                print(f"Calling block API for {src_ip}")

                                payload = {
                                    "switch_id": "openflow:2",
                                    "src_ip": src_ip
                                }
                                try:
                                    resp = requests.post(
                                        "http://localhost:5000/api/rules/block",
                                        json=payload
                                    )
                                    print(f"[+] Block API response: {resp.status_code} {resp.text}")
                                except Exception as e:
                                    print(f"[!] Error calling block API: {e}")
                    except json.JSONDecodeError:
                        print("Error decoding notify message.")
            yield alert

    return Response(event_stream(), content_type='text/event-stream')