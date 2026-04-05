from phishguard.backend.models.feature_extractor import extract_features
from phishguard.backend.models.phishing_detector import PhishingDetector

def test_feature_extractor():
    raw_email = """Return-Path: <scam@bad.com>
Authentication-Results: spf=fail (sender IP is 192.168.1.1)
From: Scam <scam@bad.com>
To: Victim <victim@example.com>
Subject: URGENT

Click http://192.168.1.1/login"""

    features = extract_features(raw_email)
    assert features['num_urls'] == 1
    assert features['num_ip_urls'] == 1
    assert features['auth_missing'] == 1
    assert 'urgent' in features['clean_text']

def test_phishing_detector_fallback():
    # Will use fallback rule-based triage if models aren't present
    detector = PhishingDetector()
    raw_email = """From: Scam <scam@bad.com>
To: Victim <victim@example.com>
Subject: Update Account
Authentication-Results: dkim=fail

Verify here: http://bit.ly/123"""

    res = detector.predict(raw_email)
    assert "risk_score" in res
    assert "classification" in res
    assert res['indicators']['auth_missing'] == True
    assert res['indicators']['suspicious_urls'] >= 0
