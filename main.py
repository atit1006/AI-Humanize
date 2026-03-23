import os
import re
from typing import Optional

import google.generativeai as genai
import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Royal Humanize AI | Premium Text Refinery",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Cormorant+Garamond:wght@500;600;700&display=swap');

        :root {
            --bg: #0f0820;
            --bg-soft: #1b1036;
            --panel: rgba(23, 16, 48, 0.82);
            --panel-strong: rgba(34, 23, 70, 0.95);
            --border: rgba(202, 178, 255, 0.18);
            --text: #f8f4ff;
            --muted: #cbbde7;
            --gold: #f4d58d;
            --gold-strong: #d4a94f;
            --violet: #8a63ff;
            --orchid: #c084fc;
            --rose: #f472b6;
            --success: #7be0b3;
            --danger: #ff8f8f;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(192,132,252,0.22), transparent 28%),
                radial-gradient(circle at top right, rgba(244,213,141,0.15), transparent 24%),
                linear-gradient(180deg, #0a0615 0%, #120a24 45%, #090511 100%);
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(19, 12, 39, 0.95), rgba(10, 6, 21, 0.98));
            border-right: 1px solid rgba(202, 178, 255, 0.12);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .royal-shell {
            padding: 0.75rem 0 1.5rem 0;
        }

        .hero-card,
        .glass-card,
        .metric-card,
        .info-card {
            background: var(--panel);
            border: 1px solid var(--border);
            box-shadow: 0 20px 70px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(18px);
            border-radius: 24px;
        }

        .hero-card {
            padding: 1.75rem 1.75rem 1.25rem 1.75rem;
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, rgba(28,18,58,0.94), rgba(15,9,30,0.88));
        }

        .glass-card {
            min-height: 520px;
            padding: 1.3rem;
        }

        .info-card {
            padding: 1rem 1.2rem;
            margin-top: 1rem;
        }

        .brand-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(202, 178, 255, 0.12);
            padding-bottom: 1rem;
        }

        .brand-mark {
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .brand-mark span {
            color: var(--gold);
        }

        .brand-badge {
            font-size: 0.82rem;
            color: var(--gold);
            border: 1px solid rgba(244,213,141,0.22);
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(244,213,141,0.08);
        }

        .hero-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 4rem;
            line-height: 0.95;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(135deg, #fff7e8 0%, #f4d58d 42%, #d6c3ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: var(--muted);
            font-size: 1.04rem;
            margin-top: 0.8rem;
            max-width: 54rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 1rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(244,213,141,0.18);
            background: rgba(244,213,141,0.08);
            color: #fff5d7;
            font-size: 0.92rem;
        }

        .section-label {
            color: #efe7ff;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 0.55rem;
        }

        .helper-text {
            color: var(--muted);
            font-size: 0.92rem;
            margin-bottom: 0.8rem;
        }

        .stTextArea textarea {
            background: rgba(12, 8, 24, 0.92) !important;
            color: var(--text) !important;
            border: 1px solid rgba(202, 178, 255, 0.14) !important;
            border-radius: 18px !important;
            font-size: 1rem !important;
            min-height: 560px !important;
            min-height: 330px !important;
        }

        .stTextInput input {
            background: rgba(12, 8, 24, 0.92) !important;
            color: var(--text) !important;
            border-radius: 14px !important;
        }

        .stButton button,
        .stDownloadButton button {
            width: 100% !important;
            border-radius: 999px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.85rem 1.2rem !important;
            background: linear-gradient(135deg, #f4d58d, #c084fc) !important;
            color: #1d1237 !important;
            box-shadow: 0 10px 30px rgba(192, 132, 252, 0.22) !important;
        }

        .stRadio [role="radiogroup"] {
            gap: 0.75rem;
        }

        .metric-card {
            padding: 1rem 1.15rem;
            margin-bottom: 0.9rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.86rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            color: var(--gold);
            font-size: 1.45rem;
            font-weight: 800;
            margin-top: 0.15rem;
        }

        .result-box {
            border-radius: 18px;
            padding: 1rem;
            background: rgba(10, 6, 21, 0.65);
            border: 1px solid rgba(202, 178, 255, 0.14);
            min-height: 560px;
            min-height: 330px;
            white-space: pre-wrap;
            line-height: 1.65;
        }

        .footer-note {
            color: var(--muted);
            text-align: center;
            font-size: 0.88rem;
            margin-top: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults = {
        "humanized_output": "",
        "detection_result": None,
        "gemini_api_key": "",
        "sapling_api_key": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()
inject_styles()


def get_secret_value(name: str) -> str:
    try:
        secret_value = st.secrets[name]
    except (KeyError, StreamlitSecretNotFoundError):
        secret_value = ""

    env_value = os.getenv(name, "")
    session_value = st.session_state.get(name.lower(), "")
    return (session_value or secret_value or env_value or "").strip()


GEMINI_API_KEY = get_secret_value("GEMINI_API_KEY")
SAPLING_API_KEY = get_secret_value("SAPLING_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


ROYAL_TONES = {
    "Royal Rewrite": "Elevate the writing with natural transitions, elegant rhythm, and modern conversational clarity while preserving the exact meaning.",
    "Warm & Human": "Make the text feel approachable, warm, and confidently human, with varied sentence lengths and authentic phrasing.",
    "Executive Polish": "Refine the text to sound polished, premium, and launch-ready for clients, founders, and brand communication.",
}


def clean_text_locally(text: str) -> str:
    replacements = {
        "utilize": "use",
        "moreover": "also",
        "in order to": "to",
        "it is important to note that": "",
        "delve": "explore",
        "tapestry": "blend",
    }
    cleaned = re.sub(r"\s+", " ", text).strip()
    for old, new in replacements.items():
        cleaned = re.sub(old, new, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bAI\b", "AI", cleaned)
    return cleaned


def build_humanize_prompt(text: str, tone: str, audience: str, preserve_length: bool) -> str:
    length_rule = "Keep the length close to the original." if preserve_length else "You may slightly shorten the text for better readability."
    return (
        f"You are a premium editorial assistant for a public website launch. {ROYAL_TONES[tone]} "
        f"Target audience: {audience}. Maintain factual meaning, remove robotic phrasing, and avoid cliches. "
        f"{length_rule} Return only the rewritten text.\n\n"
        f"Original text:\n{text}"
    )



def humanize_text(text: str, tone: str, audience: str, preserve_length: bool) -> str:
    if not GEMINI_API_KEY:
        return (
            "Add a Gemini API key in the sidebar, Streamlit secrets, or environment variables to unlock the AI humanizer.\n\n"
            "Tip: The app is launch-ready, but this feature requires your own key for production use."
        )

    prompt = build_humanize_prompt(text, tone, audience, preserve_length)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return f"Humanizer error: {exc}"



def detect_ai_sapling(text: str) -> Optional[dict]:
    if not SAPLING_API_KEY:
        return {
            "score": None,
            "label": "API key needed",
            "detail": "Add a Sapling API key in the sidebar, Streamlit secrets, or environment variables to run AI detection.",
        }

    url = "https://api.sapling.ai/api/v1/aidetector"
    payload = {"key": SAPLING_API_KEY, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        score = round(data.get("score", 0) * 100, 1)
        label = "AI-Generated" if score > 70 else "Mixed/Unclear" if score > 30 else "Human-Written"
        detail = "Higher scores suggest the text follows patterns often seen in machine-generated writing."
        return {"score": score, "label": label, "detail": detail}
    except requests.RequestException as exc:
        return {
            "score": None,
            "label": "Detection unavailable",
            "detail": f"Sapling request failed: {exc}",
        }



def render_metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class=\"metric-card\">
            <div class=\"metric-label\">{label}</div>
            <div class=\"metric-value\">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("## 👑 Launch Control")
    st.caption("Configure your app for demos, staging, or production.")

    st.session_state.gemini_api_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        placeholder="Paste your Gemini key",
        help="Optional here if you already store it in Streamlit secrets or environment variables.",
    )
    st.session_state.sapling_api_key = st.text_input(
        "Sapling API Key",
        value=st.session_state.sapling_api_key,
        type="password",
        placeholder="Paste your Sapling key",
        help="Optional here if you already store it in Streamlit secrets or environment variables.",
    )

    gemini_ready = "Ready" if get_secret_value("GEMINI_API_KEY") else "Missing"
    sapling_ready = "Ready" if get_secret_value("SAPLING_API_KEY") else "Missing"
    render_metric_card("Gemini", gemini_ready)
    render_metric_card("Sapling", sapling_ready)

    st.markdown("### ✨ Demo shortcuts")
    if st.button("Load marketing sample"):
        st.session_state.sample_text = (
            "Our AI-powered assistant helps teams produce content faster and improve clarity across emails, blogs, and sales pages. "
            "It saves time, increases output, and provides better consistency for growing brands."
        )

    st.markdown(
        """
        <div class="info-card">
            <strong>Launch checklist</strong><br>
            • Add your production API keys.<br>
            • Verify your final copy style.<br>
            • Deploy on Streamlit Community Cloud or your preferred host.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="royal-shell">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-card">
        <div class="brand-row">
            <div class="brand-mark">👑 Royal <span>Humanize AI</span></div>
            <div class="brand-badge">Launch-ready copy studio</div>
        </div>
        <h1 class="hero-title">Make AI text feel premium,<br>credible, and deeply human.</h1>
        <div class="hero-subtitle">
            Refine machine-written drafts into polished messaging for websites, emails, proposals, and product launches.
            Built with a royal palette, faster setup, and clearer controls for real-world use.
        </div>
        <div class="status-pill">● Bring your own API keys, or preview the full interface now and connect production services later.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

mode = st.radio(
    "Select Tool",
    ["Humanizer", "AI Detector"],
    horizontal=True,
    label_visibility="collapsed",
)

sample_text = st.session_state.get("sample_text", "")

if mode == "Humanizer":
    st.markdown("### Humanizer Studio")
    controls_col1, controls_col2, controls_col3 = st.columns([1.3, 1.3, 1])
    with controls_col1:
        tone = st.selectbox("Tone", list(ROYAL_TONES.keys()), index=0)
    with controls_col2:
        audience = st.selectbox(
            "Audience",
            ["Website visitors", "Clients & buyers", "Startup users", "Students", "Professional readers"],
            index=0,
        )
    with controls_col3:
        preserve_length = st.toggle("Preserve length", value=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Original text</div>', unsafe_allow_html=True)
        st.markdown('<div class="helper-text">Paste AI-generated content, ad copy, blog drafts, or product text here.</div>', unsafe_allow_html=True)

        user_input = st.text_area(
            "Input text",
            value=sample_text,
            placeholder="Paste your text here...",
            label_visibility="collapsed",
        )

        input_word_count = len(user_input.split()) if user_input else 0
        render_metric_card("Input words", str(input_word_count))

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("Humanize Content"):
                if not user_input.strip():
                    st.warning("Please paste some text before running the humanizer.")
                else:
                    st.session_state.humanized_output = humanize_text(user_input, tone, audience, preserve_length)
        with action_col2:
            if st.button("Quick Clean"):
                if not user_input.strip():
                    st.warning("Please paste some text before running Quick Clean.")
                else:
                    st.session_state.humanized_output = clean_text_locally(user_input)

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("Humanize Content"):
                if not user_input.strip():
                    st.warning("Please paste some text before running the humanizer.")
                else:
                    st.session_state.humanized_output = humanize_text(user_input, tone, audience, preserve_length)
        with action_col2:
            if st.button("Quick Clean"):
                if not user_input.strip():
                    st.warning("Please paste some text before running Quick Clean.")
                else:
                    st.session_state.humanized_output = clean_text_locally(user_input)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Refined output</div>', unsafe_allow_html=True)
        st.markdown('<div class="helper-text">Use AI Humanizer for premium rewriting or Quick Clean for a local polish pass.</div>', unsafe_allow_html=True)

        output_text = st.session_state.humanized_output
        if output_text:
            output_word_count = len(output_text.split())
            render_metric_card("Output words", str(output_word_count))
            st.markdown(f'<div class="result-box">{output_text}</div>', unsafe_allow_html=True)
            st.download_button(
                "Download refined text",
                data=output_text,
                file_name="royal-humanized-text.txt",
                mime="text/plain",
            )
        else:
            st.markdown('<div class="result-box">Your improved text will appear here after you run the humanizer.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

elif mode == "AI Detector":
    st.markdown("### AI Detector")
    detector_col1, detector_col2 = st.columns([1.1, 0.9])
    with detector_col1:
        st.markdown('<div class="section-label">Analyze a passage</div>', unsafe_allow_html=True)
        st.markdown('<div class="helper-text">Paste the text you want to review and run the detector.</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Analyze a passage</div>', unsafe_allow_html=True)
        detect_input = st.text_area(
            "Detector text",
            placeholder="Paste text to analyze for AI-like patterns...",
            label_visibility="collapsed",
        )
        if st.button("Detect AI Presence"):
            if not detect_input.strip():
                st.warning("Please paste some text before running detection.")
            else:
                st.session_state.detection_result = detect_ai_sapling(detect_input)

    with detector_col2:
        st.markdown('<div class="section-label">Detection result</div>', unsafe_allow_html=True)
        st.markdown('<div class="helper-text">View the AI probability, label, and detector notes here.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with detector_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Detection result</div>', unsafe_allow_html=True)
        result = st.session_state.detection_result
        if result:
            if result["score"] is not None:
                st.metric("Probability of AI", f"{result['score']}%")
            st.subheader(result["label"])
            st.caption(result["detail"])
        else:
            st.markdown('<div class="result-box">Your AI detection result will appear here.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer-note">Royal Humanize AI • Premium UX refresh for a more launch-ready experience.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
