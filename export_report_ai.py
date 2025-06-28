import streamlit as st

# Page config
st.set_page_config(page_title="Review Simulation Summary", layout="centered")
st.title("🧠 Simulation Summary Review")

# Retrieve simulation results
persona = st.session_state.get("selected_persona", "Unknown")
ai_answers = st.session_state.get("ai_answers", [])
issues = st.session_state.get("issue_labels", [])  # You can store this in earlier pages

# Summary Preview Box
st.markdown(f"### 👤 Persona: `{persona}`")
st.markdown("### ⚠️ Issues Found:")
if issues:
    st.markdown("<ul>" + "".join([f"<li>{issue}</li>" for issue in issues]) + "</ul>", unsafe_allow_html=True)
else:
    st.info("No issues found.")

# Show AI Answer History
st.markdown("### 📘 AI Explanations:")
if ai_answers:
    for i, ans in enumerate(ai_answers, 1):
        st.markdown(f"**{i}. {ans['rule']}** — *{ans['persona']}*")
        st.markdown(ans['content'], unsafe_allow_html=True)
else:
    st.warning("No AI explanations yet.")

# Text Note from user
user_note = st.text_area("✏️ Add a message to include in your report")

# Save everything on confirm
if st.button("✅ Confirm & Go to Export Report"):
    st.session_state["final_report"] = {
        "persona": persona,
        "note": user_note,
        "issues": issues,
        "ai_answers": ai_answers,
    }
    st.success("Report summary saved! Redirecting...")
    st.markdown("""<meta http-equiv="refresh" content="1;URL=Export_Report">""", unsafe_allow_html=True)
