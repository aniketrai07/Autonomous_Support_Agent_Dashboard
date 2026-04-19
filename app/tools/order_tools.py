import json

def get_order(order_id):
    try:
        with open("app/data/orders.json", encoding="utf-8") as f:
            orders = json.load(f)

        # 🔥 FIX: check both id and order_id
        return next(
            (
                o for o in orders
                if o.get("id") == order_id or o.get("order_id") == order_id
            ),
            {"error": "Order not found"}
        )

    except Exception as e:
        return {"error": str(e)}

import random

def check_refund(order_id):
    if random.random() < 0.2:
        raise Exception("Simulated timeout")

    return {
        "eligible": True,
        "reason": "Within return window"
    }