import streamlit as st

# Page configuration
st.set_page_config(page_title="Export Accessibility Simulation Report", layout="centered")

st.title("📄 Export Accessibility Simulation Report")

# Retrieve session data
persona = st.session_state.get("selected_persona", "Unknown")
ai_answers = st.session_state.get("ai_answers", [])
improvements_made = st.session_state.get("improvements_made", 0)

# Summary block
st.markdown(f"""
**Persona:** {persona}  
**{len(ai_answers)}** issues found  
**{improvements_made}** improvements made  
""")

# User note
user_note = st.text_area("✏️ Write your message here to add to your report")

# Checkbox for summary inclusion
include_summary = st.checkbox("Include AI Summary in Report", value=True)

# Show AI explanations
if include_summary and ai_answers:
    st.subheader("🧠 AI-Generated Explanations")
    for i, ans in enumerate(ai_answers, start=1):
        st.markdown(f"### {i}. {ans['rule']} ({ans['persona']})")
        st.markdown(ans['content'], unsafe_allow_html=True)

# Save all info for export
report_content = {
    "persona": persona,
    "note": user_note,
    "ai_answers": ai_answers if include_summary else [],
    "improvements_made": improvements_made
}
st.session_state["final_report"] = report_content

# Action buttons
st.markdown("### What would you like to do?")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("📥 Download PDF", key="download_pdf_btn")
with col2:
    st.button("📧 Email Report", key="email_report_btn")
with col3:
    st.button("🔁 Run Another Simulation", key="run_simulation_btn")

# Footer
st.markdown("🔍 [Preview report before sending](#)", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:gray; margin-top:2rem'>
    No personal data is stored or shared
</div>
""", unsafe_allow_html=True)
