import os
import time
import requests
import streamlit as st

# ============================================================
# Moodline — Streamlit version
# ============================================================

st.set_page_config(
    page_title="Moodline — read the emotion in your words",
    page_icon="✎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

#API_BASE_URL = os.getenv("MOODLINE_API_URL", "http://127.0.0.1:8000")

EMOJI = {
    "sadness": "😢",
    "joy": "😄",
    "love": "❤️",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
}

ACCENTS = {
    "sadness": "#5b7fde",
    "joy": "#f2b705",
    "love": "#e85d75",
    "anger": "#e4572e",
    "fear": "#8b5fbf",
    "surprise": "#17bebb",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #0e0f14;
        --surface: #16171f;
        --surface-2: #1c1e29;
        --border: rgba(255,255,255,0.08);
        --text: #f2f0ea;
        --text-dim: #9497a6;
        --text-faint: #5c5f6d;
        --accent: #6c7a89;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(60% 50% at 50% -10%, rgba(108,122,137,.18), transparent 70%),
            var(--bg) !important;
        color: var(--text) !important;
        font-family: "Space Grotesk", sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 960px;
        padding-top: 48px;
        padding-bottom: 40px;
    }

    .moodline-topbar {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 48px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-mark {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        display: inline-block;
    }

    .brand-mark.live {
        background: #52d17c;
        box-shadow: 0 0 0 3px rgba(82,209,124,.18);
    }

    .brand-mark.warming {
        background: #f2b705;
        box-shadow: 0 0 0 3px rgba(242,183,5,.18);
        animation: pulse-dot 1.4s ease-in-out infinite;
    }

    .brand-mark.down {
        background: #e4572e;
        box-shadow: 0 0 0 3px rgba(228,87,46,.18);
    }

    .brand-name {
        font-family: "Fraunces", serif;
        font-weight: 600;
        font-size: 20px;
        color: #f2f0ea;
    }

    .brand-tag {
        margin: 0;
        color: #9497a6;
        font-size: 13px;
    }

    @keyframes pulse-dot {
        50% { opacity: .35; }
    }

    .console {
        display: grid;
        grid-template-columns: 220px 1fr;
        gap: 40px;
        align-items: center;
        padding: 40px;
        border: 1px solid var(--border);
        border-radius: 28px;
        background: linear-gradient(180deg, var(--surface), var(--surface-2));
    }

    .orb-stage {
        position: relative;
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .orb-glow {
        position: absolute;
        width: 190px;
        height: 190px;
        border-radius: 50%;
        background: radial-gradient(circle, var(--accent) 0%, transparent 72%);
        filter: blur(26px);
        opacity: .55;
        animation: breathe 6s ease-in-out infinite;
    }

    .orb {
        position: relative;
        width: 148px;
        height: 148px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, var(--accent), #0e0f14);
        border-radius: 42% 58% 65% 35% / 48% 42% 58% 52%;
        box-shadow: inset 0 0 30px rgba(255,255,255,.14),
                    0 20px 40px -18px var(--accent);
        animation: morph 9s ease-in-out infinite, breathe 6s ease-in-out infinite;
    }

    .orb.thinking {
        animation: morph 2.1s ease-in-out infinite, spin 2.1s linear infinite;
    }

    .orb-emoji {
        font-size: 38px;
        color: rgba(255,255,255,.92);
        filter: drop-shadow(0 4px 10px rgba(0,0,0,.35));
    }

    @keyframes breathe {
        0%,100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    @keyframes morph {
        0%,100% { border-radius: 42% 58% 65% 35% / 48% 42% 58% 52%; }
        33% { border-radius: 60% 40% 44% 56% / 40% 62% 38% 60%; }
        66% { border-radius: 48% 52% 38% 62% / 62% 40% 60% 38%; }
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .eyebrow {
        display: block;
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        letter-spacing: .14em;
        color: #5c5f6d;
        margin-bottom: 14px;
    }

    .input-panel {
        min-width: 0;
    }

    .char-count {
        font-family: "JetBrains Mono", monospace;
        font-size: 12px;
        color: #5c5f6d;
        text-align: right;
        margin-top: 8px;
    }

    div[data-testid="stTextArea"] textarea {
        background: rgba(0,0,0,.18) !important;
        border: 1px solid rgba(255,255,255,.08) !important;
        border-radius: 14px !important;
        color: #f2f0ea !important;
        font-size: 16px !important;
        line-height: 1.55 !important;
        min-height: 118px !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(108,122,137,.18) !important;
    }

    .stButton > button {
        border: none !important;
        border-radius: 999px !important;
        background: #f2f0ea !important;
        color: #0e0f14 !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        min-height: 44px !important;
    }

    .stButton > button:hover {
        background: var(--accent) !important;
        color: white !important;
        transform: translateY(-2px);
    }

    .result-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
        margin-top: 32px;
    }

    .result-card {
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 24px;
        padding: 32px;
        background: linear-gradient(180deg, var(--surface), var(--surface-2));
    }

    .emotion-main {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
    }

    .emotion-emoji {
        font-size: 40px;
        line-height: 1;
    }

    .emotion-word {
        margin: 0;
        font-family: "Fraunces", serif;
        font-style: italic;
        font-weight: 600;
        font-size: clamp(36px, 6vw, 52px);
        color: var(--accent);
    }

    .confidence {
        display: inline-block;
        font-family: "JetBrains Mono", monospace;
        font-size: 13px;
        color: #9497a6;
        margin-bottom: 20px;
    }

    .echoed {
        margin: 0;
        padding-top: 18px;
        border-top: 1px solid rgba(255,255,255,.08);
        font-size: 14.5px;
        line-height: 1.6;
        color: #9497a6;
        font-style: italic;
    }

    .bar-row {
        display: grid;
        grid-template-columns: 84px 1fr 52px;
        align-items: center;
        gap: 12px;
        margin: 14px 0;
    }

    .bar-label {
        font-size: 13px;
        color: #9497a6;
    }

    .bar-track {
        height: 8px;
        border-radius: 999px;
        background: rgba(255,255,255,.06);
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 999px;
        animation: fillbar 900ms cubic-bezier(.16,1,.3,1) both;
        transform-origin: left;
    }

    @keyframes fillbar {
        from { width: 0 !important; }
    }

    .bar-pct {
        font-family: "JetBrains Mono", monospace;
        font-size: 12px;
        color: #5c5f6d;
        text-align: right;
    }

    .footbar {
        margin-top: 40px;
        display: flex;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        font-size: 12px;
        color: #5c5f6d;
        font-family: "JetBrains Mono", monospace;
    }

    .error-msg {
        color: #ff8a72;
        font-family: "JetBrains Mono", monospace;
        font-size: 13px;
        margin-top: 12px;
    }

    @media (max-width: 720px) {
        .console {
            grid-template-columns: 1fr;
            padding: 28px;
            gap: 28px;
        }
        .result-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None
if "last_text" not in st.session_state:
    st.session_state.last_text = ""
if "error" not in st.session_state:
    st.session_state.error = None

# ------------------------------------------------------------
# Health check
# ------------------------------------------------------------

def check_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        return bool(data.get("model_loaded")), None
    except Exception as exc:
        return False, str(exc)

model_ready, health_error = check_health()

if model_ready:
    status_kind = "live"
    status_text = "model ready — say something"
else:
    status_kind = "down" if health_error else "warming"
    status_text = "can't reach the server" if health_error else "waking the model up…"

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="moodline-topbar">
        <div class="brand">
            <span class="brand-mark {status_kind}"></span>
            <span class="brand-name">Moodline</span>
        </div>
        <p class="brand-tag">an instrument that reads the mood inside a sentence</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Current emotion controls the accent/orb
# ------------------------------------------------------------

current_emotion = (
    st.session_state.result.get("predicted_emotion")
    if st.session_state.result
    else None
)
accent = ACCENTS.get(current_emotion, "#6c7a89")

st.markdown(
    f"""
    <style>
    :root {{
        --accent: {accent};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Console
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="console">
        <div class="orb-stage">
            <div class="orb-glow"></div>
            <div class="orb {'thinking' if st.session_state.get('thinking') else ''}"
                 style="--accent:{accent};">
                <span class="orb-emoji">
                    {EMOJI.get(current_emotion, "✎")}
                </span>
            </div>
        </div>
        <div class="input-panel">
            <span class="eyebrow">INPUT</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Put Streamlit input over the right side of the console.
# The surrounding custom CSS makes it visually match the original.
text = st.text_area(
    "INPUT",
    value=st.session_state.get("last_text", ""),
    max_chars=2000,
    height=118,
    placeholder='Write a sentence and let it speak for itself\n— e.g. “I can\'t believe we actually pulled this off.”',
    label_visibility="collapsed",
    key="text_input",
)

st.markdown(
    f'<div class="char-count">{len(text)} / 2000</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 0.28])

with col2:
    analyze = st.button(
        "Read the mood  →",
        disabled=(not text.strip() or not model_ready),
        use_container_width=True,
    )

if analyze:
    st.session_state.thinking = True
    st.session_state.error = None
    st.session_state.last_text = text

    try:
        with st.spinner("Reading…"):
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json={"text": text.strip()},
                timeout=60,
            )

        if not response.ok:
            try:
                body = response.json()
                detail = body.get("detail", "The model couldn't process that sentence.")
            except Exception:
                detail = f"Request failed ({response.status_code})."
            raise RuntimeError(detail)

        data = response.json()

        # Same response fields expected by the original frontend.
        st.session_state.result = {
            "predicted_emotion": data["predicted_emotion"],
            "confidence": data["confidence"],
            "all_probabilites": data["all_probabilites"],
        }
        st.session_state.last_text = text.strip()
        st.session_state.error = None

    except Exception as exc:
        st.session_state.result = None
        st.session_state.error = str(exc)

    finally:
        st.session_state.thinking = False
        st.rerun()

if st.session_state.error:
    st.markdown(
        f'<div class="error-msg">{st.session_state.error}</div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

result = st.session_state.result

if result:
    emotion = result["predicted_emotion"]
    emoji = EMOJI.get(emotion, "🙂")
    confidence = float(result["confidence"]) * 100
    probs = result["all_probabilites"]

    st.markdown(
        f"""
        <style>
        :root {{
            --accent: {ACCENTS.get(emotion, "#6c7a89")};
        }}
        </style>

        <div class="result-grid">
            <div class="result-card">
                <span class="eyebrow">DETECTED</span>
                <div class="emotion-main">
                    <span class="emotion-emoji">{emoji}</span>
                    <h1 class="emotion-word">{emotion.capitalize()}</h1>
                </div>
                <span class="confidence">{confidence:.1f}% confidence</span>
                <blockquote class="echoed">“{st.session_state.last_text}”</blockquote>
            </div>

            <div class="result-card">
                <span class="eyebrow">BREAKDOWN</span>
        """,
        unsafe_allow_html=True,
    )

    for label, value in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        pct = float(value) * 100
        bar_color = ACCENTS.get(label, "#6c7a89")

        st.markdown(
            f"""
            <div class="bar-row">
                <span class="bar-label">{EMOJI.get(label, "")} {label}</span>
                <span class="bar-track">
                    <span class="bar-fill"
                          style="width:{pct:.1f}%;background:{bar_color};"></span>
                </span>
                <span class="bar-pct">{pct:.1f}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="footbar">
        <span>{status_text}</span>
        <span>⌘ / Ctrl + Enter to analyze</span>
    </div>
    """,
    unsafe_allow_html=True,
)
