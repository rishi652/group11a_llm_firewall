import pandas as pd

from src.risk_engine import analyze_risk


df = pd.read_csv(
    "data/prompts_300_clean.csv"
)


results = []


for index, row in df.iterrows():

    prompt = row["prompt_text"]

    result = analyze_risk(prompt)

    rule_result = result["rule_result"]

    semantic_result = (
        result["semantic_result"]
    )


    results.append({

        "prompt_id":
            row["prompt_id"],

        "prompt_text":
            prompt,

        "expected_category":
            row["category"],

        "expected_decision":
            row["expected_decision"],

        "rule_category":
            rule_result["category"],

        "rule_decision":
            rule_result["decision"],

        "semantic_category":
            semantic_result["category"],

        "semantic_decision":
            semantic_result["decision"],

        "final_risk":
            result["final_risk"],

        "final_decision":
            result["final_decision"],

        "correct":
            result["final_decision"]
            == row["expected_decision"]
    })


results_df = pd.DataFrame(
    results
)


results_df.to_csv(
    "evaluation/results_300.csv",
    index=False
)


print(
    "Saved:",
    "evaluation/results_300.csv"
)

print(
    "Total results:",
    len(results_df)
)

print(
    "Correct:",
    results_df["correct"].sum()
)

print(
    "Incorrect:",
    (~results_df["correct"]).sum()
)