from flask import Flask
from .config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for all routes
    
    from .controllers.network_monitor import network_bp
    from .controllers.alerts import alert_bp
    from .controllers.rules import rules_bp
    from .controllers.netinfo_controller import netinfor_bp
    
    app.register_blueprint(network_bp, url_prefix='/api/network')
    app.register_blueprint(alert_bp, url_prefix='/api/alerts')
    app.register_blueprint(rules_bp, url_prefix='/api/rules')
    app.register_blueprint(netinfor_bp, url_prefix='/api/netinfo')
    
    return app