document
.getElementById("trafficForm")
.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const data = {

            source_ip:
                document.getElementById(
                    "source_ip"
                ).value,

            destination_ip:
                document.getElementById(
                    "destination_ip"
                ).value,

            protocol:
                document.getElementById(
                    "protocol"
                ).value,

            packet_count:
                document.getElementById(
                    "packet_count"
                ).value,

            packet_size:
                document.getElementById(
                    "packet_size"
                ).value,

            connection_rate:
                document.getElementById(
                    "connection_rate"
                ).value
        };


        const response =
            await fetch(
                "/api/detect",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        const result =
            await response.json();


        document.getElementById(
            "detectionResult"
        ).innerHTML =

        "<h3>" +
        result.status +
        "</h3>" +

        "<p>Attack Type: " +
        result.attack_type +
        "</p>" +

        "<p>Risk Level: " +
        result.risk +
        "</p>" +

        "<p>Source IP: " +
        result.source_ip +
        "</p>" +

        "<p>Destination IP: " +
        result.destination_ip +
        "</p>" +

        "<p>Timestamp: " +
        result.timestamp +
        "</p>";
    }
);