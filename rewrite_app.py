import sys

with open('app.py', 'r') as f:
    text = f.read()

# Text Rebranding
text = text.replace("ClearCatchICS", "SENTINEL-OT")
text = text.replace("OT Security Monitor", "OT Threat Intelligence Platform")
text = text.replace("// INDUSTRIAL CONTROL SYSTEM — THREAT DETECTION ENGINE //", "// OT THREAT INTELLIGENCE PLATFORM //")
text = text.replace("OT SECURITY OPERATIONS CENTER", "POWERED BY ISOLATION FOREST + OC-SVM")

# Color Rebranding
text = text.replace("#00c8ff", "#00B4D8")
text = text.replace("#00ff9d", "#06D6A0") 
text = text.replace("#ff3b5c", "#E63946")
text = text.replace("#ffb830", "#F4A261")
text = text.replace("#a8ff3b", "#FFD166") # MEDIUM severity

with open('app.py', 'w') as f:
    f.write(text)
