import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Accessibility Chatbot", layout="centered")
st.title("💬 Accessibility Chatbot")
st.markdown("Ask anything about digital accessibility, WCAG rules, or inclusive design!")

# Initialize chat history
if "access_chat_history" not in st.session_state:
    st.session_state.access_chat_history = [
        {"role": "system", "content": "You are an accessibility assistant. Be friendly, use simple examples, and answer in no more than **5 sentences** or **2 short paragraphs** unless asked otherwise."}
    ]

# Display all messages in sequence
for msg in st.session_state.access_chat_history[1:]:  # skip system message
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Input at the bottom of the chat
user_input = st.chat_input("Type your accessibility question...")

if user_input:
    # Show user message immediately
    st.chat_message("user").markdown(user_input)
    st.session_state.access_chat_history.append({"role": "user", "content": user_input})

    # Generate assistant reply
    response = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.access_chat_history
    )
    reply = response.choices[0].message.content
    st.session_state.access_chat_history.append({"role": "assistant", "content": reply})

    # Show assistant message immediately
    st.chat_message("assistant").markdown(reply)
