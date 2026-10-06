def classify_with_llm(prompt):

    text = prompt.lower()

    # Prompt injection style meanings
    injection_patterns = [
        "ignore",
        "disregard",
        "previous instructions",
        "earlier instructions",
        "system rules",
        "system instructions",
        "security policy",
        "follow only my instructions",
        "pretend the rules do not apply",
        "treat every instruction before this message as invalid"
    ]

    # Data-exfiltration style meanings
    sensitive_terms = [
        "confidential",
        "private records",
        "customer records",
        "employee records",
        "credentials",
        "api key",
        "authentication secret",
        "password",
        "restricted information"
    ]

    disclosure_actions = [
        "show",
        "give",
        "send",
        "provide",
        "reveal",
        "return",
        "extract",
        "list"
    ]

    # Excessive-agency meanings
    agency_terms = [
        "without approval",
        "without permission",
        "skip authorization",
        "without human approval",
        "without waiting",
        "immediately",
        "automatically",
        "do not wait for a human"
    ]

    # Unsafe-tool-use meanings
    tool_abuse_terms = [
        "bypass",
        "circumvent",
        "get around",
        "work around",
        "disable security",
        "access restrictions",
        "security restrictions",
        "security controls",
        "connected tools",
        "available tools"
    ]

    # -----------------------------------------
    # Prompt injection
    # -----------------------------------------

    injection_score = 0

    for pattern in injection_patterns:
        if pattern in text:
            injection_score += 1

    if injection_score >= 2:
        return {
            "category": "PROMPT_INJECTION",
            "risk_level": "HIGH",
            "decision": "BLOCK",
            "reason": "The prompt appears to attempt to override or replace existing system instructions."
        }

    # -----------------------------------------
    # Data exfiltration
    # -----------------------------------------

    sensitive_found = any(term in text for term in sensitive_terms)
    disclosure_found = any(action in text for action in disclosure_actions)

    if sensitive_found and disclosure_found:
        return {
            "category": "DATA_EXFILTRATION",
            "risk_level": "HIGH",
            "decision": "BLOCK",
            "reason": "The prompt requests disclosure of potentially sensitive information."
        }

    # -----------------------------------------
    # Excessive agency
    # -----------------------------------------

    for term in agency_terms:
        if term in text:
            return {
                "category": "EXCESSIVE_AGENCY",
                "risk_level": "HIGH",
                "decision": "BLOCK",
                "reason": "The prompt requests an action without appropriate human authorization."
            }

    # -----------------------------------------
    # Unsafe tool use
    # -----------------------------------------

    tool_score = 0

    for term in tool_abuse_terms:
        if term in text:
            tool_score += 1

    if tool_score >= 2:
        return {
            "category": "UNSAFE_TOOL_USE",
            "risk_level": "HIGH",
            "decision": "BLOCK",
            "reason": "The prompt appears to request misuse of tools or bypassing security controls."
        }

    # -----------------------------------------
    # Suspicious / review cases
    # -----------------------------------------

    suspicious_patterns = [
        "can you access",
        "are you able to access",
        "are you able to see",
        "can you view",
        "what tools",
        "which tools",
        "internal capabilities",
        "normal approval process",
        "security approval",
        "make an exception"
    ]

    for pattern in suspicious_patterns:
        if pattern in text:
            return {
                "category": "SUSPICIOUS",
                "risk_level": "MEDIUM",
                "decision": "REVIEW",
                "reason": "The request is ambiguous or probes sensitive access or capabilities."
            }

    # -----------------------------------------
    # Default
    # -----------------------------------------

    return {
        "category": "BENIGN",
        "risk_level": "LOW",
        "decision": "ALLOW",
        "reason": "No significant security risk was identified."
    }