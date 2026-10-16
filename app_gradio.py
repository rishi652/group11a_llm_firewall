import time
import gradio as gr

from src.firewall_agent import run_firewall_agent
from src.human_review import human_review
from src.logger import log_decision


def analyze_prompt(prompt):
    """
    Analyze a user prompt using the Firewall Agent.
    The agent selects a cybersecurity tool, executes it,
    and returns a structured security decision.
    """

    if not prompt or not prompt.strip():
        return (
            "INVALID INPUT",
            "N/A",
            "NONE",
            "Please enter a prompt before running the analysis.",
            "No cybersecurity tool was executed.",
            "No review required."
        )

    start_time = time.time()

    try:
        result = run_firewall_agent(prompt)

        latency_seconds = time.time() - start_time

        selected_tool = result["selected_tool"]
        decision = result["decision"]
        risk_level = result["risk_level"]
        category = result["category"]
        reason = result["reason"]
        tool_result = result["tool_result"]

        # -------------------------------------------------
        # BUILD SECURITY EVIDENCE
        # -------------------------------------------------

        if selected_tool == "FULL_SECURITY_ANALYSIS":
            rule_result = tool_result["rule_result"]
            llm_result = tool_result["semantic_result"]

            evidence = (
                f"Selected Tool: {selected_tool}\n\n"
                f"--- Rule-Based Classifier ---\n"
                f"Category: {rule_result['category']}\n"
                f"Risk Level: {rule_result['risk_level']}\n"
                f"Decision: {rule_result['decision']}\n"
                f"Reason: {rule_result['reason']}\n\n"
                f"--- Local LLM Classifier ---\n"
                f"Category: {llm_result['category']}\n"
                f"Risk Level: {llm_result['risk_level']}\n"
                f"Decision: {llm_result['decision']}\n"
                f"Reason: {llm_result['reason']}\n\n"
                f"--- Final Firewall Result ---\n"
                f"Final Category: {category}\n"
                f"Final Risk Level: {risk_level}\n"
                f"Final Decision: {decision}\n"
                f"Reason: {reason}\n\n"
                f"Latency: {latency_seconds:.3f} seconds"
            )

        else:
            evidence = (
                f"Selected Tool: {selected_tool}\n\n"
                f"--- Rule-Based Classifier ---\n"
                f"Category: {tool_result['category']}\n"
                f"Risk Level: {tool_result['risk_level']}\n"
                f"Decision: {tool_result['decision']}\n"
                f"Reason: {tool_result['reason']}\n\n"
                f"--- Final Firewall Result ---\n"
                f"Final Category: {category}\n"
                f"Final Risk Level: {risk_level}\n"
                f"Final Decision: {decision}\n"
                f"Reason: {reason}\n\n"
                f"Latency: {latency_seconds:.3f} seconds"
            )

        # -------------------------------------------------
        # POLICY ACTION
        # -------------------------------------------------

        if decision == "ALLOW":
            action_message = (
                "Prompt is considered safe and may continue "
                "to the protected assistant."
            )

            review_message = (
                "Human review is not required for this prompt."
            )

            log_decision(
                prompt=prompt,
                category=category,
                risk_level=risk_level,
                decision=decision,
                action="FORWARD_TO_ASSISTANT",
                selected_tool=selected_tool,
                latency_seconds=latency_seconds,
                error_status="NONE"
            )

        elif decision == "REVIEW":
            action_message = (
                "Prompt requires human review before continuing."
            )

            review_message = (
                "Please use the Approve or Reject button below."
            )

            # We do not log a final human decision yet.
            # That happens after Approve or Reject is clicked.

        else:
            action_message = (
                "Prompt has been blocked by the firewall "
                "and will not reach the protected assistant."
            )

            review_message = (
                "Human review is not required because "
                "the prompt was blocked."
            )

            log_decision(
                prompt=prompt,
                category=category,
                risk_level=risk_level,
                decision=decision,
                action="BLOCK_REQUEST",
                selected_tool=selected_tool,
                latency_seconds=latency_seconds,
                error_status="NONE"
            )

        return (
            decision,
            risk_level,
            selected_tool,
            action_message,
            evidence,
            review_message
        )

    except Exception as error:
        error_latency = time.time() - start_time

        log_decision(
            prompt=prompt,
            category="SYSTEM_ERROR",
            risk_level="MEDIUM",
            decision="REVIEW",
            action="HUMAN_REVIEW_REQUIRED",
            selected_tool="ERROR",
            latency_seconds=error_latency,
            error_status=str(error)
        )

        return (
            "REVIEW",
            "MEDIUM",
            "ERROR",
            "The firewall encountered an error. "
            "The request has been routed to human review.",
            (
                f"System Error: {error}\n\n"
                f"Fail-safe action: REVIEW\n"
                f"Latency: {error_latency:.3f} seconds"
            ),
            "Human review is required because automatic analysis failed."
        )


