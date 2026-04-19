from app.tools.tool_registry import TOOLS
import time

def safe_tool_call(func, **kwargs):
    for i in range(3):
        try:
            return func(**kwargs)
        except Exception as e:
            print(f"⚠️ Retry {i+1} due to error: {e}")
            time.sleep(1)
    return {"error": "Tool failed after retries"}


def execute_action(action, state):
    tool_name = action.get("tool")
    args = action.get("args", {})

    print("🔧 Executing:", tool_name, args)

    if tool_name in TOOLS:
        return safe_tool_call(TOOLS[tool_name], **args)

    return {"error": "Unknown tool"}