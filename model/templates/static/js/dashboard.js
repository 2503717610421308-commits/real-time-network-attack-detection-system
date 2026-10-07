async function loadStatus() {
    const response = await fetch('/api/status');
    const data = await response.json();
    document.getElementById('totalLogs').textContent = data.total || 0;
    document.getElementById('attackCount').textContent = data.attacks || 0;
    document.getElementById('safeCount').textContent = data.safe || 0;
    document.getElementById('systemStatus').textContent = data.system || 'ONLINE';
}

async function loadLogs() {
    const response = await fetch('/api/logs');
    const data = await response.json();
    const tbody = document.getElementById('recentLogs');
    tbody.innerHTML = '';

    data.slice(0, 8).forEach((row) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.source_ip || '-'}</td>
            <td>${row.destination_ip || '-'}</td>
            <td>${row.protocol || '-'}</td>
            <td>${row.attack_type || '-'}</td>
            <td><span class="risk-pill ${row.risk && row.risk.toLowerCase() === 'high' ? 'high' : 'low'}">${row.risk || 'LOW'}</span></td>
            <td><span class="status-pill ${row.status && row.status.toLowerCase() === 'detected' ? 'detected' : 'safe'}">${row.status || 'Safe'}</span></td>
            <td>${row.timestamp || '-'}</td>
        `;
        tbody.appendChild(tr);
    });
}

loadStatus();
loadLogs();
setInterval(() => {
    loadStatus();
    loadLogs();
}, 3000);
