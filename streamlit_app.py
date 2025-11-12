from app import run_crypto_agent
import msal
from urllib.parse import urlencode
import streamlit as st
from langfuse import Langfuse
import os


st.set_page_config(page_title="CryptoCoins CrewAI Agent", page_icon="💰", layout="centered")

# # --- Mock user for local testing ---
# import os
# import streamlit as st

# if os.getenv("LOCAL_TEST", "false").lower() == "true":
#     st.session_state.user = {
#         "name": "Sanika Test",
#         "preferred_username": "sanika.test1@stevens.edu"
#     }
#     st.session_state.access_token = "dummy-token"
#     st.success("✅ Running in local mock mode — user simulated.")

st.title("💰 CryptoCoins CrewAI Agent")
st.markdown("Ask about any cryptocurrency to get live insights powered by CrewAI, Serper, and Langfuse.")

query = st.text_input("🔍 Enter your query (e.g., Bitcoin, Ethereum, Solana):")

if st.button("Run Agent"):
    if query.strip():
        with st.spinner("Running the Crypto Agent..."):
            try:
                user_email = st.session_state.user.get("preferred_username") if st.session_state.user else "local_user"
                user_name = st.session_state.user.get("name") if st.session_state.user else "Local Test User"

                result = run_crypto_agent(query, user_id=user_email)

                st.success("✅ Agent Response:")
                st.write(result)
            except Exception as e:
                st.error(f"⚠️ Error running the agent: {e}")
    else:
        st.warning("Please enter a valid query.")
