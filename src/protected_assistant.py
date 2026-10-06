def generate_response(prompt):

    text = prompt.lower()

    if "phishing" in text:
        return (
            "Phishing is a social-engineering attack in which an attacker "
            "tries to trick a user into revealing sensitive information or "
            "taking an unsafe action."
        )

    elif "multi-factor authentication" in text or "mfa" in text:
        return (
            "Multi-factor authentication improves account security by requiring "
            "more than one type of verification before access is granted."
        )

    elif "ransomware" in text:
        return (
            "Ransomware is malicious software that can encrypt files or systems "
            "and demand payment for restoration."
        )

    elif "password" in text:
        return (
            "Strong passwords should be long, unique, difficult to guess, "
            "and should not be reused across different accounts."
        )

    else:
        return (
            "The protected assistant received the approved request. "
            "A production version could send this prompt to an approved LLM."
        )