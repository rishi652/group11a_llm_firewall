from src.risk_engine import analyze_risk


def apply_policy(prompt):

    risk_result = analyze_risk(prompt)

    final_decision = risk_result["final_decision"]

    if final_decision == "ALLOW":

        action = "FORWARD_TO_ASSISTANT"
        message = "Prompt is allowed and may be sent to the protected assistant."

    elif final_decision == "REVIEW":

        action = "WAIT_FOR_HUMAN_REVIEW"
        message = "Prompt requires human review before continuing."

    else:

        action = "BLOCK_REQUEST"
        message = "Prompt is blocked by the firewall."

    return {
        "prompt": prompt,
        "risk_result": risk_result,
        "final_decision": final_decision,
        "action": action,
        "message": message
    }