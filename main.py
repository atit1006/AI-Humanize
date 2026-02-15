import streamlit as st
import google.generativeai as genai
import requests
import os

# --- CONFIGURATION & API SETUP ---
st.set_page_config(
    page_title="HumanizeAI | Professional Text Refiner",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fetching keys from Streamlit Secrets (The secure way)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    SAPLING_API_KEY = st.secrets["SAPLING_API_KEY"]
except:
    st.error("API Keys not found! Please add them to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# --- CUSTOM CSS (Tailwind + Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    .stApp {
        background-color: #0a0a0a;
        color: #f5f5f5;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 1.5rem;
        min-height: 500px;
        display: flex;
        flex-direction: column;
    }

    .gradient-text {
        background: linear-gradient(135deg, #fff 0%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3.5rem;
        line-height: 1.2;
        text-align: center;
        margin-bottom: 1rem;
    }

    .stTextArea textarea {
        background-color: transparent !important;
        color: #e4e4e7 !important;
        border: none !important;
        font-size: 1rem !important;
    }

    .stButton button {
        background: white !important;
        color: black !important;
        font-weight: 700 !important;
        border-radius: 9999px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
    }

    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'humanized_output' not in st.session_state:
    st.session_state.humanized_output = ""
if 'detection_result' not in st.session_state:
    st.session_state.detection_result = None

# --- LINGUISTIC ENGINES ---
def humanize_text(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Changed to a valid model name
        prompt = (
            "Humanize this AI text. Use natural flow, varying sentence lengths, "
            "and avoid words like 'delve' or 'tapestry'. Keep meaning identical: " + text
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def detect_ai_sapling(text):
    url = "https://api.sapling.ai/api/v1/aidetector"
    payload = {"key": SAPLING_API_KEY, "text": text}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        score = data.get("score", 0) * 100
        label = "AI-Generated" if score > 70 else "Mixed/Unknown" if score > 30 else "Human Written"
        return {"score": round(score, 1), "label": label}
    except Exception as e:
        return None

# --- UI COMPONENTS ---
st.markdown("""
    <div class="nav-container">
        <div style="font-weight:800; font-size:1.5rem;">✍️ Humanize<span style="color:#6366f1;">AI</span></div>
        <div style="color:#71717a;">v4.0 Professional</div>
    </div>
""", unsafe_allow_html=True)

mode = st.radio("Select Tool", ["Humanizer", "AI Detector"], horizontal=True, label_visibility="collapsed")

if mode == "Humanizer":
    st.markdown('<h1 class="gradient-text">Refine AI into<br>Pure Human Voice</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        user_input = st.text_area("input", placeholder="Paste AI content here...", height=350, label_visibility="collapsed")
        if st.button("Humanize Content"):
            st.session_state.humanized_output = humanize_text(user_input)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.session_state.humanized_output:
            st.write(st.session_state.humanized_output)
            st.download_button("Download", st.session_state.humanized_output)
        else:
            st.write("Result will appear here...")
        st.markdown('</div>', unsafe_allow_html=True)

elif mode == "AI Detector":
    st.markdown('<h1 class="gradient-text">Expose the<br>Silicon Patterns</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        detect_input = st.text_area("detect", placeholder="Paste text to analyze...", height=350, label_visibility="collapsed")
        if st.button("Detect AI Presence"):
            st.session_state.detection_result = detect_ai_sapling(detect_input)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.session_state.detection_result:
            res = st.session_state.detection_result
            st.metric("Probability of AI", f"{res['score']}%")
            st.subheader(f"Result: {res['label']}")
        else:
            st.write("Scan result will appear here...")
        st.markdown('</div>', unsafe_allow_html=True)
