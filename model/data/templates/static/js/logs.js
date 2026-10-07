async function loadLogs() {

    const response =
        await fetch("/api/logs");

    const data =
        await response.json();

    const table =
        document.getElementById(
            "logsTable"
        );

    table.innerHTML = "";

    data.forEach(function(item) {

        const row =
            document.createElement("tr");

        row.innerHTML =

            "<td>" +
            item.timestamp +
            "</td>" +

            "<td>" +
            item.source_ip +
            "</td>" +

            "<td>" +
            item.destination_ip +
            "</td>" +

            "<td>" +
            item.protocol +
            "</td>" +

            "<td>" +
            item.packet_count +
            "</td>" +

            "<td>" +
            item.attack_type +
            "</td>" +

            "<td>" +
            item.risk +
            "</td>" +

            "<td>" +
            item.status +
            "</td>";

        table.appendChild(row);
    });
}


loadLogs();

setInterval(
    loadLogs,
    5000
);