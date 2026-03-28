import json

# Initialize dictionaries and list
level_counts = {}
service_counts = {}
error_logs = []

# Read the log file
with open("clean_logs_l4.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            continue
        ts, level, service, msg = parts
        # Count levels
        level_counts[level] = level_counts.get(level, 0) + 1
        # Count services
        service_counts[service] = service_counts.get(service, 0) + 1
        # Collect ERROR logs
        if level == "ERROR":
            error_logs.append(line)

# Create summary dictionary
summary = {
    "level_counts": level_counts,
    "service_counts": service_counts
}

# Save JSON summary
with open("summary_l4.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

# Build human-readable report
report_lines = []
report_lines.append("INCIDENT MINI-REPORT")
report_lines.append("")
report_lines.append("INFO: {}".format(level_counts.get("INFO", 0)))
report_lines.append("WARN: {}".format(level_counts.get("WARN", 0)))
report_lines.append("ERROR: {}".format(level_counts.get("ERROR", 0)))
report_lines.append("")
report_lines.append("Top services:")
# Sort services by count descending
sorted_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)
for service, count in sorted_services:
    report_lines.append("{}: {}".format(service, count))
report_lines.append("")
report_lines.append("Sample ERROR logs:")
for error in error_logs:
    report_lines.append(error)

report_text = "\n".join(report_lines)

# Save incident report
with open("incident_report_l4.txt", "w", encoding="utf-8") as f:
    f.write(report_text)