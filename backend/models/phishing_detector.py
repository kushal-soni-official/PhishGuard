import os
import joblib
import numpy as np
from typing import Dict, Any

from phishguard.backend.models.feature_extractor import extract_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'rf_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'tfidf_vectorizer.pkl')

class PhishingDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            print("Model and vectorizer loaded successfully.")
        else:
            print("Warning: Model files not found. Detector will only use rule-based triage until trained.")
            
    def predict(self, raw_email: str | bytes) -> Dict[str, Any]:
        """
        Runs the email through feature extraction and prediction.
        """
        features_dict = extract_features(raw_email)
        
        # Rule-based triage (fast path)
        triage_score = 0.0
        if features_dict['num_suspicious_attachments'] > 0:
            triage_score += 0.4
        if features_dict['num_ip_urls'] > 0:
            triage_score += 0.3
        if features_dict['auth_missing'] == 1:
            triage_score += 0.2
            
        risk_score = min(triage_score, 1.0) * 100
        classification = "Phishing" if risk_score > 60 else "Safe"
        confidence = risk_score
        
        # Deep ML Analysis if models are loaded
        if self.model and self.vectorizer:
            # Prepare numeric features
            numeric_features = [
                features_dict['num_urls'],
                features_dict['num_suspicious_urls'],
                features_dict['num_ip_urls'],
                features_dict['num_shortened_urls'],
                features_dict['auth_missing'],
                features_dict['auth_score'],
                features_dict['num_attachments'],
                features_dict['num_suspicious_attachments']
            ]
            
            # Prepare text features
            text_features = self.vectorizer.transform([features_dict['clean_text']]).toarray()
            
            # Combine
            X = np.hstack((np.array([numeric_features]), text_features))
            
            # Predict
            prob = self.model.predict_proba(X)[0]
            # Assumes class 1 is Phishing
            phishing_prob = prob[1] * 100
            
            # Hybrid approach: max of triage or ML probability
            final_risk = max(risk_score, phishing_prob)
            
            classification = "Phishing" if final_risk > 50 else "Safe"
            confidence = final_risk
            
        else:
            final_risk = risk_score
            
        # Determine Severity
        if final_risk >= 75:
            severity = "High"
        elif final_risk >= 50:
            severity = "Medium"
        else:
            severity = "Low"
            
        return {
            "classification": classification,
            "risk_score": round(final_risk, 2),
            "severity": severity,
            "sender": features_dict['meta_sender'],
            "subject": features_dict['meta_subject'],
            "indicators": {
                "suspicious_attachments": features_dict['num_suspicious_attachments'],
                "suspicious_urls": features_dict['num_suspicious_urls'],
                "auth_missing": bool(features_dict['auth_missing'])
            }
        }
