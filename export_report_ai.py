import streamlit as st
import urllib.parse
import json
import ast

st.set_page_config(page_title="Accessibility Report", layout="centered")
st.title("📤 Export Accessibility Simulation Report")

# ---- Extract Query Parameters ----
query_params = st.query_params

# Decode and sanitize URL parameters
persona = urllib.parse.unquote(query_params.get("persona", "Unknown"))
issues_param = urllib.parse.unquote(query_params.get("issues", "[]"))
answers_param = urllib.parse.unquote(query_params.get("ai_answers", "[]"))
note = urllib.parse.unquote(query_params.get("note", ""))
include_summary = query_params.get("include_summary", "false") == "true"

# Safely evaluate list values
try:
    issues = ast.literal_eval(issues_param)
except:
    issues = []

try:
    ai_answers = ast.literal_eval(answers_param)
except:
    ai_answers = []

# ---- Render Report ----
st.markdown(f"### 👤 Persona: `{persona}`")

st.markdown("### ⚠️ Detected Issues:")
if issues:
    st.markdown("<ul>" + "".join([f"<li>{i}</li>" for i in issues]) + "</ul>", unsafe_allow_html=True)
else:
    st.info("No issues provided.")

st.markdown("### 🤖 AI Explanation History:")
if ai_answers:
    for i, message in enumerate(ai_answers, 1):
        role = message.get("role", "assistant")
        content = message.get("content", "")
        label = "🧑‍💬 You:" if role == "user" else "🤖 AI:"
        st.markdown(f"**{label}** {content}")
else:
    st.warning("No AI explanation history available.")

st.markdown("### 📝 Additional Note:")
if note:
    st.code(note)
else:
    st.text("No additional notes.")

# ---- Export Options ----
st.markdown("---")
st.success("✅ Ready to export your report.")
st.button("📥 Download PDF (coming soon)", disabled=True)
st.button("📧 Email Report (coming soon)", disabled=True)
