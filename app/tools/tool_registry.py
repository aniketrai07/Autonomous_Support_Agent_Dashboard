from app.tools.order_tools import get_order
from app.tools.customer_tools import get_customer
from app.tools.action_tools import issue_refund, send_reply, escalate
from app.tools.order_tools import get_order, check_refund

TOOLS = {
    "get_order": get_order,
    "check_refund": check_refund,
    "issue_refund": issue_refund,
    "send_reply": send_reply,
    "escalate": escalate
}