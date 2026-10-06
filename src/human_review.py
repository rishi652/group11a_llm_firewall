def human_review(decision):

    if decision == "APPROVE":
        return {
            "review_status": "APPROVED",
            "final_action": "FORWARD_TO_ASSISTANT",
            "message": "Human reviewer approved the request."
        }

    elif decision == "REJECT":
        return {
            "review_status": "REJECTED",
            "final_action": "BLOCK_REQUEST",
            "message": "Human reviewer rejected the request."
        }

    else:
        return {
            "review_status": "PENDING",
            "final_action": "WAIT_FOR_HUMAN_REVIEW",
            "message": "A valid human decision has not yet been provided."
        }