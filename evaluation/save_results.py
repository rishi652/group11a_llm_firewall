import pandas as pd

from src.risk_engine import analyze_risk


df = pd.read_csv(
    "evaluation/bypass_tests.csv"
)


results = []


for index, row in df.iterrows():

    prompt = row["prompt_text"]

    expected_category = (
        row["expected_category"]
    )

    expected_decision = (
        row["expected_decision"]
    )

    result = analyze_risk(prompt)

    rule_result = (
        result["rule_result"]
    )

    semantic_result = (
        result["semantic_result"]
    )


    results.append({

        "prompt":
            prompt,

        "expected_category":
            expected_category,

        "expected_decision":
            expected_decision,

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
            == expected_decision
    })


results_df = pd.DataFrame(
    results
)


results_df.to_csv(
    "evaluation/results.csv",
    index=False
)


print(
    "Results saved to evaluation/results.csv"
)