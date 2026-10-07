async function renderLogs() {
    const response = await fetch('/api/logs');
    const logs = await response.json();
    const tbody = document.getElementById('logsTable');
    tbody.innerHTML = '';

    logs.forEach((log) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${log.id || '-'}</td>
            <td>${log.source_ip || '-'}</td>
            <td>${log.destination_ip || '-'}</td>
            <td>${log.protocol || '-'}</td>
            <td>${log.packet_count || 0}</td>
            <td>${log.packet_size || 0}</td>
            <td>${log.connection_rate || 0}</td>
            <td>${log.attack_type || '-'}</td>
            <td><span class="risk-pill ${log.risk && log.risk.toLowerCase() === 'high' ? 'high' : 'low'}">${log.risk || 'LOW'}</span></td>
            <td><span class="status-pill ${log.status && log.status.toLowerCase() === 'detected' ? 'detected' : 'safe'}">${log.status || 'Safe'}</span></td>
            <td>${log.timestamp || '-'}</td>
        `;
        tbody.appendChild(tr);
    });
}

renderLogs();
setInterval(renderLogs, 4000);
