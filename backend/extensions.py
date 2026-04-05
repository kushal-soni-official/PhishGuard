from flask_socketio import SocketIO
from backend.models.phishing_detector import PhishingDetector

socketio = SocketIO(cors_allowed_origins="*")
detector = PhishingDetector()

alerts = []
stats = {
    "total_scanned": 0,
    "phishing_detected": 0,
    "safe_detected": 0
}
