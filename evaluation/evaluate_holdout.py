import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

from src.risk_engine import analyze_risk


df = pd.read_csv("data/holdout_60.csv")

expected = []
predicted = []

for _, row in df.iterrows():
    result = analyze_risk(row["prompt_text"])

    expected.append(row["expected_decision"])
    predicted.append(result["final_decision"])


accuracy = accuracy_score(expected, predicted)
precision = precision_score(expected, predicted, average="weighted", zero_division=0)
recall = recall_score(expected, predicted, average="weighted", zero_division=0)
f1 = f1_score(expected, predicted, average="weighted", zero_division=0)


print("\n==============================")
print("HOLDOUT SET EVALUATION")
print("==============================")

print("Total prompts:", len(df))
print("Accuracy:", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall:", round(recall * 100, 2), "%")
print("F1 Score:", round(f1 * 100, 2), "%")

print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        expected,
        predicted,
        labels=["ALLOW", "REVIEW", "BLOCK"],
        zero_division=0
    )
)

print("\nCONFUSION MATRIX")
print(["ALLOW", "REVIEW", "BLOCK"])
print(
    confusion_matrix(
        expected,
        predicted,
        labels=["ALLOW", "REVIEW", "BLOCK"]
    )
)