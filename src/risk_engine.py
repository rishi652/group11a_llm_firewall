from src.rule_classifier import classify_prompt
from src.llm_classifier import classify_with_llm


def analyze_risk(prompt):

    rule_result = classify_prompt(prompt)
    semantic_result = classify_with_llm(prompt)

    rule_risk = rule_result["risk_level"]
    semantic_risk = semantic_result["risk_level"]

    if rule_risk == "HIGH" or semantic_risk == "HIGH":

        final_risk = "HIGH"
        final_decision = "BLOCK"

    elif rule_risk == "MEDIUM" or semantic_risk == "MEDIUM":

        final_risk = "MEDIUM"
        final_decision = "REVIEW"

    else:

        final_risk = "LOW"
        final_decision = "ALLOW"

    return {
        "rule_result": rule_result,
        "semantic_result": semantic_result,
        "final_risk": final_risk,
        "final_decision": final_decision
    }