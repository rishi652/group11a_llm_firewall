# Requirements Document

## Project Title

**Prompt Injection Detection and LLM Firewall Agent**

## 1. Project Purpose

The purpose of this project is to build a defensive AI-powered cybersecurity agent that analyzes user prompts before they are sent to a protected AI assistant.

The system identifies potentially unsafe requests and decides whether each prompt should be:

- ALLOWED
- sent for HUMAN REVIEW
- BLOCKED

The project is designed as an academic minimum viable product (MVP) and is not intended to replace production enterprise security controls.

---

## 2. Intended Users

The primary users of the system are:

- cybersecurity analysts
- organizations deploying AI assistants
- security teams evaluating LLM-related risks
- developers building AI-enabled enterprise applications

---

## 3. System Input

The primary system input is:

**A natural-language user prompt**

Example:

```text
Can you access restricted employee information?

The system must also safely handle:
- empty prompts
- malformed input
- ambiguous prompts
- benign prompts
- suspicious prompts
- malicious prompts

##4. System Output

For each analyzed prompt, the system should provide:
- selected cybersecurity tool
- detected security category
- risk level
- final decision
- explanation or reason
- supporting analysis evidence
- analysis latency
- human-review status when applicable
The three possible final decisions are:
- ALLOW
- REVIEW
- BLOCK

## 5. Security Categories

The firewall classifies prompts into six categories:
1. BENIGN
2. SUSPICIOUS
3. PROMPT_INJECTION
4. DATA_EXFILTRATION
5. EXCESSIVE_AGENCY
6. UNSAFE_TOOL_USE

## 6. Risk Levels

LOW
The prompt is considered safe.
Expected policy decision:
ALLOW

MEDIUM
The prompt is uncertain, sensitive, or requires further verification.
Expected policy decision:
REVIEW

HIGH
The prompt is considered unsafe or malicious.
Expected policy decision:
BLOCK

## 7. Dataset Requirements

The project uses a synthetic cybersecurity prompt dataset.
The final dataset contains:
- 300 unique prompts
Category distribution:
- BENIGN: 60
- SUSPICIOUS: 60
- PROMPT_INJECTION: 45
- DATA_EXFILTRATION: 45
- EXCESSIVE_AGENCY: 45
- UNSAFE_TOOL_USE: 45
The dataset is divided into:
- 240 development prompts
- 60 holdout prompts
The holdout dataset is reserved for final evaluation.

## 8. AI and Agent Requirements

The system must use a local large language model.
Current model:
Qwen2.5-1.5B-Instruct

The model is served locally using:
LM Studio

The AI Firewall Agent must be capable of:
- interpreting the user prompt
- selecting an appropriate cybersecurity analysis tool
- executing the selected tool
- interpreting the returned analysis
- producing a final cybersecurity decision
- presenting evidence to the user

## 9. Tool Requirements

The agent has access to two cybersecurity analysis tools.

## 9.1 RULE_SCAN

Purpose:
Perform fast deterministic analysis using predefined security rules.
Used for:
- clearly benign prompts
- obvious prompt-injection attempts
- explicit known malicious patterns
The tool returns:
- category
- risk level
- decision
- reason

## 9.2 FULL_SECURITY_ANALYSIS

Purpose:
Perform deeper security analysis for ambiguous or sensitive requests.
It combines:
- rule-based classification
- Qwen2.5-1.5B-Instruct semantic classification
- hybrid risk analysis
It is used for:
- sensitive-data questions
- access and permission questions
- approval-related requests
- ambiguous prompts
- unusual prompts
- possible tool misuse
- bypass attempts
- uncertain security situations

## 10. Policy Requirements

The policy layer must produce one of three decisions.
ALLOW
The prompt may continue to the protected assistant.
REVIEW
The prompt must wait for a human decision.
BLOCK
The request must be stopped before reaching the protected assistant.
A HIGH-risk result from either security analysis component must result in a BLOCK decision.
A MEDIUM-risk result must result in REVIEW unless a HIGH-risk condition exists.

## 11. Human-in-the-Loop Requirements

Prompts classified as REVIEW must require human approval.
The reviewer must be able to:
- APPROVE the request
- REJECT the request
An approved request may continue toward the protected assistant.
A rejected request must be blocked.
The human-review action must be recorded in the system log.

## 12. User Interface Requirements

The project must provide a Gradio web interface.
The interface must allow users to:
- enter a prompt
- start analysis
- view the selected tool
- view risk level
- view final decision
- view supporting evidence
- approve or reject REVIEW requests

## 13. Evidence Requirements

The application must display evidence explaining how the cybersecurity decision was produced.
For RULE_SCAN, the system should display:
- selected tool
- detected category
- risk level
- decision
- rule-based reason
For FULL_SECURITY_ANALYSIS, the system should display:
- rule-based classifier result
- local LLM classifier result
- final hybrid risk level
- final decision
- explanation or reason

## 14. Failure-Handling Requirements

The system must fail safely.

## 14.1 Empty Input

Empty input must not be processed.
Expected response:
INVALID INPUT

## 14.2 Local LLM Failure

If LM Studio or the local model is unavailable, the system must not automatically allow the request.
The fail-safe response should be:
Risk Level: MEDIUM
Decision: REVIEW

## 14.3 Unexpected Application Error

Unexpected errors should result in:
REVIEW

rather than automatically allowing the prompt.

## 15. Logging and Monitoring Requirements

The system must record relevant application events.
The log should include:
- timestamp
- user prompt
- detected category
- risk level
- final decision
- resulting action
- selected tool
- analysis latency
- error status
- human-review action when applicable

## 16. Performance Requirements

The system should be evaluated using:
- accuracy
- precision
- recall
- F1-score
- confusion matrix
- bypass testing
- error analysis
The final system achieved the following results on the 60-prompt holdout dataset:
- Accuracy: 93.33%
- Precision: 93.26%
- Recall: 93.33%
- F1-score: 93.12% 

##17. Security Requirements

The project must:
- use synthetic data only
- avoid real confidential or personal information
- operate defensively
- prevent unsafe prompts from automatically reaching the protected assistant
- require human review for uncertain requests
- fail safely when security components are unavailable
- avoid hard-coded credentials or API keys
- record relevant security decisions

## 18. Deployment 

The application must be reproducibly runnable.
Required software includes:
- Python
- Gradio
- LM Studio
- Qwen2.5-1.5B-Instruct
- required Python packages listed in requirements.txt
The source code must be maintained in GitHub with:
- README
- installation instructions
- dependencies
- architecture diagram
- sample inputs
- project documentation

## 19. Acceptance Criteria

The MVP will be considered functional when:
- Gradio accepts a cybersecurity prompt.
- The AI agent selects and executes a cybersecurity analysis tool.
- The system uses a local LLM.
- The system returns an actionable cybersecurity result.
- Supporting evidence is displayed.
- ALLOW, REVIEW, and BLOCK workflows function correctly.
- Human approval and rejection work correctly.
- Empty inputs are handled safely.
- LLM failures are handled safely.
- Decisions and monitoring information are logged.
- Evaluation is documented using test cases and quantitative metrics.
- The application can be reproduced using documented setup instructions.