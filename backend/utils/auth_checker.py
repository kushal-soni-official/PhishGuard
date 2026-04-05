import re
from typing import Dict, Any

def check_auth_headers(headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Checks SPF, DKIM, and DMARC results from email headers.
    """
    # Extract Authentication-Results header
    auth_results = headers.get('Authentication-Results', '').lower()
    
    spf_pass = False
    dkim_pass = False
    dmarc_pass = False
    
    if auth_results:
        # Simple string matching for common pass indicators
        if 'spf=pass' in auth_results:
            spf_pass = True
        if 'dkim=pass' in auth_results:
            dkim_pass = True
        if 'dmarc=pass' in auth_results:
            dmarc_pass = True
            
    # Also check Received-SPF if present
    received_spf = headers.get('Received-SPF', '').lower()
    if 'pass' in received_spf:
        spf_pass = True

    # Consider missing authentication as suspicious
    auth_missing = not (spf_pass or dkim_pass)
    
    return {
        'spf_pass': spf_pass,
        'dkim_pass': dkim_pass,
        'dmarc_pass': dmarc_pass,
        'auth_missing': auth_missing,
        'auth_score': sum([spf_pass, dkim_pass, dmarc_pass]) / 3.0
    }
