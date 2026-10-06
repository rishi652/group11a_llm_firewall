import streamlit as st
import pandas as pd
import os

from src.policy_agent import apply_policy
from src.protected_assistant import generate_response
from src.human_review import human_review
from src.logger import log_decision


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LLM Firewall",
    page_icon="🛡️",
    layout="wide"
)


st.title("🛡️ Prompt Injection Detection and LLM Firewall")

st.write(
    "Group 11A - AI/ML in Cybersecurity Capstone Project"
)

st.write(
    "This system analyzes prompts before they reach a protected assistant."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

if "review_completed" not in st.session_state:
    st.session_state.review_completed = False


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

prompt = st.text_area(
    "Enter a prompt:",
    height=150
)


if st.button("Analyze Prompt"):

    if prompt.strip() == "":

        st.warning(
            "Please enter a prompt."
        )

    else:

        # Analyze prompt
        result = apply_policy(prompt)

        # Save result so it survives Streamlit reruns
        st.session_state.analysis_result = result
        st.session_state.current_prompt = prompt
        st.session_state.review_completed = False


        risk_result = result["risk_result"]
        semantic_result = risk_result["semantic_result"]

        final_risk = risk_result["final_risk"]
        final_decision = result["final_decision"]
        action = result["action"]


        # Log ALLOW immediately
        if final_decision == "ALLOW":

            log_decision(
                prompt=prompt,
                category=semantic_result["category"],
                risk_level=final_risk,
                decision="ALLOW",
                action="FORWARD_TO_ASSISTANT"
            )


        # Log BLOCK immediately
        elif final_decision == "BLOCK":

            log_decision(
                prompt=prompt,
                category=semantic_result["category"],
                risk_level=final_risk,
                decision="BLOCK",
                action="BLOCK_REQUEST"
            )


        # IMPORTANT:
        # REVIEW is NOT logged yet.
        # We wait until the human clicks APPROVE or REJECT.


# --------------------------------------------------
# DISPLAY ANALYSIS RESULT
# --------------------------------------------------

if st.session_state.analysis_result is not None:

    result = st.session_state.analysis_result
    current_prompt = st.session_state.current_prompt

    risk_result = result["risk_result"]

    rule_result = risk_result["rule_result"]
    semantic_result = risk_result["semantic_result"]

    final_risk = risk_result["final_risk"]
    final_decision = result["final_decision"]
    action = result["action"]


    # --------------------------------------------------
    # RESULT SUMMARY
    # --------------------------------------------------

    st.subheader("Firewall Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Final Risk",
            final_risk
        )

    with col2:
        st.metric(
            "Decision",
            final_decision
        )

    with col3:
        st.metric(
            "Action",
            action
        )


    # --------------------------------------------------
    # CLASSIFIER DETAILS
    # --------------------------------------------------

    st.subheader("Classifier Details")

    st.write("### Rule-Based Classifier")

    st.write(
        "Category:",
        rule_result["category"]
    )

    st.write(
        "Risk:",
        rule_result["risk_level"]
    )

    st.write(
        "Reason:",
        rule_result["reason"]
    )


    st.write("### Semantic Classifier")

    st.write(
        "Category:",
        semantic_result["category"]
    )

    st.write(
        "Risk:",
        semantic_result["risk_level"]
    )

    st.write(
        "Reason:",
        semantic_result["reason"]
    )


    # --------------------------------------------------
    # ALLOW
    # --------------------------------------------------

    if final_decision == "ALLOW":

        st.success(
            "Prompt allowed."
        )

        response = generate_response(
            current_prompt
        )

        st.subheader(
            "Protected Assistant Response"
        )

        st.write(
            response
        )


    # --------------------------------------------------
    # REVIEW
    # --------------------------------------------------

    elif final_decision == "REVIEW":

        st.warning(
            "Human review is required."
        )

        st.write(
            "A human reviewer must approve or reject this request."
        )


        if not st.session_state.review_completed:

            col1, col2 = st.columns(2)


            # APPROVE BUTTON
            with col1:

                if st.button(
                    "Approve",
                    key="approve_button"
                ):

                    review_result = human_review(
                        "APPROVE"
                    )

                    log_decision(
                        prompt=current_prompt,
                        category=semantic_result["category"],
                        risk_level=final_risk,
                        decision="REVIEW",
                        action="HUMAN_APPROVED"
                    )

                    st.session_state.review_completed = True

                    st.success(
                        review_result["message"]
                    )

                    response = generate_response(
                        current_prompt
                    )

                    st.subheader(
                        "Protected Assistant Response"
                    )

                    st.write(
                        response
                    )


            # REJECT BUTTON
            with col2:

                if st.button(
                    "Reject",
                    key="reject_button"
                ):

                    review_result = human_review(
                        "REJECT"
                    )

                    log_decision(
                        prompt=current_prompt,
                        category=semantic_result["category"],
                        risk_level=final_risk,
                        decision="REVIEW",
                        action="HUMAN_REJECTED"
                    )

                    st.session_state.review_completed = True

                    st.error(
                        review_result["message"]
                    )


        else:

            st.info(
                "Human review has been completed for this request."
            )


    # --------------------------------------------------
    # BLOCK
    # --------------------------------------------------

    else:

        st.error(
            "Request blocked by the firewall."
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.divider()

st.header("📊 Firewall Dashboard")


if os.path.exists("data/logs.csv"):

    logs = pd.read_csv(
        "data/logs.csv"
    )

    total = len(logs)

    allowed = len(
        logs[
            logs["decision"] == "ALLOW"
        ]
    )

    review = len(
        logs[
            logs["decision"] == "REVIEW"
        ]
    )

    blocked = len(
        logs[
            logs["decision"] == "BLOCK"
        ]
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Prompts",
        total
    )

    col2.metric(
        "Allowed",
        allowed
    )

    col3.metric(
        "Human Review",
        review
    )

    col4.metric(
        "Blocked",
        blocked
    )


    st.subheader(
        "Recent Firewall Decisions"
    )

    st.dataframe(
        logs.tail(10),
        use_container_width=True
    )


else:

    st.info(
        "No firewall activity has been logged yet."
    )