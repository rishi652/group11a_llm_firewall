import pandas as pd

from src.risk_engine import analyze_risk


# Load the untouched holdout dataset
df = pd.read_csv("data/holdout_60.csv")

rows = []

for _, row in df.iterrows():

    result = analyze_risk(row["prompt_text"])

    rows.append({
        "prompt_id": row["prompt_id"],
        "prompt_text": row["prompt_text"],

        "expected_category": row["category"],
        "expected_decision": row["expected_decision"],

        "rule_category": result["rule_result"]["category"],
        "rule_decision": result["rule_result"]["decision"],

        "llm_category": result["semantic_result"]["category"],
        "llm_decision": result["semantic_result"]["decision"],

        "final_risk": result["final_risk"],
        "final_decision": result["final_decision"],

        "correct": (
            row["expected_decision"]
            == result["final_decision"]
        )
    })


results_df = pd.DataFrame(rows)


output_file = "evaluation/final_holdout_results.csv"

results_df.to_csv(
    output_file,
    index=False
)


print("Saved:", output_file)
print("Total results:", len(results_df))

print(
    "Correct:",
    results_df["correct"].sum()
)

print(
    "Incorrect:",
    (~results_df["correct"]).sum()
)