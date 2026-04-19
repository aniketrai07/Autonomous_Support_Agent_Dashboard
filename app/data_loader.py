import json
import re

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# 🔥 Extract order ID from text like "ORD-1001"
def extract_order_id(text):
    if not text:
        return None
    match = re.search(r"ORD-\d+", text)
    return match.group(0) if match else None


def normalize_ticket(ticket):
    # combine subject + body for better context
    text = (ticket.get("subject") or "") + " " + (ticket.get("body") or "")

    return {
        "id": ticket.get("ticket_id") or ticket.get("id"),
        "order_id": extract_order_id(text),   # 🔥 key fix
        "message": text,
        "email": ticket.get("customer_email"),
        "raw": ticket
    }


def load_tickets():
    raw_tickets = load_json("app/data/tickets.json")

    normalized = []
    for t in raw_tickets:
        nt = normalize_ticket(t)

        if not nt["id"]:
            print("⚠️ Skipping invalid ticket:", t)
            continue

        normalized.append(nt)

    print(f"✅ Loaded {len(normalized)} valid tickets")
    print("🔍 Sample:", normalized[:2])

    return normalized