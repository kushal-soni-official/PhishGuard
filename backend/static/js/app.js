document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation Logic
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('data-target');
            
            // UI Switch
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(sec => sec.classList.remove('active'));

            item.classList.add('active');
            document.getElementById(targetId).classList.add('active');
            
            // Trigger chart resize on dashboard activation
            if (targetId === 'dashboard-section' && threatChart) {
                threatChart.resize();
            }
        });
    });

    // 2. Chart.js Initialization
    const ctx = document.getElementById('threatTrendChart').getContext('2d');
    let threatChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(12).fill('').map((_, i) => `${i*2}h`),
            datasets: [{
                label: 'Threat Intensity',
                data: [12, 19, 3, 5, 2, 3, 10, 15, 8, 12, 20, 5],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { display: false },
                x: { grid: { display: false }, ticks: { color: '#64748b' } }
            }
        }
    });

    // 3. Data Synchronization
    const statsElements = {
        scanned: document.getElementById('stat-scanned'),
        phishing: document.getElementById('stat-phishing'),
        safe: document.getElementById('stat-safe')
    };
    const historyTableBody = document.getElementById('history-table-body');
    const miniAlertList = document.getElementById('mini-alert-list');

    async function syncData() {
        try {
            // Fetch Stats
            const statsRes = await fetch('/api/stats');
            const stats = await statsRes.json();
            
            // Simple counter animation
            animateValue(statsElements.scanned, stats.total_scanned);
            animateValue(statsElements.phishing, stats.phishing_detected);
            animateValue(statsElements.safe, stats.safe_detected);

            // Fetch History
            const alertsRes = await fetch('/api/alerts');
            const alerts = await alertsRes.json();
            renderHistory(alerts);
            renderMiniAlerts(alerts);
        } catch (e) {
            console.error('Sync failed:', e);
        }
    }

    function animateValue(obj, end) {
        let start = parseInt(obj.innerText) || 0;
        let duration = 800;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function renderHistory(alerts) {
        if (!alerts || alerts.length === 0) return;
        
        historyTableBody.innerHTML = '';
        alerts.forEach(alert => {
            const tr = document.createElement('tr');
            const isPhish = alert.classification === 'Phishing';
            tr.innerHTML = `
                <td class="text-muted">${alert.timestamp}</td>
                <td>${alert.sender || 'Unknown'}</td>
                <td><span class="badge ${isPhish ? 'phishing' : 'safe'}">${alert.classification}</span></td>
                <td><strong class="${isPhish ? 'critical-glow' : 'safe-glow'}">${alert.risk_score}%</strong></td>
                <td><button class="view-btn"><i class="fa-solid fa-eye"></i></button></td>
            `;
            historyTableBody.appendChild(tr);
        });
    }

    function renderMiniAlerts(alerts) {
        const criticals = alerts.filter(a => a.classification === 'Phishing').slice(0, 3);
        if (criticals.length === 0) {
            miniAlertList.innerHTML = '<p class="empty-msg">No critical threats detected.</p>';
            return;
        }

        miniAlertList.innerHTML = criticals.map(a => `
            <div class="mini-alert-item">
                <div class="mini-alert-header">
                    <span class="badge phishing">CRITICAL</span>
                    <span class="time">${a.timestamp.split(' ')[1]}</span>
                </div>
                <p>${a.subject || 'Suspicious Activity Detected'}</p>
            </div>
        `).join('');
    }

    // 4. Scan Implementation
    const scanBtn = document.getElementById('scan-btn');
    const emailInput = document.getElementById('raw-email-input');
    const resultContainer = document.getElementById('scan-result-container');

    scanBtn.addEventListener('click', async () => {
        const content = emailInput.value.trim();
        if (!content) return;

        // UI State
        scanBtn.disabled = true;
        scanBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> ANALYZING SEQUENCE...';
        resultContainer.innerHTML = `
            <div class="placeholder-content">
                <div class="scanner-loader"></div>
                <p>Decoding Heuristics...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/scan-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ raw_email: content })
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.error);

            displayResult(result);
            syncData(); // Update dashboard after scan
            
        } catch (e) {
            resultContainer.innerHTML = `<div class="error-msg"><i class="fa-solid fa-triangle-exclamation"></i> ${e.message}</div>`;
        } finally {
            scanBtn.disabled = false;
            scanBtn.innerHTML = '<i class="fa-solid fa-bolt-lightning"></i> RUN AI DIAGNOSTICS';
        }
    });

    function displayResult(result) {
        const isPhish = result.classification === 'Phishing';
        const colorClass = isPhish ? 'critical-glow' : 'safe-glow';
        const meterClass = isPhish ? 'risk-high' : 'risk-low';
        
        resultContainer.innerHTML = `
            <div class="result-display fade-in">
                <div class="result-header">
                    <div class="result-title">
                        <h3 class="${colorClass}">
                            <i class="fa-solid ${isPhish ? 'fa-ban' : 'fa-shield-check'}"></i> 
                            ${result.classification.toUpperCase()}
                        </h3>
                        <p class="text-muted">Security Severity: ${result.severity}</p>
                    </div>
                    <div class="risk-meter ${meterClass}">
                        ${result.risk_score}%
                    </div>
                </div>

                <div class="indicator-showcase">
                    <h4>Behavioral Artifacts</h4>
                    <div class="artifact-list">
                        ${Object.entries(result.indicators).map(([key, val]) => `
                            <div class="artifact-item">
                                <span>${key.replace(/_/g, ' ').toUpperCase()}</span>
                                <span class="${val ? 'danger-text' : 'safe-text'}">${val === true ? 'DETECTED' : (val === false ? 'CLEAN' : val)}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="result-footer">
                    <p><i class="fa-solid fa-info-circle"></i> Detection based on ${result.classification === 'Phishing' ? 'high-entropy suspicious keywords and pattern mismatch.' : 'verified sender behavior and low-risk text indicators.'}</p>
                </div>
            </div>
        `;
    }

    // Initial Sync and Polling
    syncData();
    setInterval(syncData, 10000); // Sync every 10s
});
