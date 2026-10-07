// ==========================================
// UPDATE DASHBOARD STATISTICS
// ==========================================

async function updateDashboard() {

    try {

        const response =
            await fetch("/api/status");

        const data =
            await response.json();


        document.getElementById("total")
            .textContent = data.total;


        document.getElementById("attacks")
            .textContent = data.attacks;


        document.getElementById("safe")
            .textContent = data.safe;


        document.getElementById("system")
            .textContent = data.system;

    }

    catch (error) {

        console.log(
            "Dashboard update error:",
            error
        );

    }

}



// ==========================================
// LOAD RECENT EVENTS
// ==========================================

async function loadRecentEvents() {

    try {

        const response =
            await fetch("/api/recent");


        const events =
            await response.json();


        const table =
            document.getElementById(
                "recentEvents"
            );


        table.innerHTML = "";


        if (events.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No network events available
                    </td>
                </tr>
            `;

            return;
        }


        events.forEach(function(event) {


            const row =
                document.createElement("tr");


            let riskClass = "";


            if (event.risk === "HIGH") {

                riskClass = "risk-high";

            }

            else if (event.risk === "MEDIUM") {

                riskClass = "risk-medium";

            }

            else {

                riskClass = "risk-low";

            }



            let statusClass = "";


            if (event.status === "Detected") {

                statusClass =
                    "status-detected";

            }

            else {

                statusClass =
                    "status-safe";

            }



            row.innerHTML = `

                <td>
                    ${event.source_ip}
                </td>

                <td>
                    ${event.destination_ip}
                </td>

                <td>
                    ${event.protocol}
                </td>

                <td>
                    ${event.attack_type}
                </td>

                <td class="${riskClass}">
                    ${event.risk}
                </td>

                <td class="${statusClass}">
                    ${event.status}
                </td>

                <td>
                    ${event.timestamp}
                </td>

            `;


            table.appendChild(row);

        });

    }

    catch (error) {

        console.log(
            "Events loading error:",
            error
        );

    }

}



// ==========================================
// AUTOMATIC NETWORK TRAFFIC GENERATOR
// ==========================================

async function generateTraffic() {

    try {


        const packetCount =
            Math.floor(
                Math.random() * 300
            ) + 1;


        const packetSize =
            Math.floor(
                Math.random() * 1900
            ) + 100;


        const connectionRate =
            Math.floor(
                Math.random() * 40
            ) + 1;


        const sourceIP =
            "192.168.1." +
            Math.floor(
                Math.random() * 220
            ) + 10;


        const protocols = [
            "TCP",
            "UDP",
            "HTTP"
        ];


        const protocol =
            protocols[
                Math.floor(
                    Math.random() *
                    protocols.length
                )
            ];


        await fetch(
            "/api/detect",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    source_ip:
                        sourceIP,

                    destination_ip:
                        "192.168.1.1",

                    protocol:
                        protocol,

                    packet_count:
                        packetCount,

                    packet_size:
                        packetSize,

                    connection_rate:
                        connectionRate

                })

            }
        );


        // Refresh dashboard

        updateDashboard();

        loadRecentEvents();


    }

    catch (error) {

        console.log(
            "Traffic generation error:",
            error
        );

    }

}



// ==========================================
// INITIAL LOAD
// ==========================================

updateDashboard();

loadRecentEvents();



// ==========================================
// AUTO REFRESH DASHBOARD
// ==========================================

setInterval(
    updateDashboard,
    3000
);


setInterval(
    loadRecentEvents,
    3000
);



// ==========================================
// GENERATE NEW EVENT EVERY 5 SECONDS
// ==========================================

setInterval(
    generateTraffic,
    5000
);