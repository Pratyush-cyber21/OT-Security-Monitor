import sqlite3
from datetime import datetime

DB_PATH = 'clearcatchics.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        affected_sensors TEXT,
        iso_score REAL,
        svm_score REAL,
        confidence REAL,
        mitre_id TEXT,
        mitre_technique TEXT,
        severity TEXT,
        operator_action TEXT,
        status TEXT DEFAULT "OPEN"
    )''')
    conn.commit()
    conn.close()

def log_incident(d):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO incidents
        (timestamp, affected_sensors, iso_score, svm_score,
         confidence, mitre_id, mitre_technique, severity,
         operator_action, status)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (
            d.get('timestamp', str(datetime.now())),
            d.get('affected_sensors', ''),
            d.get('iso_score', 0.0),
            d.get('svm_score', 0.0),
            d.get('confidence', 0.0),
            d.get('mitre_id', ''),
            d.get('mitre_technique', ''),
            d.get('severity', ''),
            d.get('operator_action', ''),
            d.get('status', 'OPEN')
        )
    )
    conn.commit()
    conn.close()

def get_all_incidents():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM incidents ORDER BY id DESC')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM incidents')
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM incidents WHERE status='OPEN'")
    open_i = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM incidents WHERE severity='CRITICAL'")
    critical = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM incidents WHERE severity='HIGH'")
    high = c.fetchone()[0]
    conn.close()
    return {'total_incidents': total, 'open_incidents': open_i, 'critical_count': critical, 'high_count': high}

def close_incident(incident_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE incidents SET status='CLOSED' WHERE id=?", (incident_id,))
    conn.commit()
    conn.close()
