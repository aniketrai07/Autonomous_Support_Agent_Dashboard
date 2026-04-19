class TicketState:
    def __init__(self, ticket):
        self.ticket = ticket
        self.history = []
        self.resolved = False
        self.confidence = 1.0

    def update(self, action, result):
        self.history.append({
            "action": action,
            "result": result
        })

        # confidence drops if error
        if isinstance(result, dict) and "error" in result:
            self.confidence -= 0.3

        # mark resolved
        if action.get("tool") == "send_reply":
            self.resolved = True