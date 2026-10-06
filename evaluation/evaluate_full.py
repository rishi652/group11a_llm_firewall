import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from src.risk_engine import analyze_risk


df = pd.read_csv("evaluation/bypass_tests.csv")

expected = []
predicted = []


for index, row in df.iterrows():

    prompt = row["prompt_text"]
    expected_decision = row["expected_decision"]

    result = analyze_risk(prompt)

    predicted_decision = result["final_decision"]

    expected.append(expected_decision)
    predicted.append(predicted_decision)

    print("-----------------------------------")
    print("Prompt:", prompt)
    print("Expected:", expected_decision)
    print("Predicted:", predicted_decision)


# --------------------------------------------------
# BASIC ACCURACY
# --------------------------------------------------

accuracy = accuracy_score(
    expected,
    predicted
)


# --------------------------------------------------
# PRECISION
# --------------------------------------------------

precision = precision_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)


# --------------------------------------------------
# RECALL
# --------------------------------------------------

recall = recall_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)


# --------------------------------------------------
# F1 SCORE
# --------------------------------------------------

f1 = f1_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)


print("\n================================")
print("FINAL FIREWALL EVALUATION")
print("================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print(
    "Precision:",
    round(precision * 100, 2),
    "%"
)

print(
    "Recall:",
    round(recall * 100, 2),
    "%"
)

print(
    "F1 Score:",
    round(f1 * 100, 2),
    "%"
)


print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        expected,
        predicted,
        zero_division=0
    )
)


print("\nCONFUSION MATRIX")

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

print(labels)
print(matrix)