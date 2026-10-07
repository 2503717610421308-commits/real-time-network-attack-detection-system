async function renderMonitoring() {
    const response = await fetch('/api/logs');
    const logs = await response.json();
    const feed = document.getElementById('monitoringFeed');
    feed.innerHTML = '';

    logs.slice(0, 10).forEach((log) => {
        const item = document.createElement('div');
        item.className = 'feed-item';
        item.innerHTML = `
            <strong>${log.attack_type || 'Normal Traffic'} • ${log.status || 'Safe'}</strong>
            <div>Source: ${log.source_ip || '-'} → ${log.destination_ip || '-'}</div>
            <div>Protocol: ${log.protocol || '-'} • Packets: ${log.packet_count || 0}</div>
            <div>Risk: ${log.risk || 'LOW'} • Timestamp: ${log.timestamp || '-'}</div>
        `;
        feed.appendChild(item);
    });
}

renderMonitoring();
setInterval(renderMonitoring, 4000);
