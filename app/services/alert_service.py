import redis
import json
import time


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
                    yield f"data: {json.dumps(alert_data)}\n\n"
            except json.JSONDecodeError:
                print("Invalid JSON received from Redis.")
        else:
            time.sleep(1)
