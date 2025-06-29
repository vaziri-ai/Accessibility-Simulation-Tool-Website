import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
import urllib.parse
import json

# --- Setup OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Get Query Parameters ---
query_params = st.query_params
persona_param = query_params.get("persona", "")
rule_param = query_params.get("rule", "")

# --- Define WCAG rules and personas ---
personas = [
    "Low Literacy – Age 65+",
    "Cognitive Load",
    "Visual Impairment",
    "Autism Spectrum",
    "Motor Impairment",
    "Non-Native Speakers"
]

wcag_rules = [
    {"id": "1.1.1", "title": "Non-text Content", "description": "Provide text alternatives for any non-text content.", "personas": "visual impairment, cognitive load challenges"},
    {"id": "1.2.1", "title": "Audio-only and Video-only", "description": "Provide alternatives for audio-only and video-only content.", "personas": "visual impairment, older adults with declining digital skills"},
    {"id": "1.2.2", "title": "Captions (Prerecorded)", "description": "Provide captions for prerecorded audio.", "personas": "non-native language speakers, hearing impairment"},
    {"id": "1.3.1", "title": "Info and Relationships", "description": "Ensure information and relationships can be determined programmatically.", "personas": "low literacy, cognitive load challenges"},
    {"id": "1.3.2", "title": "Meaningful Sequence", "description": "Content must be in a meaningful order.", "personas": "cognitive load challenges, older adults with declining digital skills"},
    {"id": "2.4.6", "title": "Headings and Labels", "description": "Headings and labels must describe topic or purpose.", "personas": "cognitive load"},
    {"id": "3.2.4", "title": "Consistent Identification", "description": "Components with same function are identified consistently.", "personas": "cognitive load, autism spectrum"},
    {"id": "2.5.5", "title": "Target Size", "description": "Touch targets should be at least 44 by 44 CSS pixels.", "personas": "visual impairment, motor impairment"},
    {"id": "2.4.7", "title": "Focus Visible", "description": "Keyboard focus should be clearly visible.", "personas": "motor impairment"},
    {"id": "3.1.5", "title": "Reading Level", "description": "Use language that requires lower than upper secondary education.", "personas": "low literacy, non-native speakers"},
]

# --- LLM Prompt Builder ---
def generate_why_this_matters(rule_title, rule_description, persona):
    prompt = f"""
Accessibility Rule: {rule_title}
Description: {rule_description}

This issue affects {persona}. Please explain why this accessibility issue matters for them in plain language.
Use a helpful, gentle tone. Keep the explanation short, and use a maximum of 3 sentences.
Avoid jargon, and speak as if guiding a non-technical healthcare staff member using an accessibility simulation tool for the first time.
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an accessibility assistant helping explain accessibility barriers to non-technical healthcare professionals."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- UI Start ---
st.set_page_config(page_title="Accessibility Explainer", layout="centered")
st.title("🧠 Why This Matters")

# --- Explanation Block ---
if persona_param and rule_param:
    st.markdown(f"**Persona:** {persona_param}<br>**Issue:** {rule_param}", unsafe_allow_html=True)

    selected_rule = next(
        (rule for rule in wcag_rules if rule["id"] in rule_param or rule["title"].lower() in rule_param.lower()),
        None
    )

    if selected_rule:
        rule_description = selected_rule["description"]
        rule_title = selected_rule["title"]
        explanation = generate_why_this_matters(rule_title, rule_description, persona_param)
        st.write("### Why this Matters:")
        st.write(explanation)
    else:
        st.warning("⚠️ WCAG rule not found. Please check the rule parameter in the URL.")
else:
    st.warning("Missing query parameters: `persona` or `rule`.")

# --- Chat Assistant Section ---
st.markdown("---")
st.subheader("💬 Ask a Follow-up Question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an accessibility assistant for non-technical healthcare teams. Help explain WCAG rules clearly and give short, working code examples (e.g. HTML, CSS, ARIA, JS) to fix the problem. Be gentle and helpful."}
    ]

if "ai_answers" not in st.session_state:
    st.session_state.ai_answers = []

user_input = st.text_input("Type your question here:")

if st.button("Send") and user_input:
    context = ""
    if selected_rule:
        context = f"""
The user is asking a follow-up question based on this WCAG rule:

Persona: {persona_param}
Rule Title: {selected_rule['title']}
Description: {selected_rule['description']}

Please include a small and simple code example (HTML/CSS/ARIA or JavaScript) that addresses this accessibility rule.
"""
    message = context + "\n\n" + user_input if context else user_input
    st.session_state.chat_history.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=st.session_state.chat_history
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.ai_answers.append(reply)

    st.markdown("### 👩‍⚕️ Assistant's Answer")
    st.write(reply)

# Save AI answers to sessionStorage for access via HTML link
import json
components.html(f"""
<script>
    sessionStorage.setItem("ai_answers", {json.dumps(st.session_state.ai_answers)});
</script>
""", height=0)
# Before redirecting to preview/export
ai_answers = json.dumps(st.session_state.chat_history)
encoded_ai = urllib.parse.quote(ai_answers)

export_url = f"https://accessibility-simulation-tool-website-export-report-ai.streamlit.app/?persona={persona}&issues={encoded_issues}&ai_answers={encoded_ai}&note={encoded_note}"
st.markdown(f"[🔍 Preview report before sending]({export_url})")
