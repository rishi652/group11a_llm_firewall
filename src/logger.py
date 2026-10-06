import csv
import os
from datetime import datetime


LOG_FILE = "data/logs.csv"


def log_decision(
    prompt,
    category,
    risk_level,
    decision,
    action
):

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "prompt",
                "category",
                "risk_level",
                "decision",
                "action"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prompt,
            category,
            risk_level,
            decision,
            action
        ])