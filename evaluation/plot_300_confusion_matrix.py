import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)

from src.risk_engine import analyze_risk


df = pd.read_csv(
    "data/prompts_300_clean.csv"
)


expected = []
predicted = []


for index, row in df.iterrows():

    prompt = row["prompt_text"]

    result = analyze_risk(prompt)

    expected.append(
        row["expected_decision"]
    )

    predicted.append(
        result["final_decision"]
    )


labels = [
    "ALLOW",
    "REVIEW",
    "BLOCK"
]


matrix = confusion_matrix(
    expected,
    predicted,
    labels=labels
)


display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=labels
)


display.plot()

plt.title(
    "Firewall Evaluation - 300 Prompt Dataset"
)

plt.tight_layout()

plt.savefig(
    "evaluation/confusion_matrix_300.png"
)

plt.show()