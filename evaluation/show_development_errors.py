import pandas as pd

from src.risk_engine import analyze_risk


df = pd.read_csv("data/development_240.csv")

rows = []

for _, row in df.iterrows():

    result = analyze_risk(row["prompt_text"])

    rows.append({
        "prompt_text": row["prompt_text"],
        "expected_category": row["category"],
        "expected_decision": row["expected_decision"],
        "rule_category": result["rule_result"]["category"],
        "rule_decision": result["rule_result"]["decision"],
        "llm_category": result["semantic_result"]["category"],
        "llm_decision": result["semantic_result"]["decision"],
        "final_decision": result["final_decision"]
    })


results = pd.DataFrame(rows)

errors = results[
    results["expected_decision"] != results["final_decision"]
]


print("\n==============================")
print("DEVELOPMENT ERROR ANALYSIS")
print("==============================")

print("Total predictions:", len(results))
print("Total errors:", len(errors))

print("\nErrors by expected category:")
print(
    errors["expected_category"].value_counts()
)

print("\nErrors by expected decision:")
print(
    errors["expected_decision"].value_counts()
)

print("\nExpected vs predicted:")
print(
    pd.crosstab(
        errors["expected_decision"],
        errors["final_decision"]
    )
)

print("\nDetailed errors:")
print(
    errors.to_string(index=False)
)
