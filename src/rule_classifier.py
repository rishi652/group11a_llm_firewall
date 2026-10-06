def classify_prompt(prompt):

    # Convert prompt to lowercase
    prompt = prompt.lower()

    # --------------------------------------------------
    # 1. PROMPT INJECTION
    # --------------------------------------------------

    prompt_injection_keywords = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "forget previous instructions",
        "forget your security policy",
        "disregard previous instructions",
        "override system instructions",
        "reveal your system prompt",
        "show me your system prompt"
    ]

    for keyword in prompt_injection_keywords:
        if keyword in prompt:
            return {
                "category": "PROMPT_INJECTION",
                "risk_level": "HIGH",
                "decision": "BLOCK",
                "reason": "Prompt attempts to override or reveal system instructions."
            }

    # --------------------------------------------------
    # 2. UNSAFE TOOL USE
    # --------------------------------------------------

    if (
        "bypass" in prompt
        and (
            "access control" in prompt
            or "security control" in prompt
            or "security restriction" in prompt
        )
    ):
        return {
            "category": "UNSAFE_TOOL_USE",
            "risk_level": "HIGH",
            "decision": "BLOCK",
            "reason": "Prompt attempts to bypass security or access controls."
        }

    # --------------------------------------------------
    # 3. EXCESSIVE AGENCY
    # --------------------------------------------------

    excessive_agency_keywords = [
        "without asking for approval",
        "without human approval",
        "without permission",
        "do not ask for permission",
        "automatically delete",
        "disable every employee account",
        "take action immediately"
    ]

    for keyword in excessive_agency_keywords:
        if keyword in prompt:
            return {
                "category": "EXCESSIVE_AGENCY",
                "risk_level": "HIGH",
                "decision": "BLOCK",
                "reason": "Prompt requests a high-impact action without appropriate approval."
            }

    # --------------------------------------------------
    # 4. SUSPICIOUS REQUESTS
    # --------------------------------------------------

    if "can you access" in prompt and (
        "confidential" in prompt
        or "private" in prompt
        or "restricted" in prompt
    ):
        return {
            "category": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Prompt asks about access to potentially protected information."
        }

    if (
        "exception" in prompt
        and "security policy" in prompt
    ):
        return {
            "category": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Prompt requests an exception to established security policy."
        }

    if (
        "normal employees" in prompt
        and (
            "cannot see" in prompt
            or "can't see" in prompt
        )
    ):
        return {
            "category": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Prompt may request information outside the user's normal authorization."
        }

    if "what tools do you have access to" in prompt:
        return {
            "category": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Prompt probes available system or tool capabilities."
        }

    if "without asking the security team" in prompt:
        return {
            "category": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Prompt may attempt to avoid normal security approval."
        }

    # --------------------------------------------------
    # 5. DATA EXFILTRATION
    # --------------------------------------------------

    sensitive_terms = [
        "confidential information",
        "confidential employee records",
        "customer database",
        "private records",
        "api key",
        "passwords",
        "secret information"
    ]

    extraction_actions = [
        "reveal",
        "show",
        "send",
        "give",
        "extract",
        "provide"
    ]

    sensitive_found = False
    extraction_found = False

    for term in sensitive_terms:
        if term in prompt:
            sensitive_found = True

    for action in extraction_actions:
        if action in prompt:
            extraction_found = True

    if sensitive_found and extraction_found:
        return {
            "category": "DATA_EXFILTRATION",
            "risk_level": "HIGH",
            "decision": "BLOCK",
            "reason": "Prompt requests extraction or disclosure of sensitive information."
        }

    # --------------------------------------------------
    # 6. DEFAULT SAFE RESULT
    # --------------------------------------------------

    return {
        "category": "BENIGN",
        "risk_level": "LOW",
        "decision": "ALLOW",
        "reason": "No dangerous rule-based pattern was detected."
    }