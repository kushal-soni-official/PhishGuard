const socket = io();

// Chart Initialization
const ctx = document.getElementById('threatChart').getContext('2d');
const threatChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Safe', 'Phishing'],
        datasets: [{
            data: [0, 0],
            backgroundColor: ['#03dac6', '#cf6679'],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'right', labels: { color: '#e0e0e0' } }
        }
    }
});

// Real-time Updates via WebSockets
socket.on('stats_update', function(stats) {
    document.getElementById('stat-total').innerText = stats.total_scanned;
    document.getElementById('stat-phishing').innerText = stats.phishing_detected;
    document.getElementById('stat-safe').innerText = stats.safe_detected;
    
    threatChart.data.datasets[0].data = [stats.safe_detected, stats.phishing_detected];
    threatChart.update();
});

socket.on('new_alert', function(alert) {
    const tbody = document.querySelector('#alerts-table tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${alert.timestamp}</td>
        <td>${alert.sender || 'Unknown'}</td>
        <td>${alert.subject || 'No Subject'}</td>
        <td><span class="badge ${alert.severity}">${alert.severity}</span></td>
        <td>${alert.risk_score}%</td>
    `;
    tbody.insertBefore(tr, tbody.firstChild);
    
    // Keep max 100 rows
    if (tbody.children.length > 100) {
        tbody.removeChild(tbody.lastChild);
    }
});

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(el => el.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';
    
    document.querySelectorAll('.nav li').forEach(el => el.classList.remove('active'));
    event.currentTarget.parentElement.classList.add('active');
}

async function scanEmail() {
    const content = document.getElementById('raw-email-input').value;
    const btn = document.getElementById('scan-btn');
    const resultDiv = document.getElementById('scan-result');
    
    if (!content.trim()) return alert("Please enter email content.");
    
    btn.disabled = true;
    btn.innerText = "Analyzing...";
    
    try {
        const response = await fetch('/api/scan-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_email: content })
        });
        
        const data = await response.json();
        
        document.getElementById('res-class').innerText = data.classification;
        document.getElementById('res-score').innerText = data.risk_score;
        document.getElementById('res-severity').innerText = data.severity;
        
        resultDiv.style.borderLeftColor = data.classification === 'Phishing' ? '#cf6679' : '#03dac6';
        resultDiv.style.display = 'block';
    } catch (e) {
        console.error(e);
        alert("Error analyzing email");
    } finally {
        btn.disabled = false;
        btn.innerText = "Analyze Email";
    }
}

// Initial fetch
fetch('/api/stats').then(r => r.json()).then(stats => {
    document.getElementById('stat-total').innerText = stats.total_scanned;
    document.getElementById('stat-phishing').innerText = stats.phishing_detected;
    document.getElementById('stat-safe').innerText = stats.safe_detected;
    threatChart.data.datasets[0].data = [stats.safe_detected, stats.phishing_detected];
    threatChart.update();
});

fetch('/api/alerts').then(r => r.json()).then(alerts => {
    alerts.reverse().forEach(alert => {
        const tbody = document.querySelector('#alerts-table tbody');
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${alert.timestamp}</td>
            <td>${alert.sender || 'Unknown'}</td>
            <td>${alert.subject || 'No Subject'}</td>
            <td><span class="badge ${alert.severity}">${alert.severity}</span></td>
            <td>${alert.risk_score}%</td>
        `;
        tbody.insertBefore(tr, tbody.firstChild);
    });
});
