import streamlit as st
from agent import SalesProposalAgent

st.set_page_config(page_title="Copilot Sales Agent", layout="wide")
st.title("Microsoft 365 Copilot — Sales Proposal Agent")

if "agent" not in st.session_state:
    st.session_state.agent = SalesProposalAgent()

agent = st.session_state.agent

user_input = st.chat_input("Create or revise a proposal")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    # If proposal already exists, treat input as revision
    if agent.state.get("proposal_text"):
        revised = agent.revise_proposal(user_input)

        with st.chat_message("assistant"):
            if revised:
                st.success("Proposal updated based on your feedback.")
            else:
                st.write("No proposal found to revise.")

    else:
        analysis = agent.analyze_request(user_input)
        crm_info, meeting_info = agent.gather_context()
        proposal = agent.generate_proposal(crm_info, meeting_info)

    actions = agent.plan_actions()

    with st.chat_message("assistant"):
        st.subheader("Agent Activity Log")
        for action in actions:
            st.write(f"- {action}")

        if agent.state.get("proposal_text"):
            st.subheader("Current Proposal Draft")
            st.text(agent.state["proposal_text"])

# Approval buttons
st.divider()
st.subheader("Simulate Internal Approvals")

col1, col2 = st.columns(2)

with col1:
    if st.button("Approve Finance"):
        agent.approve("finance")
        st.success("Finance approval granted.")

with col2:
    if st.button("Approve Sales Manager"):
        agent.approve("sales_manager")
        st.success("Sales Manager approval granted.")
