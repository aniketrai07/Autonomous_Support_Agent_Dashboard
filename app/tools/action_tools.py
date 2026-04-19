def issue_refund(order_id, amount):
    return {
        "status": "success",
        "message": f"Refund of {amount} issued for order {order_id}"
    }

def send_reply(ticket_id, message):
    return {
        "status": "sent",
        "ticket_id": ticket_id,
        "message": message
    }

def escalate(ticket_id, summary="Escalated", priority="high"):
    return {
        "status": "escalated",
        "ticket_id": ticket_id,
        "priority": priority
    }