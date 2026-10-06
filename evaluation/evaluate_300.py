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


# -----------------------------------------
# LOAD DATASET
# -----------------------------------------

df = pd.read_csv(
    "data/prompts_300_clean.csv"
)


expected = []
predicted = []


# -----------------------------------------
# RUN FIREWALL ON EVERY PROMPT
# -----------------------------------------

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


# -----------------------------------------
# METRICS
# -----------------------------------------

accuracy = accuracy_score(
    expected,
    predicted
)

precision = precision_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    expected,
    predicted,
    average="weighted",
    zero_division=0
)


# -----------------------------------------
# PRINT RESULTS
# -----------------------------------------

print("\n================================")
print("300-PROMPT FIREWALL EVALUATION")
print("================================")

print(
    "Total prompts:",
    len(df)
)

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


# -----------------------------------------
# CONFUSION MATRIX
# -----------------------------------------

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


print("\nCONFUSION MATRIX")

print(labels)
print(matrix)