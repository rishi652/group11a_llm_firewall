# Data Card: Group 11A Prompt Injection Dataset

## 1. Dataset Name

Group 11A Synthetic Prompt Injection and LLM Firewall Dataset

## 2. Project

Prompt Injection Detection and LLM Firewall Agent

AI/ML in Cybersecurity  
Laurentian University  
Fall 2026

## 3. Dataset Purpose

This dataset was created to support the development and evaluation of a defensive LLM firewall.

The firewall analyzes user prompts and determines whether they should be:

- ALLOW
- REVIEW
- BLOCK

The dataset contains examples of normal, suspicious, and malicious prompts that could be submitted to an enterprise AI assistant.

## 4. Dataset Size

The main dataset contains 300 synthetic prompts.

## 5. Categories

The dataset contains the following categories:

- BENIGN
- SUSPICIOUS
- PROMPT_INJECTION
- DATA_EXFILTRATION
- EXCESSIVE_AGENCY
- UNSAFE_TOOL_USE

## 6. Category Distribution

BENIGN: 60 prompts

SUSPICIOUS: 60 prompts

PROMPT_INJECTION: 45 prompts

DATA_EXFILTRATION: 45 prompts

EXCESSIVE_AGENCY: 45 prompts

UNSAFE_TOOL_USE: 45 prompts

Total: 300 prompts

## 7. Risk Levels

The dataset uses three risk levels:

LOW:
Normal and safe requests.

MEDIUM:
Ambiguous or potentially sensitive requests requiring human review.

HIGH:
Clearly malicious or unsafe requests.

## 8. Decision Labels

LOW risk prompts are normally labeled:

ALLOW

MEDIUM risk prompts are normally labeled:

REVIEW

HIGH risk prompts are normally labeled:

BLOCK

## 9. Dataset Schema

The dataset contains the following columns:

### prompt_id

A unique identifier assigned to every prompt.

### prompt_text

The text submitted by the simulated user.

### category

The assigned cybersecurity risk category.

### risk_level

The expected risk level:

- LOW
- MEDIUM
- HIGH

### expected_decision

The expected firewall decision:

- ALLOW
- REVIEW
- BLOCK

### reason

A short explanation describing why the prompt received the assigned label.

### source

The origin of the example.

All prompts in the current dataset use:

synthetic

## 10. Dataset Generation

The dataset was generated programmatically using Python templates.

The generator combines different sentence templates with cybersecurity topics, actions, sensitive resources, and security-policy scenarios.

A fixed random seed of 42 was used to make generation reproducible.

The dataset generation script is located at:

data/generate_dataset.py

The resulting dataset is stored at:

data/prompts_300.csv

## 11. Intended Use

The dataset is intended for:

- defensive cybersecurity research
- prompt-injection detection
- LLM firewall prototyping
- rule-based classifier evaluation
- semantic classifier testing
- agent decision-policy testing
- cybersecurity education

## 12. Not Intended For

The dataset is not intended for:

- offensive cybersecurity operations
- attacking real AI systems
- extracting real confidential information
- testing systems without authorization
- representing real employee or customer activity

## 13. Privacy

The dataset contains no real:

- employee information
- student information
- customer information
- passwords
- API keys
- company records
- personal data

All examples are synthetic.

## 14. Safety

The project is designed for defensive cybersecurity purposes only.

Malicious prompts are simulated and are used only to test whether the firewall correctly identifies unsafe requests.

No real systems are targeted.

No live malware is included.

No real credentials or private records are used.

## 15. Limitations

The dataset has several limitations.

First, the prompts are synthetic rather than collected from real enterprise LLM traffic.

Second, template-generated prompts may contain repeated linguistic patterns.

Third, the dataset may not represent every possible prompt-injection technique.

Fourth, attackers can use paraphrasing, indirect wording, multilingual prompts, encoding, or other techniques that may not be represented.

Fifth, class labels are manually defined according to the project policy and may contain subjective decisions.

## 16. Known Bias

Because prompts are generated using predefined English-language templates, the dataset is biased toward English phrasing and the specific security terminology used during dataset generation.

The system may therefore perform worse on:

- unusual wording
- slang
- multilingual prompts
- heavily obfuscated prompts
- indirect prompt injection

## 17. Evaluation Strategy

The main dataset is used for development.

Separate test datasets are maintained for evaluation:

evaluation/test_cases.csv

and

evaluation/bypass_tests.csv

The bypass dataset contains paraphrased and adversarial prompts designed to test whether the classifier can generalize beyond familiar keywords.

## 18. Current Findings

The baseline rule-based classifier performs strongly on familiar prompt patterns but shows significantly reduced performance on paraphrased bypass prompts.

The broader semantic-style classifier improves detection of some paraphrased attacks but still misses several adversarial examples.

These results demonstrate the limitation of exact keyword matching and motivate future integration of a real LLM-based classifier.

## 19. Future Improvements

Future versions of the dataset could include:

- multilingual prompts
- indirect prompt injection
- encoded or obfuscated instructions
- multi-turn conversations
- tool-use attacks
- RAG-based injection attempts
- more diverse benign prompts
- more independently generated adversarial test cases

## 20. Ethical Considerations

The dataset is intended only for defensive security research and education.

All testing should remain within simulated or authorized environments.

Human approval should be required before sensitive actions are performed.