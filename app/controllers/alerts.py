from flask import Blueprint, jsonify, request, Response
from app.services.alert_service import get_alerts

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/get_all_alert', methods = ['GET'])
def all_alert():
    def event_stream():
        for alert in get_alerts():
            yield alert
    return Response(event_stream(), content_type='text/event-stream')