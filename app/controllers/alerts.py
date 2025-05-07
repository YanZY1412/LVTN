from flask import Blueprint, Response
import json
import requests
import re
import csv
from datetime import datetime, timezone, timedelta
import time
from app.services.alert_service import get_alerts

alert_bp = Blueprint('alert', __name__)

def log_response_time(t0, t2, src_ip, dst_ip="", signature=""):
    dt_obj = datetime.strptime(t0, "%Y-%m-%dT%H:%M:%S.%f%z")
    t0 = dt_obj.timestamp()
    duration = t2 - t0
    vn_tz = timezone(timedelta(hours=7))
    with open("reaction_times.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.fromtimestamp(t0, tz=vn_tz).isoformat(),
            datetime.fromtimestamp(t2, tz=vn_tz).isoformat(),
            f"{duration:.6f}",
            src_ip,
            dst_ip,
            signature
        ])
    print(f"Reaction Time: {duration:.6f} seconds for {src_ip} -> {dst_ip or 'N/A'}")
    

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
                            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:\+\d{4})?) Network Trojan alert detected', message)                        
                            t0 = timestamp_match.group(1)  
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
                                t2 = time.time()
                                print(f"[+] Block API response: {resp.status_code} {resp.text}")
                                if resp.text.strip() and resp.text.strip() != "[]":
                                    log_response_time(t0, t2, src_ip, dest_ip, "Network Trojan")
                            except Exception as e:
                                print(f"[!] Error calling block API: {e}")
                        elif "ET SCAN" in message:
                            ip_match = re.search(r'ET SCAN alert detected. Blocking rule installing for ([\d\.]+)', message)
                            if ip_match:
                                src_ip = ip_match.group(1)
                                timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:\+\d{4})?) ET SCAN alert detected', message)                        
                                t0 = timestamp_match.group(1) 
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
                                    t2 = time.time()
                                    print(f"[+] Block API response: {resp.status_code} {resp.text}")
                                    if resp.text.strip() and resp.text.strip() != "[]":
                                        log_response_time(t0, t2, src_ip, "", "ET SCAN")
                                except Exception as e:
                                    print(f"[!] Error calling block API: {e}")
                        elif "ET DOS" in message:
                            ip_match = re.search(r'ET DOS alert detected. Blocking rule installing for ([\d\.]+)', message)
                            if ip_match:
                                src_ip = ip_match.group(1)
                                timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:\+\d{4})?) ET DOS alert detected', message)                        
                                t0 = timestamp_match.group(1)
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
                                    t2 = time.time()
                                    print(f"[+] Block API response: {resp.status_code} {resp.text}")
                                    if resp.text.strip() and resp.text.strip() != "[]":
                                        log_response_time(t0, t2, src_ip, "", "ET DOS")
                                except Exception as e:
                                    print(f"[!] Error calling block API: {e}")
                    except json.JSONDecodeError:
                        print("Error decoding notify message.")
            yield alert

    return Response(event_stream(), content_type='text/event-stream')