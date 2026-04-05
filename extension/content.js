// CSS for injected elements can be handled in content.css or inline
function extractEmailContent() {
    // Gmail DOM is highly dynamic. Best-effort extraction.
    // Sender
    let senderEl = document.querySelector('span.gD');
    let sender = senderEl ? senderEl.getAttribute('email') : '';
    
    // Subject
    let subjectEl = document.querySelector('h2.hP');
    let subject = subjectEl ? subjectEl.innerText : '';
    
    // Body (visible message body)
    let bodyEl = document.querySelector('div.a3s.aiL');
    let bodyText = bodyEl ? bodyEl.innerText : '';
    
    return `From: ${sender}\nSubject: ${subject}\n\n${bodyText}`;
}

function createScanButton() {
    let btn = document.createElement('button');
    btn.className = 'phishguard-scan-btn';
    btn.innerHTML = `<img src="${chrome.runtime.getURL('icons/icon16.png')}" style="vertical-align:middle;margin-right:5px;width:16px;"> Scan with PhishGuard`;
    
    btn.onclick = (e) => {
        e.stopPropagation();
        btn.innerText = "Scanning...";
        btn.disabled = true;
        
        let content = extractEmailContent();
        
        chrome.runtime.sendMessage({ action: "scan_email", raw_email: content }, response => {
            btn.innerText = "Scan Again";
            btn.disabled = false;
            
            if (response.success && response.data) {
                showResultBadge(btn, response.data);
            } else {
                alert("PhishGuard Analysis Failed: " + (response.error || 'Unknown error'));
            }
        });
    };
    return btn;
}

function showResultBadge(anchorBtn, data) {
    // Remove old badge
    let oldBadge = document.getElementById('phishguard-result-badge');
    if (oldBadge) oldBadge.remove();
    
    let badge = document.createElement('span');
    badge.id = 'phishguard-result-badge';
    badge.className = `phishguard-badge phishguard-${data.severity}`;
    badge.innerText = `${data.classification} (Score: ${data.risk_score}%)`;
    
    anchorBtn.parentNode.insertBefore(badge, anchorBtn.nextSibling);
}

// Observing DOM to inject button when reading an email
const observer = new MutationObserver((mutations) => {
    // Look for the header toolbar to place the button
    let toolbar = document.querySelector('.iH > div');
    if (toolbar && !document.querySelector('.phishguard-scan-btn')) {
        toolbar.appendChild(createScanButton());
    }
});

observer.observe(document.body, { childList: true, subtree: true });
