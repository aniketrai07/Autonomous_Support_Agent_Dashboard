def plan_action(state):
    ticket = state.ticket
    msg = ticket.get("message", "").lower()
    history = state.history

    used = lambda tool: any(h["action"]["tool"] == tool for h in history)

    # ✅ Case 1: Missing order ID
    if not ticket.get("order_id"):
        if not used("send_reply"):
            return {
                "tool": "send_reply",
                "args": {
                    "ticket_id": ticket["id"],
                    "message": "Could you please provide your order ID so I can assist you?"
                }
            }

    # ✅ Step 1: Get order details
    if not used("get_order"):
        return {
            "tool": "get_order",
            "args": {"order_id": ticket["order_id"]}
        }

    last_result = history[-1]["result"] if history else {}

    # ❌ Order not found
    if last_result.get("error") == "Order not found":
        if not used("send_reply"):
            return {
                "tool": "send_reply",
                "args": {
                    "ticket_id": ticket["id"],
                    "message": "We could not find your order. Please check your order ID and try again."
                }
            }

    # 🔥 Priority 1: Escalation (replacement/warranty)
    if "replacement" in msg or "warranty" in msg:
        if not used("escalate"):
            return {
                "tool": "escalate",
                "args": {
                    "ticket_id": ticket["id"],
                    "summary": "Warranty/replacement request",
                    "priority": "high"
                }
            }

    # 💰 Priority 2: Refund flow
    if "refund" in msg or "damaged" in msg:
        if not used("check_refund"):
            return {
                "tool": "check_refund",
                "args": {"order_id": ticket["order_id"]}
            }

        if not used("issue_refund"):
            return {
                "tool": "issue_refund",
                "args": {
                    "order_id": ticket["order_id"],
                    "amount": 100
                }
            }

    # 🧠 Low confidence escalation
    if state.confidence < 0.6 and not used("escalate"):
        return {
            "tool": "escalate",
            "args": {
                "ticket_id": ticket["id"],
                "summary": "Low confidence case",
                "priority": "high"
            }
        }

    # ✅ FINAL RESPONSE (CORRECT PRIORITY HANDLING)
    if not used("send_reply"):

        # 🔥 Highest priority: refund confirmation
        if used("issue_refund"):
            message = "Your refund has been successfully processed. It will reflect within 5–7 business days."

        # 🔥 Next: escalation message
        elif used("escalate"):
            message = "Your request has been escalated to our specialist team. They will contact you shortly."

        # 📜 Policy / return questions
        elif "policy" in msg or "return" in msg:
            message = "Our return policy allows returns within 30 days for most products."

        # ❓ Missing order ID fallback
        elif not ticket.get("order_id"):
            message = "Could you please provide your order ID so I can assist you?"

        # ✅ Default
        else:
            message = "Your request has been processed successfully."

        return {
            "tool": "send_reply",
            "args": {
                "ticket_id": ticket["id"],
                "message": message
            }
        }

    return {"tool": "noop", "args": {}}