import streamlit as st
from app import run_crypto_agent

st.set_page_config(page_title="CryptoCoins CrewAI Agent", page_icon="💰", layout="centered")

st.title("💰 CryptoCoins CrewAI Agent")
st.markdown("Ask about any cryptocurrency to get live insights powered by CrewAI, Serper, and Langfuse.")

query = st.text_input("🔍 Enter your query (e.g., Bitcoin, Ethereum, Solana):")

if st.button("Run Agent"):
    if query.strip():
        with st.spinner("Running the Crypto Agent..."):
            try:
                result = run_crypto_agent(query, user_id="streamlit_user")
                st.success("✅ Agent Response:")
                st.write(result)
            except Exception as e:
                st.error(f"⚠️ Error running the agent: {e}")
    else:
        st.warning("Please enter a valid query.")
