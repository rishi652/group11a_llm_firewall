import csv
import os
from datetime import datetime


LOG_FILE = "data/logs.csv"


def log_decision(
    prompt,
    category,
    risk_level,
    decision,
    action,
    selected_tool="N/A",
    latency_seconds=0.0,
    error_status="NONE"
):
    """
    Save firewall activity to a CSV log file.
    """

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(LOG_FILE)

    with open(
        LOG_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "prompt",
                "category",
                "risk_level",
                "decision",
                "action",
                "selected_tool",
                "latency_seconds",
                "error_status"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            prompt,
            category,
            risk_level,
            decision,
            action,
            selected_tool,
            round(latency_seconds, 3),
            error_status
        ])