def approve_review(prompt):
    """
    Human reviewer approves a REVIEW decision.
    """

    if not prompt or not prompt.strip():
        return "No prompt is available for review."

    try:
        review_result = human_review("APPROVE")

        log_decision(
            prompt=prompt,
            category="HUMAN_REVIEW",
            risk_level="MEDIUM",
            decision="REVIEW",
            action="HUMAN_APPROVED",
            selected_tool="HUMAN_REVIEW",
            latency_seconds=0.0,
            error_status="NONE"
        )

        return (
            f"Human Review Decision: APPROVED\n\n"
            f"{review_result}"
        )

    except Exception as error:
        return f"Human review failed: {error}"


def reject_review(prompt):
    """
    Human reviewer rejects a REVIEW decision.
    """

    if not prompt or not prompt.strip():
        return "No prompt is available for review."

    try:
        review_result = human_review("REJECT")

        log_decision(
            prompt=prompt,
            category="HUMAN_REVIEW",
            risk_level="MEDIUM",
            decision="REVIEW",
            action="HUMAN_REJECTED",
            selected_tool="HUMAN_REVIEW",
            latency_seconds=0.0,
            error_status="NONE"
        )

        return (
            f"Human Review Decision: REJECTED\n\n"
            f"{review_result}"
        )

    except Exception as error:
        return f"Human review failed: {error}"


# =========================================================
# GRADIO INTERFACE
# =========================================================

with gr.Blocks(
    title="Prompt Injection Detection and LLM Firewall Agent"
) as demo:

    gr.Markdown(
        """
        # 🛡️ Prompt Injection Detection and LLM Firewall Agent

        This defensive cybersecurity system analyzes user prompts
        before they reach a protected AI assistant.

        The AI firewall agent selects an appropriate cybersecurity tool,
        analyzes the request, evaluates its risk, and produces one of
        three decisions:

        **ALLOW → REVIEW → BLOCK**
        """
    )

    # -----------------------------------------------------
    # INPUT
    # -----------------------------------------------------

    gr.Markdown("## 1. Submit a Prompt")

    prompt_box = gr.Textbox(
        label="User Prompt",
        placeholder="Enter a prompt for security analysis...",
        lines=5
    )

    analyze_button = gr.Button(
        "Analyze Prompt",
        variant="primary"
    )

    # -----------------------------------------------------
    # FIREWALL RESULT
    # -----------------------------------------------------

    gr.Markdown("## 2. Firewall Analysis")

    with gr.Row():

        decision_output = gr.Textbox(
            label="Final Decision",
            interactive=False
        )

        risk_output = gr.Textbox(
            label="Risk Level",
            interactive=False
        )

        tool_output = gr.Textbox(
            label="Selected Tool",
            interactive=False
        )

    message_output = gr.Textbox(
        label="Policy Action",
        lines=2,
        interactive=False
    )

    evidence_output = gr.Textbox(
        label="Security Evidence",
        lines=14,
        interactive=False
    )

    # -----------------------------------------------------
    # HUMAN REVIEW
    # -----------------------------------------------------

    gr.Markdown(
        """
        ## 3. Human-in-the-Loop Review

        Prompts classified as **REVIEW** require human approval
        before they may continue.
        """
    )

    review_status = gr.Textbox(
        label="Review Status",
        interactive=False
    )

    with gr.Row():

        approve_button = gr.Button(
            "Approve",
            variant="secondary"
        )

        reject_button = gr.Button(
            "Reject",
            variant="stop"
        )

    review_output = gr.Textbox(
        label="Human Review Result",
        lines=4,
        interactive=False
    )

    # -----------------------------------------------------
    # EVENT HANDLERS
    # -----------------------------------------------------

    analyze_button.click(
        fn=analyze_prompt,
        inputs=prompt_box,
        outputs=[
            decision_output,
            risk_output,
            tool_output,
            message_output,
            evidence_output,
            review_status
        ]
    )

    approve_button.click(
        fn=approve_review,
        inputs=prompt_box,
        outputs=review_output
    )

    reject_button.click(
        fn=reject_review,
        inputs=prompt_box,
        outputs=review_output
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    demo.launch()