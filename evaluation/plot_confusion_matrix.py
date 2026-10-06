import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from src.risk_engine import analyze_risk


df = pd.read_csv(
    "evaluation/bypass_tests.csv"
)


expected = []
predicted = []


for index, row in df.iterrows():

    prompt = row["prompt_text"]

    expected_decision = (
        row["expected_decision"]
    )

    result = analyze_risk(prompt)

    predicted_decision = (
        result["final_decision"]
    )

    expected.append(
        expected_decision
    )

    predicted.append(
        predicted_decision
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
    "LLM Firewall Confusion Matrix"
)

plt.tight_layout()

plt.savefig(
    "evaluation/confusion_matrix.png"
)

plt.show()