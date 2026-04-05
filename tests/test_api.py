import pytest
from backend.app import create_app
from backend.extensions import alerts, stats

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'PhishGuard' in rv.data

def test_scan_email_api(client):
    # Initial stats
    initial_scanned = stats['total_scanned']
    
    # Send a dummy email
    payload = {
        "raw_email": "To: victim@example.com\nFrom: badguy@evil.com\nSubject: URGENT\n\nClick here."
    }
    rv = client.post('/api/scan-email', json=payload)
    
    assert rv.status_code == 200
    data = rv.get_json()
    assert "classification" in data
    assert "risk_score" in data
    assert data["classification"] in ["Safe", "Phishing"]
    
    # Stats should have updated
    assert stats['total_scanned'] == initial_scanned + 1

def test_alerts_api(client):
    rv = client.get('/api/alerts')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
