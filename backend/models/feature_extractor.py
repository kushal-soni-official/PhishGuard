from typing import Dict, Any, List
from phishguard.backend.utils import email_parser, url_analyzer, auth_checker, nlp_processor

def extract_features(raw_email: str | bytes) -> Dict[str, Any]:
    """
    Extracts numerical and categorical features from an email for ML.
    """
    parsed = email_parser.parse_raw_email(raw_email)
    
    # 1. URL Features
    urls = url_analyzer.extract_urls(parsed['body'])
    url_stats = url_analyzer.analyze_urls(urls)
    
    # 2. Auth Features
    auth_stats = auth_checker.check_auth_headers(parsed['headers'])
    
    # 3. Text/NLP Features - returning raw preprocessed text for TF-IDF pipeline
    clean_body = nlp_processor.preprocess_text(parsed['body'])
    clean_subject = nlp_processor.preprocess_text(parsed['subject'])
    combined_text = clean_subject + " " + clean_body
    
    # 4. Attachment Features
    num_attachments = len(parsed['attachments'])
    suspicious_exts = ['.exe', '.scr', '.vbs', '.bat', '.cmd', '.js', '.wsf', '.docm', '.xlsm']
    suspicious_attachment_count = 0
    
    for att in parsed['attachments']:
        fname = str(att.get('filename', '')).lower()
        if any(fname.endswith(ext) for ext in suspicious_exts):
            suspicious_attachment_count += 1
            
    # Assemble feature vector dictionary
    features = {
        'num_urls': url_stats['total_urls'],
        'num_suspicious_urls': url_stats['suspicious_urls'],
        'num_ip_urls': url_stats['ip_based_urls'],
        'num_shortened_urls': url_stats['shortened_urls'],
        
        'auth_missing': 1 if auth_stats['auth_missing'] else 0,
        'auth_score': auth_stats['auth_score'],
        
        'num_attachments': num_attachments,
        'num_suspicious_attachments': suspicious_attachment_count,
        
        # We pass the combined text to be victimized by the vectorizer later
        'clean_text': combined_text,
        
        # Meta info for dashboard
        'meta_sender': parsed['sender'],
        'meta_subject': parsed['subject']
    }
    
    return features
