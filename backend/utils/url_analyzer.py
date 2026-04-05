import re
import urllib.parse
from typing import List, Dict, Any

URL_REGEX = r'(https?://[^\s]+)'
IP_REGEX = r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}'

# Basic mock blocklist (in a real app, this would be a DB or API query)
MOCK_BLOCKLIST = ['bit.ly', 'tinyurl.com', 'evil-phish.net']

def extract_urls(text: str) -> List[str]:
    """
    Extracts all URLs from the given text.
    """
    return re.findall(URL_REGEX, text)

def analyze_urls(urls: List[str]) -> Dict[str, Any]:
    """
    Analyzes a list of URLs and returns risk indicators.
    """
    suspicious_count = 0
    ip_based_count = 0
    shortened_count = 0
    
    for url in urls:
        # Check for IP-based URLs
        domain = urllib.parse.urlparse(url).netloc
        if re.search(IP_REGEX, domain):
            ip_based_count += 1
            suspicious_count += 1
            
        # Check blocklist/shorteners
        if any(bad_domain in domain for bad_domain in MOCK_BLOCKLIST):
            shortened_count += 1
            suspicious_count += 1
            
    return {
        'total_urls': len(urls),
        'suspicious_urls': suspicious_count,
        'ip_based_urls': ip_based_count,
        'shortened_urls': shortened_count,
        'has_suspicious_urls': suspicious_count > 0
    }
