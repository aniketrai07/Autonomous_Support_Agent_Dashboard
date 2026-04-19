import streamlit as st
from app.agent.state import TicketState
from app.agent.planner import plan_action
from app.agent.executor import execute_action

# 🎨 Page config
st.set_page_config(page_title="AI Support Agent", layout="wide")

# 🎨 Custom CSS (premium look)
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.stTextInput input, .stTextArea textarea {
    background-color: #1e1e2f;
    color: white;
    border-radius: 10px;
}
.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #00c6ff);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
.card {
    background-color: #1e1e2f;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.step {
    border-left: 4px solid #00c6ff;
    padding-left: 10px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Title
st.title("🤖 Autonomous Support Agent")
st.markdown("AI-powered multi-step reasoning system")

# 🎯 Layout
col1, col2 = st.columns([1, 2])

# 🧾 LEFT SIDE — INPUT
with col1:
    st.subheader("📩 Ticket Input")

    ticket_id = st.text_input("Ticket ID", "TKT-001")
    order_id = st.text_input("Order ID", "ORD-1001")
    message = st.text_area("Message", "I received a damaged product and want a refund.")

    run = st.button("🚀 Run Agent")

# 🧠 RIGHT SIDE — OUTPUT
with col2:
    st.subheader("🧠 Agent Execution")

    if run:
        ticket = {
            "id": ticket_id,
            "order_id": order_id,
            "message": message
        }

        state = TicketState(ticket)

        # 💬 User message (chat style)
        st.markdown(f"""
        <div class="card">
        👤 <b>User:</b> {message}
        </div>
        """, unsafe_allow_html=True)

        for step in range(5):
            action = plan_action(state)

            if action.get("tool") == "noop":
                break

            result = execute_action(action, state)

            # 🧠 Step card
            st.markdown(f"""
            <div class="card step">
            <b>Step {step+1}</b><br>
            🔧 <b>Action:</b> {action['tool']}<br>
            📥 <b>Input:</b> {action['args']}<br>
            📤 <b>Output:</b> {result}
            </div>
            """, unsafe_allow_html=True)

            # 🧠 Confidence badge
            st.markdown(f"""
            <div style="color:#00c6ff;">
            🧠 Confidence: {round(state.confidence,2)}
            </div>
            """, unsafe_allow_html=True)

            state.history.append({
                "action": action,
                "result": result
            })

            if action.get("tool") == "send_reply":
                st.success("🎉 Ticket Resolved")

                # 💬 Final reply
                st.markdown(f"""
                <div class="card">
                🤖 <b>Agent:</b> {action['args']['message']}
                </div>
                """, unsafe_allow_html=True)

                break