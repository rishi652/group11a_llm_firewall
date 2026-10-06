import pandas as pd


df = pd.read_csv(
    "evaluation/results_300.csv"
)

errors = df[
    df["correct"] == False
]

print("\n==============================")
print("ERROR ANALYSIS")
print("==============================")

print("Total predictions:", len(df))
print("Total errors:", len(errors))

print("\nErrors by expected category:")
print(
    errors["expected_category"]
    .value_counts()
)

print("\nErrors by expected decision:")
print(
    errors["expected_decision"]
    .value_counts()
)

print("\nExpected vs predicted decisions:")
print(
    pd.crosstab(
        errors["expected_decision"],
        errors["final_decision"]
    )
)

print("\nDetailed errors:")
print(
    errors[
        [
            "prompt_text",
            "expected_category",
            "expected_decision",
            "rule_category",
            "rule_decision",
            "semantic_category",
            "semantic_decision",
            "final_decision"
        ]
    ].to_string(index=False)
)