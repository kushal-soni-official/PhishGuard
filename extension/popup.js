document.addEventListener('DOMContentLoaded', () => {
  const apiUrlInput = document.getElementById('apiUrl');
  const saveBtn = document.getElementById('saveBtn');
  const statusDiv = document.getElementById('status');

  // Load saved setting
  chrome.storage.sync.get({ apiUrl: 'http://localhost:5000' }, (items) => {
    apiUrlInput.value = items.apiUrl;
  });

  saveBtn.addEventListener('click', () => {
    const apiUrl = apiUrlInput.value;
    chrome.storage.sync.set({ apiUrl: apiUrl }, () => {
      statusDiv.textContent = 'Settings saved.';
      setTimeout(() => statusDiv.textContent = '', 2000);
    });
  });
});
