MITRE_ICS_MAP = {
    "tank_manipulation": {
        "technique_id": "T0831",
        "technique_name": "Manipulation of Control",
        "tactic": "Impair Process Control",
        "severity": "CRITICAL",
        "operator_action": "Isolate tank level controllers immediately",
        "description": "Adversary manipulating tank sensor readings to cause overflow or drainage"
    },
    "pump_manipulation": {
        "technique_id": "T0855",
        "technique_name": "Unauthorized Command Message",
        "tactic": "Impair Process Control",
        "severity": "HIGH",
        "operator_action": "Shut down affected pump segment",
        "description": "Unauthorized commands sent to pump actuators via Modbus protocol"
    },
    "pressure_spoofing": {
        "technique_id": "T0856",
        "technique_name": "Spoof Reporting Message",
        "tactic": "Impair Process Control",
        "severity": "HIGH",
        "operator_action": "Cross-verify pressure with manual gauges",
        "description": "Pressure sensor readings being falsified to mask actual system state"
    },
    "multi_sensor_deviation": {
        "technique_id": "T0801",
        "technique_name": "Monitor Process State",
        "tactic": "Collection",
        "severity": "MEDIUM",
        "operator_action": "Increase monitoring frequency and alert supervisor",
        "description": "Multiple sensors deviating simultaneously indicating reconnaissance or staged attack"
    },
    "flow_anomaly": {
        "technique_id": "T0882",
        "technique_name": "Theft of Operational Information",
        "tactic": "Collection",
        "severity": "MEDIUM",
        "operator_action": "Audit recent flow control commands",
        "description": "Abnormal flow patterns suggesting unauthorized process state collection"
    }
}

def classify_attack(triggered_features):
    has_tank = any('L_T' in f for f in triggered_features)
    has_pump = any('F_PU' in f or 'S_PU' in f for f in triggered_features)
    has_pressure = any('P_J' in f for f in triggered_features)
    count = sum([has_tank, has_pump, has_pressure])
    if count >= 2:
        return MITRE_ICS_MAP["multi_sensor_deviation"]
    elif has_tank:
        return MITRE_ICS_MAP["tank_manipulation"]
    elif has_pump:
        return MITRE_ICS_MAP["pump_manipulation"]
    elif has_pressure:
        return MITRE_ICS_MAP["pressure_spoofing"]
    else:
        return MITRE_ICS_MAP["flow_anomaly"]

def get_alert_message(mitre_entry, triggered_features):
    return (
        f"ALERT: {mitre_entry['description']}. "
        f"Affected sensors: {triggered_features}. "
        f"MITRE ATT&CK ICS: {mitre_entry['technique_id']} "
        f"— {mitre_entry['technique_name']}. "
        f"Recommended Action: {mitre_entry['operator_action']}"
    )
