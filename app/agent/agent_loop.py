from app.data_loader import load_tickets
from app.agent.state import TicketState
from app.agent.planner import plan_action
from app.agent.executor import execute_action
from app.utils.logger import log_audit, log_failure
from app.utils.concurrency import run_parallel


def process_ticket(ticket):
    print(f"\n📩 Processing Ticket: {ticket.get('id')}")

    state = TicketState(ticket)

    for step in range(5):
        action = plan_action(state)

        if action.get("tool") == "noop":
            break

        reason = f"Agent chose '{action['tool']}' based on context"

        print(f"➡️ Step {step+1}: {action}")
        print(f"🧠 Reason: {reason}")

        result = execute_action(action, state)
        print(f"✅ Result: {result}")

        # ✅ ADD HERE (correct place)
        print(f"🧠 Confidence Score: {state.confidence}")

        state.history.append({
            "action": action,
            "result": result,
            "reason": reason
        })

        if isinstance(result, dict) and "error" in result:
            state.confidence -= 0.3

        if action.get("tool") == "send_reply":
            state.resolved = True
            print("🎉 Ticket Resolved")
            break

    if not state.resolved:
        log_failure(ticket)

    log_audit(state)

def process_all_tickets():
    tickets = load_tickets()
    print(f"🚀 Total Tickets: {len(tickets)}")

    run_parallel(process_ticket, tickets)
