from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import os
import joblib
import random
from datetime import datetime

app = Flask(
    __name__,
    template_folder="model/templates",
    static_folder="model/templates/static"
)

app.secret_key = "secure_net_project_secret_key"

DATABASE = "database/database.db"

# Load trained ML model
model = joblib.load("model/attack_detection_model.pkl")


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db():

    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# --------------------------------------------------
# CREATE DATABASE TABLE
# --------------------------------------------------

def init_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS traffic_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source_ip TEXT,

            destination_ip TEXT,

            protocol TEXT,

            packet_count INTEGER,

            packet_size REAL,

            connection_rate REAL,

            attack_type TEXT,

            risk TEXT,

            status TEXT,

            timestamp TEXT
        )
    """)

    conn.commit()

    conn.close()


# --------------------------------------------------
# INSERT INITIAL SAMPLE DATA
# --------------------------------------------------

def add_sample_data():

    conn = get_db()

    count = conn.execute(
        "SELECT COUNT(*) FROM traffic_logs"
    ).fetchone()[0]

    # If database already contains records,
    # don't insert duplicate sample data.
    if count > 0:

        conn.close()

        return


    sample_data = [

        (
            "192.168.1.21",
            "192.168.1.1",
            "TCP",
            230,
            1600,
            38,
            "Port Scan",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.25",
            "192.168.1.1",
            "TCP",
            210,
            1500,
            35,
            "DoS Attack",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.32",
            "192.168.1.1",
            "UDP",
            190,
            1400,
            30,
            "Suspicious Traffic",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.40",
            "192.168.1.1",
            "TCP",
            45,
            450,
            8,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.45",
            "192.168.1.1",
            "HTTP",
            35,
            350,
            6,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.51",
            "192.168.1.1",
            "TCP",
            200,
            1700,
            32,
            "Brute Force",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.60",
            "192.168.1.1",
            "UDP",
            30,
            300,
            5,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.71",
            "192.168.1.1",
            "HTTP",
            55,
            500,
            9,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.80",
            "192.168.1.1",
            "TCP",
            250,
            1900,
            42,
            "DoS Attack",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.91",
            "192.168.1.1",
            "TCP",
            40,
            400,
            7,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.101",
            "192.168.1.1",
            "UDP",
            35,
            450,
            6,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.112",
            "192.168.1.1",
            "TCP",
            220,
            1500,
            36,
            "Port Scan",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.125",
            "192.168.1.1",
            "HTTP",
            50,
            500,
            8,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.138",
            "192.168.1.1",
            "TCP",
            180,
            1300,
            25,
            "Suspicious Traffic",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.150",
            "192.168.1.1",
            "UDP",
            42,
            420,
            7,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.160",
            "192.168.1.1",
            "TCP",
            28,
            300,
            5,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.175",
            "192.168.1.1",
            "TCP",
            240,
            1800,
            40,
            "DoS Attack",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.181",
            "192.168.1.1",
            "HTTP",
            38,
            380,
            6,
            "Normal Traffic",
            "LOW",
            "Safe"
        ),

        (
            "192.168.1.190",
            "192.168.1.1",
            "TCP",
            215,
            1550,
            34,
            "Brute Force",
            "HIGH",
            "Detected"
        ),

        (
            "192.168.1.200",
            "192.168.1.1",
            "UDP",
            48,
            450,
            8,
            "Normal Traffic",
            "LOW",
            "Safe"
        )

    ]


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    for item in sample_data:

        conn.execute("""
            INSERT INTO traffic_logs
            (
                source_ip,
                destination_ip,
                protocol,
                packet_count,
                packet_size,
                connection_rate,
                attack_type,
                risk,
                status,
                timestamp
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*item, timestamp))


    conn.commit()

    conn.close()


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route("/")
def home():

    return redirect("/login")


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():

    username = request.form.get("username")

    password = request.form.get("password")


    if username == "admin" and password == "admin123":

        session["user"] = username

        return redirect("/dashboard")


    return render_template(
        "login.html",
        error="Invalid username or password"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# --------------------------------------------------
# PAGES
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/monitoring")
def monitoring():

    if "user" not in session:

        return redirect("/login")

    return render_template("monitoring.html")


@app.route("/logs")
def logs_page():

    if "user" not in session:

        return redirect("/login")

    return render_template("logs.html")


# --------------------------------------------------
# DASHBOARD STATUS API
# --------------------------------------------------

@app.route("/api/status")
def status():

    conn = get_db()


    total = conn.execute(
        "SELECT COUNT(*) FROM traffic_logs"
    ).fetchone()[0]


    attacks = conn.execute(
        """
        SELECT COUNT(*)
        FROM traffic_logs
        WHERE status = 'Detected'
        """
    ).fetchone()[0]


    safe = conn.execute(
        """
        SELECT COUNT(*)
        FROM traffic_logs
        WHERE status = 'Safe'
        """
    ).fetchone()[0]


    conn.close()


    return jsonify({

        "total": total,

        "attacks": attacks,

        "safe": safe,

        "system": "ONLINE"
    })


# --------------------------------------------------
# RECENT EVENTS API
# --------------------------------------------------

@app.route("/api/recent")
def recent_events():

    conn = get_db()


    rows = conn.execute("""
        SELECT *
        FROM traffic_logs
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()


    conn.close()


    return jsonify([
        dict(row)
        for row in rows
    ])


# --------------------------------------------------
# ATTACK DETECTION API
# --------------------------------------------------

@app.route("/api/detect", methods=["POST"])
def detect():

    data = request.get_json() or {}


    source_ip = data.get(
        "source_ip",
        "192.168.1." +
        str(random.randint(10, 220))
    )


    destination_ip = data.get(
        "destination_ip",
        "192.168.1.1"
    )


    protocol = data.get(
        "protocol",
        random.choice([
            "TCP",
            "UDP",
            "HTTP"
        ])
    )


    packet_count = int(
        data.get(
            "packet_count",
            random.randint(10, 300)
        )
    )


    packet_size = float(
        data.get(
            "packet_size",
            random.randint(100, 2000)
        )
    )


    connection_rate = float(
        data.get(
            "connection_rate",
            random.randint(1, 40)
        )
    )


    # ML MODEL INPUT

    features = [[

        packet_count,

        packet_size,

        connection_rate

    ]]


    prediction = model.predict(
        features
    )[0]


    # ATTACK

    if prediction == 1:

        attack_type = random.choice([

            "Port Scan",

            "Brute Force",

            "DoS Attack",

            "Suspicious Traffic"

        ])

        risk = "HIGH"

        status = "Detected"


    # NORMAL

    else:

        attack_type = "Normal Traffic"

        risk = "LOW"

        status = "Safe"


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = get_db()


    conn.execute("""
        INSERT INTO traffic_logs
        (
            source_ip,
            destination_ip,
            protocol,
            packet_count,
            packet_size,
            connection_rate,
            attack_type,
            risk,
            status,
            timestamp
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        source_ip,

        destination_ip,

        protocol,

        packet_count,

        packet_size,

        connection_rate,

        attack_type,

        risk,

        status,

        timestamp
    ))


    conn.commit()

    conn.close()


    return jsonify({

        "source_ip": source_ip,

        "destination_ip":
            destination_ip,

        "protocol": protocol,

        "packet_count":
            packet_count,

        "packet_size":
            packet_size,

        "connection_rate":
            connection_rate,

        "attack_type":
            attack_type,

        "risk": risk,

        "status": status,

        "timestamp": timestamp
    })


# --------------------------------------------------
# ALL LOGS API
# --------------------------------------------------

@app.route("/api/logs")
def get_logs():

    conn = get_db()


    rows = conn.execute("""
        SELECT *
        FROM traffic_logs
        ORDER BY id DESC
        LIMIT 100
    """).fetchall()


    conn.close()


    return jsonify([
        dict(row)
        for row in rows
    ])


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    init_database()

    add_sample_data()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )