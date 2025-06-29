import streamlit as st
import urllib.parse
import ast

st.set_page_config(page_title="Accessibility Report", layout="centered")
st.title("📤 Export Accessibility Simulation Report")

# ---- URL Parameter Parsing ----
query_params = st.query_params

# Decode and sanitize
persona = urllib.parse.unquote(query_params.get("persona", "Unknown"))
issues_param = urllib.parse.unquote(query_params.get("issues", "[]"))
answers_param = urllib.parse.unquote(query_params.get("ai_answers", "[]"))
note = urllib.parse.unquote(query_params.get("note", ""))
include_summary = query_params.get("include_summary", "false") == "true"

# Safely evaluate lists
try:
    issues = ast.literal_eval(issues_param)
except:
    issues = []

try:
    ai_answers = ast.literal_eval(answers_param)
except:
    ai_answers = []

# ---- Display Report Content ----
st.markdown(f"### 👤 Persona: `{persona}`")

st.markdown("### ⚠️ Issues Detected:")
if issues:
    st.markdown("<ul>" + "".join([f"<li>{i}</li>" for i in issues]) + "</ul>", unsafe_allow_html=True)
else:
    st.info("No issues were provided.")

st.markdown("### 📘 AI Explanations:")
if ai_answers:
    for i, answer in enumerate(ai_answers, 1):
        st.markdown(f"**{i}.** {answer}", unsafe_allow_html=True)
else:
    st.warning("No AI explanations were included.")

if note:
    st.markdown("### ✏️ Additional Note:")
    st.code(note)
else:
    st.markdown("### ✏️ No additional notes.")

# Optional PDF + Email buttons
st.markdown("---")
st.success("✅ Ready to export your report.")
st.button("📥 Download PDF (coming soon)", disabled=True)
st.button("📧 Email Report (coming soon)", disabled=True)
