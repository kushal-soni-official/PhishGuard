chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scan_email") {
    
    // Retrieve API URL from storage or default to localhost
    chrome.storage.sync.get({apiUrl: 'http://localhost:5000'}, function(items) {
      const endpoint = items.apiUrl.replace(/\/$/, '') + '/api/scan-email';
      
      fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ raw_email: request.raw_email })
      })
      .then(response => response.json())
      .then(data => sendResponse({ success: true, data: data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    });

    return true; // Indicates asynchronous response
  }
});
