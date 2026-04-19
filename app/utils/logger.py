import json
import os

os.makedirs("outputs", exist_ok=True)

def log_audit(state):
    try:
        with open("outputs/audit_log.json", "a", encoding="utf-8") as f:
            json.dump({
                "ticket_id": state.ticket.get("id"),
                "history": state.history,
                "confidence": getattr(state, "confidence", 1.0)
            }, f)
            f.write("\n")
    except Exception as e:
        print("⚠️ Logging error:", e)


def log_failure(ticket):
    with open("outputs/failed_tickets.json", "a", encoding="utf-8") as f:
        json.dump(ticket, f)
        f.write("\n")