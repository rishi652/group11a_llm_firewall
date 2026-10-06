# Prompt Injection Detection and LLM Firewall Agent

## Group 11A
AI/ML in Cybersecurity  
Laurentian University  
Fall 2026

## Project Overview

This project implements a defensive LLM firewall that analyzes user prompts before they reach a protected AI assistant.

The system identifies:

- Prompt injection
- Data exfiltration attempts
- Excessive agency
- Unsafe tool use
- Suspicious requests
- Benign requests

The firewall produces one of three decisions:

- ALLOW
- REVIEW
- BLOCK

## Project Architecture

User Prompt  
↓  
Rule-Based Classifier  
↓  
Semantic-Style Classifier  
↓  
Risk Engine  
↓  
Policy Agent  
↓  
ALLOW / REVIEW / BLOCK  
↓  
Human Review when required  
↓  
Protected Assistant  
↓  
Logging and Dashboard

## Main Components

### Rule-Based Classifier

Detects known risky phrases and patterns.

File:

src/rule_classifier.py

### Semantic-Style Classifier

Provides broader pattern-based semantic detection.

File:

src/llm_classifier.py

Note: This is currently a rule-based semantic prototype and not a genuine LLM.

### Risk Engine

Combines classifier outputs and determines the final risk level.

File:

src/risk_engine.py

### Policy Agent

Applies the ALLOW, REVIEW, or BLOCK policy.

File:

src/policy_agent.py

### Human Review

Allows suspicious prompts to be manually approved or rejected.

File:

src/human_review.py

### Protected Assistant

Generates a safe response for approved prompts.

File:

src/protected_assistant.py

### Logging

Stores firewall decisions for later analysis.

File:

src/logger.py

### Streamlit Application

Provides the interactive firewall interface and dashboard.

File:

app.py

## Dataset

The main dataset contains 300 synthetic prompts.

Categories:

- BENIGN
- SUSPICIOUS
- PROMPT_INJECTION
- DATA_EXFILTRATION
- EXCESSIVE_AGENCY
- UNSAFE_TOOL_USE

Dataset:

data/prompts_300.csv

Cleaned dataset:

data/prompts_300_clean.csv

Dataset generation script:

data/generate_dataset.py

## Preprocessing

The preprocessing pipeline:

- removes duplicates
- removes missing prompts
- converts text to lowercase
- removes extra spaces
- standardizes labels

File:

src/preprocessing.py

## Evaluation

The system is evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Error analysis
- Adversarial bypass testing

### 300-Prompt Dataset Results

Accuracy: 64.0%

Weighted Precision: 85.48%

Weighted Recall: 64.0%

Weighted F1 Score: 67.11%

### Bypass Test Results

Accuracy: 55.0%

Weighted Precision: 92.0%

Weighted Recall: 55.0%

Weighted F1 Score: 63.0%

## Current Limitations

The system currently relies heavily on keyword and phrase matching.

The semantic classifier is a rule-based prototype rather than a genuine LLM.

The system may therefore struggle with:

- paraphrased attacks
- multilingual prompts
- obfuscated instructions
- indirect prompt injection
- multi-turn attacks
- unusual tool-use requests

## Future Improvements

Future work may include:

- integration with a real LLM classifier
- confidence scoring
- multilingual detection
- indirect prompt-injection detection
- stronger adversarial testing
- multi-turn conversation analysis
- improved unsafe-tool-use detection
- more independent test data

## Installation

Create a virtual environment:

python -m venv venv

Install dependencies:

pip install -r requirements.txt

Run preprocessing:

python -m src.preprocessing

Run the Streamlit app:

streamlit run app.py

## Safety

This project is intended for defensive cybersecurity education and research only.

The system uses synthetic data and does not interact with real confidential systems or credentials.