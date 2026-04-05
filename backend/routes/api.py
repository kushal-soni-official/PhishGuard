from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.extensions import socketio, detector, alerts, stats

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

@api_bp.route('/scan-email', methods=['POST'])
def scan_email():
    """
    Accepts raw email content, processes it, and returns a classification.
    """
    data = request.json
    raw_email = data.get('raw_email', '')
    
    if not raw_email:
        return jsonify({"error": "No email content provided"}), 400
        
    try:
        # Run detection
        result = detector.predict(raw_email)
        
        # Update statistics
        stats['total_scanned'] += 1
        if result['classification'] == 'Phishing':
            stats['phishing_detected'] += 1
        else:
            stats['safe_detected'] += 1
            
        # Create alert entry
        alert = {
            "id": len(alerts) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": result['sender'],
            "subject": result['subject'],
            "classification": result['classification'],
            "risk_score": result['risk_score'],
            "severity": result['severity'],
            "indicators": result['indicators']
        }
        
        # Add to global alerts in memory
        alerts.insert(0, alert)
        # Keep only the last 100 alerts for demo
        if len(alerts) > 100:
            alerts.pop()
            
        # Emit WebSocket event for real-time dashboard update
        socketio.emit('new_alert', alert)
        socketio.emit('stats_update', stats)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Returns recent alerts.
    """
    return jsonify(alerts), 200

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Returns aggregated statistics.
    """
    return jsonify(stats), 200
