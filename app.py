"""
The Bio-Sieve Protocol - v5.0.0-PROD
Complete UI/UX Redesign & Functional Multi-Page Biotechnology Platform.
Inspired by the NovaCell Biotechnology Aesthetic:
- Soft pale cyan & ice-blue backgrounds (#F7FCFD, #D1F7FC, #EAF8FB)
- Deep navy editorial typography (#102D4D, #536D82)
- Teal (#168FA1) and cyan (#69D9E8) accents
- Clean rectangular top navbar with organized options and solid border
- Announcement strip in clean sans-serif typography throughout
- Reliable button navigation across all pages and actions
- Rounded floating scientific cards, 3D cellular structures with seamless background fusion
- Transparent reporting: Core implemented engines vs. simulated hardware boundaries
- Six dedicated pages: Overview, Exact Match, Fuzzy Analysis, Secure Enclave, Homomorphic Sync, Analysis History
- Zero cloud dependencies: 100% local-first air-gapped processing
- Zero emojis: Clean vector SVGs and typography throughout
"""

import base64
from collections import Counter
from datetime import datetime, timezone
import json
import math
import os
import textwrap
import time
import streamlit as st

# Import core algorithmic engines from engine.py
from engine import (
    AUTOMATON_ROOT,
    HAZARDOUS_REFERENCE_BACKBONE,
    HAZARDOUS_WATCHLIST,
    REFERENCE_TOXIN_PROFILE,
    SAMPLE_BENIGN_SEQUENCE,
    compute_shannon_entropy,
    compute_vector_cosine_similarity,
    de_shuffle_steganographic_fragments,
    execute_ephemeral_honeynet_invalidation,
    execute_honeynet_redirection,
    execute_mesh_optical_handshake,
    generate_sat_broadcast_payload,
    homomorphic_blind_delta_merge,
    parse_canonical_fasta,
    search_aho_corasick,
    simulate_runtime_execution_matrix,
    synchronize_mesh_ledger,
    tokenize_kmers,
)

# Import Offline AI/ML & Physics simulation modules
from fragment_affinity import FragmentAffinityAnalyzer
from thermal_interlock import FlowRegime, InterlockState, RuntimePhysicsSimulator, SafetyThresholds
from validation_engine import EphemeralValidationEngine, PeerRegistryMesh
from dashboard import MonochromeTerminalDashboard


# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="The Bio-Sieve Protocol | Local-First Biosecurity",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Helper for rendering raw HTML safely without Markdown indentation code-block bugs
def render_html(content: str):
    """Renders raw HTML directly via st.html() with all leading indents stripped."""
    st.html(textwrap.dedent(content).strip())


# Asset helpers for offline Base64 data URIs
def get_image_base64(relative_path: str) -> str:
    """Returns local image encoded as a base64 Data URI for offline rendering."""
    abs_path = os.path.join(os.path.dirname(__file__), relative_path)
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            data = f.read()
        ext = relative_path.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
        return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"
    return ""


# Pre-encode images once for maximum rendering performance
IMG_HERO_CELL = get_image_base64("assets/hero_cell.jpg")
IMG_EXACT_MATCH = get_image_base64("assets/exact_match.jpg")
IMG_FUZZY_ANALYSIS = get_image_base64("assets/fuzzy_analysis.jpg")
IMG_SECURE_ENCLAVE = get_image_base64("assets/secure_enclave.jpg")
IMG_HOMOMORPHIC_SYNC = get_image_base64("assets/homomorphic_sync.jpg")


# ==============================================================================
# 1B. SAMPLE SPECIMEN FOR INGESTION (RESILIENT FOR LOCAL & CLOUD DEPLOYMENT)
# ==============================================================================
def load_sample_specimen_fasta() -> str:
    """
    Loads the canonical synthetic biosecurity specimen for user download.
    Reads from disk if present, with a guaranteed fallback so it always works
    when deployed to Streamlit Cloud, Docker, or any remote server.
    """
    sample_path = os.path.join(os.path.dirname(__file__), "synthetic_biosecurity_specimen.fasta")
    if os.path.exists(sample_path):
        try:
            with open(sample_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    return content
        except Exception:
            pass
    # Resilient fallback for Docker / Streamlit Community Cloud deployments
    return textwrap.dedent("""\
        >SYNTHETIC_CHIMERA_EXPRESSION_CONSTRUCT_VECTOR_v4 [ORGANISM: SYNTHETIC] [RISK_PROFILE: UNVERIFIED]
        ATGCGTACGATCGATCGATCGATCGATCGAATTCGCGCGCGATCGATCGATCGATCGATC
        GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCCCGGGATT
        AGCTAGCTAGCTAGCTAAGCTTGCATGCATGCATGCATGCATGCATTTTAAAGCGATCGA
        TCGATCGAATTCCCGGGAAATTTCCCGGGAAATTTCCCGGATGTTTCCCAAGGCCTTAAA
        TTTGGGCCCAACGCGCGATCGATATGCGTACGATCCGGGAAATTTAAATTTCCCGGGCTA
        GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAAGCTTGATCGATCGATCGATCGATCGA
    """).strip()

SAMPLE_SPECIMEN_FASTA = load_sample_specimen_fasta()

# Presentation deck loaders (PDF & Google Drive)
GOOGLE_DRIVE_SLIDES_URL = "https://drive.google.com/drive/folders/10k-tbMdE30vJ5d2VdZpnDgXNbewXMHdC?usp=sharing"

def load_presentation_pdf_bytes() -> bytes:
    pdf_path = os.path.join(os.path.dirname(__file__), "Bio SIeve Protocol.pdf")
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                return f.read()
        except Exception:
            pass
    return b"%PDF-1.4 [Bio Sieve Protocol Presentation Deck]"

PRESENTATION_PDF_BYTES = load_presentation_pdf_bytes()


# ==============================================================================
# 2. NOVACELL BIOTECHNOLOGY DESIGN SYSTEM (INLINE CSS)
# ==============================================================================
NOVACELL_THEME_CSS = """
<style>
/* ---------------- Typography & Fonts ---------------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

:root {
    --bg-primary: #FFFFFF;
    --hero-bg: radial-gradient(120% 80% at 75% 20%, #F0F9FF 0%, #F8FAFC 50%, #FFFFFF 100%);
    --surface-card: #FFFFFF;
    --surface-secondary: #F8FAFC;
    --text-navy: #102D4D;
    --text-muted: #536D82;
    --teal-accent: #168FA1;
    --cyan-accent: #0EA5E9;
    --border-light: rgba(22, 143, 161, 0.16);
    --border-input: #CBD5E1;
    --diagnostic-dark: #0F172A;
    --shadow-soft: 0 10px 30px rgba(16, 45, 77, 0.06);
    --shadow-card: 0 8px 25px rgba(16, 45, 77, 0.07);
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #FFFFFF !important;
    color: #102D4D !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 16px !important;
    -webkit-font-smoothing: antialiased;
}

/* Hide default streamlit header decoration */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu, footer {
    visibility: hidden !important;
}

/* ---------------- Global Typography System ---------------- */
.section-eyebrow {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #168FA1 !important;
    background: #EAF8FB !important;
    padding: 6px 14px !important;
    border-radius: 9999px !important;
    display: inline-block !important;
    margin-bottom: 12px !important;
    border: 1px solid rgba(22, 143, 161, 0.25) !important;
}

.section-headline {
    font-family: 'Inter', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    color: #102D4D !important;
    letter-spacing: -0.03em !important;
    margin: 6px 0 10px 0 !important;
    line-height: 1.2 !important;
}

.section-description {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    color: #536D82 !important;
    line-height: 1.65 !important;
    max-width: 720px !important;
    margin-bottom: 24px !important;
}

.feature-title {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.60rem !important;
    font-weight: 900 !important;
    color: #102D4D !important;
    letter-spacing: -0.025em !important;
    margin: 8px 0 !important;
    line-height: 1.25 !important;
}

.feature-description {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    color: #536D82 !important;
    line-height: 1.65 !important;
    margin-bottom: 18px !important;
}

.card-title {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.32rem !important;
    font-weight: 900 !important;
    color: #102D4D !important;
    letter-spacing: -0.02em !important;
}

.card-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.96rem !important;
    font-weight: 500 !important;
    color: #536D82 !important;
    line-height: 1.55 !important;
    margin-top: 4px !important;
}

/* ---------------- Highlighted Capability Badges ---------------- */
.capability-highlight-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #F0F9FF;
    border: 1.5px solid rgba(22, 143, 161, 0.25);
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.86rem;
    font-weight: 700;
    color: #102D4D;
    box-shadow: 0 4px 12px rgba(22, 143, 161, 0.08);
    margin: 12px 0 20px 0;
}

.capability-highlight-badge.badge-warning {
    background: #FFFBEB;
    border-color: #FCD34D;
    color: #92400E;
}

.badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #168FA1;
    display: inline-block;
}

.badge-dot.pulse {
    animation: pulseGlow 2s infinite ease-in-out;
}

@keyframes pulseGlow {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 143, 161, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(22, 143, 161, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 143, 161, 0); }
}

.badge-dot-amber {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #F59E0B;
    display: inline-block;
}

.badge-sep {
    color: #94A3B8;
    font-weight: 800;
    margin: 0 4px;
}

/* ---------------- Image Fusion Styles (Seamless Background Blending) ---------------- */
.hero-image-fused-container {
    position: relative;
    width: 100%;
    height: 480px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border-radius: 24px;
    border: none !important;
    overflow: hidden;
    box-shadow: none !important;
}

.hero-fused-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border: none !important;
    border-radius: 24px;
    -webkit-mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 58%, rgba(0,0,0,0) 98%);
    mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 58%, rgba(0,0,0,0) 98%);
    filter: drop-shadow(0 20px 40px rgba(16, 45, 77, 0.08));
}

.feature-image-fused-container {
    position: relative;
    width: 100%;
    height: 290px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border-radius: 18px;
    overflow: hidden;
    border: none !important;
    box-shadow: none !important;
}

.feature-fused-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border: none !important;
    border-radius: 18px;
    -webkit-mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 60%, rgba(0,0,0,0) 100%);
    mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 60%, rgba(0,0,0,0) 100%);
    filter: drop-shadow(0 12px 30px rgba(16, 45, 77, 0.06));
}

.floating-hero-card {
    position: absolute;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1.5px solid rgba(22, 143, 161, 0.22);
    border-radius: 14px;
    padding: 14px 20px;
    box-shadow: 0 16px 36px rgba(16, 45, 77, 0.12);
    z-index: 10;
}

/* ---------------- Top Announcement Strip (Strict Sans-Serif) ---------------- */
.announcement-strip {
    background: #0A192F;
    color: #FFFFFF;
    padding: 8px 18px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.80rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid rgba(22, 143, 161, 0.25);
    white-space: nowrap;
    overflow: hidden;
}

.announcement-strip * {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.announcement-left {
    font-weight: 800;
    letter-spacing: 0.03em;
    font-size: 0.80rem;
    white-space: nowrap;
}

.announcement-right {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.78rem;
    white-space: nowrap;
}

.announcement-divider {
    color: rgba(255, 255, 255, 0.4);
}

/* ---------------- Rectangular Top Navbar Styling ---------------- */
.brand-badge {
    display: flex;
    align-items: center;
    gap: 8px;
}

.brand-icon-circle {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, #168FA1 0%, #102D4D 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(22, 143, 161, 0.3);
}

/* Custom Navbar container with clean rectangular border */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1.5px solid rgba(22, 143, 161, 0.20) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(16, 45, 77, 0.04) !important;
    padding: 8px 12px !important;
    margin-bottom: 16px !important;
}

/* Navbar button & Download button styling with zero truncation */
div.stButton > button,
div.stDownloadButton > button {
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 5px 6px !important;
    border-radius: 6px !important;
    white-space: nowrap !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    min-height: 34px !important;
    letter-spacing: -0.01em !important;
}

div.stButton > button p,
div.stDownloadButton > button p {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    margin: 0 !important;
    padding: 0 !important;
}

div.stButton > button[kind="primary"],
div.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(135deg, #168FA1 0%, #102D4D 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(22, 143, 161, 0.3) !important;
    box-shadow: 0 4px 14px rgba(22, 143, 161, 0.25) !important;
}

div.stButton > button[kind="primary"]:hover,
div.stDownloadButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #127585 0%, #0B2036 100%) !important;
    box-shadow: 0 6px 20px rgba(22, 143, 161, 0.35) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="secondary"],
div.stDownloadButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #102D4D !important;
    border: 1.5px solid rgba(22, 143, 161, 0.22) !important;
    box-shadow: 0 2px 6px rgba(16, 45, 77, 0.04) !important;
}

div.stButton > button[kind="secondary"]:hover,
div.stDownloadButton > button[kind="secondary"]:hover {
    background: #F0F9FF !important;
    border-color: #168FA1 !important;
    color: #168FA1 !important;
    transform: translateY(-1px) !important;
}

/* ---------------- Light Native Form Inputs Override ---------------- */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #102D4D !important;
    border: 1.5px solid var(--border-input) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.94rem !important;
    padding: 14px !important;
    box-shadow: inset 0 2px 4px rgba(16, 45, 77, 0.02) !important;
}

.stTextArea textarea:focus {
    border-color: #168FA1 !important;
    box-shadow: 0 0 0 3px rgba(22, 143, 161, 0.15) !important;
}

div[data-testid="stFileUploader"] {
    background-color: #F7FCFD !important;
    border: 1.5px dashed #A8DCE6 !important;
    border-radius: 14px !important;
    padding: 18px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: #168FA1 !important;
    background-color: #EAF8FB !important;
}

div[data-testid="stFileUploader"] section {
    background-color: transparent !important;
}

div[data-testid="stFileUploader"] section button {
    background: #FFFFFF !important;
    color: #102D4D !important;
    border: 1.5px solid #C8E6ED !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
}

div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] div {
    color: #536D82 !important;
    font-size: 0.90rem !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #102D4D !important;
    border: 1.5px solid var(--border-input) !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #102D4D !important;
    font-size: 0.95rem !important;
}

label, div[data-testid="stWidgetLabel"] p {
    color: #102D4D !important;
    font-weight: 700 !important;
    font-size: 0.96rem !important;
    letter-spacing: -0.01em !important;
}

/* ---------------- Hero Section Typography ---------------- */
.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.12;
    color: var(--text-navy);
    letter-spacing: -0.035em;
    margin-bottom: 18px;
}

.hero-subtitle {
    font-size: 1.18rem;
    line-height: 1.65;
    color: var(--text-muted);
    margin-bottom: 28px;
    max-width: 640px;
}

.hero-footer-line {
    font-size: 0.86rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--teal-accent);
    text-transform: uppercase;
    margin-top: 24px;
}

/* Diagnostic Panels (Dark Navy Terminal) */
.diagnostic-panel {
    background: var(--diagnostic-dark);
    border: 1.5px solid #1B3857;
    border-radius: 16px;
    padding: 22px;
    color: #F7FCFD;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.90rem;
    line-height: 1.65;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(16, 36, 58, 0.25);
}

.diagnostic-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1F4266;
    padding-bottom: 10px;
    margin-bottom: 12px;
    font-size: 0.86rem;
    color: var(--cyan-accent);
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* Stepper Component */
.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;
    padding: 14px 20px;
    background: var(--surface-secondary);
    border-radius: 16px;
    border: 1.5px solid var(--border-light);
}

.step-node {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-muted);
}

.step-node.active {
    color: var(--teal-accent);
    font-weight: 800;
}

.step-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #D8EAF0;
    color: #102D4D;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    font-weight: 800;
}

.step-node.active .step-circle {
    background: var(--teal-accent);
    color: #FFFFFF;
}

/* Tables */
.bio-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1.5px solid var(--border-light);
    margin-top: 14px;
    font-size: 0.92rem;
}

.bio-table th {
    background: var(--surface-secondary);
    color: var(--text-navy);
    font-weight: 700;
    text-align: left;
    padding: 13px 18px;
    border-bottom: 1.5px solid var(--border-light);
    font-size: 0.86rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.bio-table td {
    padding: 13px 18px;
    border-bottom: 1px solid var(--border-light);
    color: var(--text-navy);
    font-size: 0.92rem;
}

.bio-table tr:last-child td {
    border-bottom: none;
}

.bio-table tr:hover td {
    background: #F2FBFC;
}

/* Metric component override */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1.5px solid var(--border-light) !important;
    border-radius: 16px !important;
    padding: 18px 22px !important;
    box-shadow: var(--shadow-soft) !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

div[data-testid="stMetricValue"] {
    font-size: 1.85rem !important;
    font-weight: 900 !important;
    color: var(--text-navy) !important;
    letter-spacing: -0.02em !important;
}

/* Footer */
.biotech-footer {
    border-top: 1.5px solid var(--border-light);
    padding: 32px 0 20px 0;
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
</style>
"""

render_html(NOVACELL_THEME_CSS)


# ==============================================================================
# 3. STATE MANAGEMENT
# ==============================================================================
def init_session_state():
    """Initializes persistent application session variables."""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Overview"

    if "homomorphic_db_index" not in st.session_state:
        st.session_state.homomorphic_db_index = 1.0

    if "reference_toxin_weights" not in st.session_state:
        st.session_state.reference_toxin_weights = dict(REFERENCE_TOXIN_PROFILE)

    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = [
            {
                "timestamp": "2026-10-20T17:40:22Z",
                "filename": "synthetic_biosecurity_specimen.fasta",
                "length": 217,
                "sha256": "11b514ffc30bc6c1902811cd05f8636ccbd6ce2a8fa77ee9b382a58d71a0fb6b",
                "duration_ms": 0.0835,
                "status": "FLAGGED (3 MOTIFS)",
                "matches_count": 3,
            },
            {
                "timestamp": "2026-10-20T17:42:05Z",
                "filename": "Benign_Control_Actin1.fasta",
                "length": 271,
                "sha256": "9f8e21a4bc317208cd2814ef2981aa77218ef81c0029b37190019273cba14820",
                "duration_ms": 0.0612,
                "status": "CLEARED (0 MOTIFS)",
                "matches_count": 0,
            },
        ]

    if "threat_logs" not in st.session_state:
        st.session_state.threat_logs = [
            {
                "timestamp": "2026-10-20T17:35:12Z",
                "channel": "SYSTEM_CORE",
                "signature": "BOOT_INITIALIZE",
                "detail": "Air-Gapped Sieve Core loaded. Reference Watchlist: 7 Motifs. Hash tree verified.",
                "status": "NOMINAL",
            },
            {
                "timestamp": "2026-10-20T17:35:14Z",
                "channel": "MESH_REGISTRY",
                "signature": "OPTICAL_BUS_SYNC",
                "detail": "Ad-Hoc Ring Handshake established across 4 secure enclave nodes. Aggregate bandwidth: 41.6 Gbps.",
                "status": "SYNCHRONIZED",
            },
        ]

    if "active_nodes" not in st.session_state:
        st.session_state.active_nodes = [
            {
                "node_id": "NODE-SEC-ALPHA-01",
                "enclave_arch": "Intel SGX (Confidential Compute)",
                "pcr0_measurement": "0x89EF4C3A901B2C",
                "mesh_latency": "0.18 ms",
                "bandwidth": "10.4 Gbps Optical",
                "status": "AIR-GAPPED // SYNCHRONIZED",
                "compliance_state": "UNANIMOUS_CONSENSUS",
                "synced_db_index": "v1.0",
                "quarantine_token": "NONE",
            },
            {
                "node_id": "NODE-SEC-BETA-02",
                "enclave_arch": "AMD SEV-SNP (Isolated VM Memory)",
                "pcr0_measurement": "0x4B3A89EF901B2C",
                "mesh_latency": "0.24 ms",
                "bandwidth": "10.4 Gbps Optical",
                "status": "AIR-GAPPED // SYNCHRONIZED",
                "compliance_state": "UNANIMOUS_CONSENSUS",
                "synced_db_index": "v1.0",
                "quarantine_token": "NONE",
            },
            {
                "node_id": "NODE-SEC-GAMMA-03",
                "enclave_arch": "Apple Silicon Enclave (Secure Vault)",
                "pcr0_measurement": "0x1B2C4B3A89EF90",
                "mesh_latency": "0.31 ms",
                "bandwidth": "9.6 Gbps Optical",
                "status": "AIR-GAPPED // SYNCHRONIZED",
                "compliance_state": "UNANIMOUS_CONSENSUS",
                "synced_db_index": "v1.0",
                "quarantine_token": "NONE",
            },
            {
                "node_id": "NODE-SEC-DELTA-04",
                "enclave_arch": "AWS Nitro Enclave (Cryptographic HSM)",
                "pcr0_measurement": "0xEF901B2C4B3A89",
                "mesh_latency": "0.15 ms",
                "bandwidth": "11.2 Gbps Direct",
                "status": "AIR-GAPPED // SYNCHRONIZED",
                "compliance_state": "UNANIMOUS_CONSENSUS",
                "synced_db_index": "v1.0",
                "quarantine_token": "NONE",
            },
        ]

    if "latest_analysis" not in st.session_state:
        st.session_state.latest_analysis = None

    if "sample_fasta" not in st.session_state:
        st.session_state.sample_fasta = ""

    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = ""

    if "performance_telemetry" not in st.session_state:
        st.session_state.performance_telemetry = {
            "fasta_parse_ms": 0.0,
            "automaton_ms": 0.0,
            "tokenizer_ms": 0.0,
            "cosine_math_ms": 0.0,
            "last_similarity_score": 0.0,
            "safety_margin": 0.0,
        }

    if "last_fhe_update" not in st.session_state:
        st.session_state.last_fhe_update = None

    if "ml_analyzer" not in st.session_state:
        st.session_state.ml_analyzer = FragmentAffinityAnalyzer()

    if "ml_physics" not in st.session_state:
        st.session_state.ml_physics = RuntimePhysicsSimulator()

    if "ml_mesh_registry" not in st.session_state:
        st.session_state.ml_mesh_registry = PeerRegistryMesh()

    if "ml_validation_engine" not in st.session_state:
        st.session_state.ml_validation_engine = EphemeralValidationEngine(
            output_directory=".",
            registry=st.session_state.ml_mesh_registry,
        )

    if "last_ml_result" not in st.session_state:
        st.session_state.last_ml_result = None

    if "ml_sample_input" not in st.session_state:
        st.session_state.ml_sample_input = ""


init_session_state()


# Helper function for reliable programmatic page navigation
def navigate_to(page_name: str):
    """Sets active page and triggers clean Streamlit rerun without state conflicts."""
    st.session_state.active_page = page_name
    st.rerun()


# ==============================================================================
# 4. TOP ANNOUNCEMENT STRIP & RECTANGULAR TOP NAVBAR
# ==============================================================================
def render_header_and_navbar():
    """Renders the top announcement bar and rectangular top navbar with reliable button routing."""
    # 1. Top Announcement Strip (Clean single line)
    render_html(f"""
    <div class="announcement-strip">
        <div class="announcement-left">
            <span>BIO-SIEVE PROTOCOL // AIR-GAPPED BIOSECURITY</span>
            <span class="announcement-divider">|</span>
            <span style="color: #69D9E8;">SAMPLE: <strong>synthetic_biosecurity_specimen.fasta</strong></span>
            <span class="announcement-divider">|</span>
            <a href="{GOOGLE_DRIVE_SLIDES_URL}" target="_blank" style="color: #FDE047; text-decoration: none; font-weight: 700;">📁 PPT DRIVE FOLDER ↗</a>
        </div>
        <div class="announcement-right">
            <span>LOCAL: <strong style="color: #69D9E8;">ACTIVE</strong></span>
            <span class="announcement-divider">|</span>
            <span>AIR-GAP: <strong style="color: #69D9E8;">100%</strong></span>
            <span class="announcement-divider">|</span>
            <span>LEDGER: <strong style="color: #FFFFFF;">v{st.session_state.homomorphic_db_index:.1f}</strong></span>
            <span class="announcement-divider">|</span>
            <span>ZERO-CLOUD</span>
        </div>
    </div>
    """)

    # 2. Main Top Navbar with clean rectangular border and proper column widths
    current_page = st.session_state.active_page

    with st.container(border=True):
        col_brand, col_nav_1, col_nav_2, col_nav_3, col_nav_ml, col_nav_4, col_nav_5, col_nav_6, col_ppt, col_upload = st.columns(
            [0.92, 0.70, 0.76, 0.76, 0.92, 0.92, 1.05, 0.92, 1.10, 1.45],
            gap="small",
            vertical_alignment="center",
        )

        with col_brand:
            render_html("""
            <div class="brand-badge">
                <div class="brand-icon-circle">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                    </svg>
                </div>
                <div>
                    <div style="font-weight: 900; letter-spacing: -0.02em; color: #102D4D; font-size: 1.05rem; line-height: 1;">BIO-SIEVE</div>
                    <div style="font-size: 0.70rem; color: #168FA1; font-weight: 800; letter-spacing: 0.05em; margin-top: 2px;">PROTOCOL 5.0</div>
                </div>
            </div>
            """)

        with col_nav_1:
            if st.button("Overview", key="nav_btn_overview", type="primary" if current_page == "Overview" else "secondary", use_container_width=True):
                navigate_to("Overview")

        with col_nav_2:
            if st.button("Exact Match", key="nav_btn_exact", type="primary" if current_page == "Exact Match" else "secondary", use_container_width=True):
                navigate_to("Exact Match")

        with col_nav_3:
            if st.button("Fuzzy Sieve", key="nav_btn_fuzzy", type="primary" if current_page == "Fuzzy Analysis" else "secondary", use_container_width=True):
                navigate_to("Fuzzy Analysis")

        with col_nav_ml:
            if st.button("ML Operations", key="nav_btn_ml", type="primary" if current_page == "ML Operations" else "secondary", use_container_width=True):
                navigate_to("ML Operations")

        with col_nav_4:
            if st.button("Secure Enclave", key="nav_btn_enclave", type="primary" if current_page == "Secure Enclave" else "secondary", use_container_width=True):
                navigate_to("Secure Enclave")

        with col_nav_5:
            if st.button("Homomorphic Sync", key="nav_btn_sync", type="primary" if current_page == "Homomorphic Sync" else "secondary", use_container_width=True):
                navigate_to("Homomorphic Sync")

        with col_nav_6:
            if st.button("Analysis History", key="nav_btn_history", type="primary" if current_page == "Analysis History" else "secondary", use_container_width=True):
                navigate_to("Analysis History")

        with col_ppt:
            st.download_button(
                label="📥 Download PPT",
                data=PRESENTATION_PDF_BYTES,
                file_name="Bio_Sieve_Protocol_Presentation.pdf",
                mime="application/pdf",
                type="secondary",
                use_container_width=True,
                help="Download official presentation deck (Bio Sieve Protocol.pdf). Drive link: " + GOOGLE_DRIVE_SLIDES_URL,
                key="nav_btn_dl_ppt",
            )

        with col_upload:
            st.download_button(
                label="📥 Download Sample for Ingestion",
                data=SAMPLE_SPECIMEN_FASTA,
                file_name="synthetic_biosecurity_specimen.fasta",
                mime="text/plain",
                type="primary",
                use_container_width=True,
                help="Download the verified sample FASTA file (synthetic_biosecurity_specimen.fasta) containing threat motifs for screening ingestion.",
                key="nav_btn_dl_sample",
            )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 5. PAGE 1: PREMIUM LANDING PAGE (OVERVIEW)
# ==============================================================================
def render_page_overview():
    """Renders the NovaCell-inspired Biotechnology Landing Page."""
    # --------------------------------------------------------------------------
    # Hero Section (Asymmetric Two-Column)
    # --------------------------------------------------------------------------
    col_hero_left, col_hero_right = st.columns([1.3, 1.1], gap="large")

    with col_hero_left:
        render_html("""
        <div style="padding: 16px 0;">
            <span class="section-eyebrow">PRIVACY-FIRST BIOSECURITY INFRASTRUCTURE</span>
            <h1 class="hero-title">
                Screen with precision.<br/><span style="color: #168FA1;">Protect with confidence.</span>
            </h1>
            <p class="hero-subtitle">
                A modular sequence-screening platform combining exact-pattern filtering, similarity analysis,
                isolated execution concepts, and controlled reference updates in a privacy-conscious local workflow.
            </p>
            <div class="hero-footer-line">
                LOCAL-FIRST DESIGN · TRANSPARENT PROCESSING · AUDITABLE RESULTS
            </div>
        </div>
        """)

        # Call to Action Buttons
        col_cta_1, col_cta_2, col_cta_3, col_cta_4 = st.columns([1.1, 1.25, 1.45, 1.35])
        with col_cta_1:
            if st.button("Start an Analysis", key="hero_start_btn", type="primary", use_container_width=True):
                navigate_to("Exact Match")
        with col_cta_2:
            if st.button("Explore the Architecture", key="hero_arch_btn", type="secondary", use_container_width=True):
                navigate_to("Secure Enclave")
        with col_cta_3:
            st.download_button(
                label="📥 Download Sample for Ingestion",
                data=SAMPLE_SPECIMEN_FASTA,
                file_name="synthetic_biosecurity_specimen.fasta",
                mime="text/plain",
                type="primary",
                use_container_width=True,
                help="Download canonical synthetic FASTA specimen with threat motifs for immediate ingestion.",
                key="hero_dl_sample_btn",
            )
        with col_cta_4:
            st.download_button(
                label="📥 Download PPT",
                data=PRESENTATION_PDF_BYTES,
                file_name="Bio_Sieve_Protocol_Presentation.pdf",
                mime="application/pdf",
                type="secondary",
                use_container_width=True,
                help="Download the verified presentation deck (Bio Sieve Protocol.pdf).",
                key="hero_dl_ppt_btn",
            )

    with col_hero_right:
        # High-res scientific biotechnology asset seamlessly fused with background
        render_html(f"""
        <div class="hero-image-fused-container">
            <img src="{IMG_HERO_CELL}" alt="Cellular Biosecurity Structure" class="hero-fused-img" />
        </div>
        <div style="display: flex; gap: 14px; margin-top: 14px;">
            <div style="background: #FFFFFF; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 16px 20px; flex: 1; box-shadow: 0 4px 14px rgba(16, 45, 77, 0.04);">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase; letter-spacing: 0.05em;">Aho-Corasick Engine</div>
                <div style="font-size: 1.04rem; font-weight: 800; color: #102D4D; margin: 4px 0;">O(N) Line-Rate Traversal</div>
                <div style="font-size: 0.86rem; color: #536D82;">7 Reference Pathogen Motifs</div>
            </div>
            <div style="background: #FFFFFF; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 16px 20px; flex: 1; box-shadow: 0 4px 14px rgba(16, 45, 77, 0.04);">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase; letter-spacing: 0.05em;">32-Bit K-Mer Vector Sieve</div>
                <div style="font-size: 1.04rem; font-weight: 800; color: #102D4D; margin: 4px 0;">Vector Cosine Distance</div>
                <div style="font-size: 0.86rem; color: #536D82;">Gate Threshold: 0.8500</div>
            </div>
        </div>
        """)

    # --------------------------------------------------------------------------
    # Integrated Upload Area
    # --------------------------------------------------------------------------
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        render_html("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1.5px solid #D8EAF0;">
            <div>
                <span class="section-eyebrow">INGESTION GATEWAY</span>
                <div class="card-title">Begin with a sequence file</div>
                <div class="card-subtitle">Submit a standard canonical FASTA sequence file (.fasta, .fa, .txt) or enter raw nucleotide strings for real-time local inspection.</div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; background: #EAF8FB; color: #168FA1; padding: 7px 16px; border-radius: 9999px; font-weight: 700; border: 1px solid #D8EAF0;">
                FORMATS: FASTA / CANONICAL TXT
            </div>
        </div>
        """)

        col_up_file, col_up_text = st.columns([1.1, 1.9], gap="medium")

        with col_up_file:
            st.download_button(
                label="📥 Download Sample File for Ingestion",
                data=SAMPLE_SPECIMEN_FASTA,
                file_name="synthetic_biosecurity_specimen.fasta",
                mime="text/plain",
                type="primary",
                use_container_width=True,
                help="Download the verified synthetic FASTA specimen file for local ingestion screening.",
                key="overview_dl_sample_btn",
            )
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload Biological Sequence Record",
                type=["fasta", "fa", "fna", "txt"],
                help="Select a local sequence file. Data is parsed strictly in-memory without remote uploads.",
                key="overview_file_uploader",
            )

            if uploaded_file is not None:
                try:
                    file_text = uploaded_file.getvalue().decode("utf-8", errors="replace")
                    if file_text != st.session_state.get("sample_fasta", "") or uploaded_file.name != st.session_state.get("uploaded_filename", ""):
                        st.session_state.sample_fasta = file_text
                        st.session_state.uploaded_filename = uploaded_file.name
                        st.session_state.ml_sample_input = file_text
                        st.session_state.last_ml_result = None
                except Exception as e:
                    st.error(f"Error decoding uploaded file: {str(e)}")

            if st.session_state.get("uploaded_filename"):
                render_html(f"""
                <div style="background: #EAF8FB; border: 1.5px solid #168FA1; border-radius: 12px; padding: 12px 16px; margin-top: 10px; font-size: 0.88rem; color: #102D4D;">
                    <div style="font-weight: 800; color: #168FA1; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">Active Specimen Loaded Across All Tabs</div>
                    <div style="font-weight: 700; margin: 2px 0;">{st.session_state.uploaded_filename} ({len(st.session_state.sample_fasta):,} bp)</div>
                    <div style="font-size: 0.80rem; color: #536D82;">Synchronized with Exact Match, Fuzzy Sieve, ML Operations, and History.</div>
                </div>
                """)
            else:
                render_html("""
                <div style="background: #F7FCFD; border: 1px dashed #D8EAF0; border-radius: 12px; padding: 14px; margin-top: 10px; font-size: 0.88rem; color: #536D82; line-height: 1.55;">
                    <strong>Local Privacy Notice:</strong> Sequence records are processed exclusively in volatile memory and are never transmitted across external networks.
                </div>
                """)

        with col_up_text:
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("Load Hazardous Specimen", key="load_hazard_preset_ov", use_container_width=True):
                    st.session_state.sample_fasta = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state["overview_text_area"] = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state.uploaded_filename = "Hazardous_Synthetic_Backbone.fasta"
                    st.session_state.ml_sample_input = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state.last_ml_result = None
                    st.rerun()
            with col_btn2:
                if st.button("Load Benign Control", key="load_benign_preset_ov", use_container_width=True):
                    st.session_state.sample_fasta = SAMPLE_BENIGN_SEQUENCE
                    st.session_state["overview_text_area"] = SAMPLE_BENIGN_SEQUENCE
                    st.session_state.uploaded_filename = "Benign_Control_Actin1.fasta"
                    st.session_state.ml_sample_input = SAMPLE_BENIGN_SEQUENCE
                    st.session_state.last_ml_result = None
                    st.rerun()
            with col_btn3:
                if st.button("Clear Input Buffer", key="clear_preset_ov", use_container_width=True):
                    st.session_state.sample_fasta = ""
                    st.session_state["overview_text_area"] = ""
                    st.session_state.uploaded_filename = ""
                    st.session_state.ml_sample_input = ""
                    st.session_state.last_ml_result = None
                    st.rerun()

            input_text = st.text_area(
                "Or Paste Canonical FASTA String",
                value=st.session_state.get("overview_text_area") or st.session_state.sample_fasta,
                height=130,
                placeholder=">SEQUENCE_IDENTIFIER | METADATA\nATGCGATCGATCGATCGATCGA...",
                key="overview_text_area",
            )

            col_sub_sel, col_sub_btn = st.columns([1.4, 1.0])
            with col_sub_sel:
                eval_mode = st.selectbox(
                    "Select Evaluation Pipeline",
                    [
                        "Comprehensive Pipeline (Exact Match + Fuzzy Cosine Sieve)",
                        "High-Speed Exact Match Automaton Only",
                        "Mathematical K-Mer Vector Sieve Only",
                    ],
                    key="overview_eval_mode",
                )
            with col_sub_btn:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                execute_screening = st.button(
                    "Run Biosecurity Screening",
                    use_container_width=True,
                    type="primary",
                    key="overview_run_screening_btn",
                )

        if execute_screening:
            sequence_data = ""
            filename_label = st.session_state.get("uploaded_filename") or "Direct_Buffer_Input"

            if uploaded_file is not None:
                filename_label = uploaded_file.name
                try:
                    sequence_data = uploaded_file.getvalue().decode("utf-8", errors="replace")
                except Exception as e:
                    st.error(f"Error decoding uploaded file: {str(e)}")
            else:
                sequence_data = input_text if input_text.strip() else st.session_state.sample_fasta

            if not sequence_data.strip():
                st.warning("Please provide a valid sequence string or upload a sequence file.")
            else:
                st.session_state.sample_fasta = sequence_data
                st.session_state.uploaded_filename = filename_label
                st.session_state.ml_sample_input = sequence_data
                st.session_state.last_ml_result = None
                with st.spinner("Processing sequence through local air-gapped screening pipeline..."):
                    parsed = parse_canonical_fasta(sequence_data)

                    if not parsed["is_valid"]:
                        st.error(f"Sequence Validation Error: {parsed['error']}")
                    else:
                        seq_str = parsed["sequence"]
                        seq_len = parsed["length"]
                        seq_hash = parsed["sha256"]

                        # 1. Exact Match Engine
                        matches, exact_ms = search_aho_corasick(AUTOMATON_ROOT, seq_str)

                        # 2. Fuzzy Analysis Engine
                        kmer_counts, kmer_ms = tokenize_kmers(seq_str, k=3)
                        similarity_score, cosine_ms = compute_vector_cosine_similarity(
                            kmer_counts, st.session_state.reference_toxin_weights
                        )
                        safety_threshold = 0.8500
                        has_hazard = (len(matches) > 0) or (similarity_score >= safety_threshold)

                        # 3. Honey-Net & Interlock
                        if has_hazard:
                            hazard_summary = f"{len(matches)} exact motif matches, Cosine Similarity: {similarity_score:.4f}"
                            honeynet_res = execute_honeynet_redirection(seq_hash, hazard_summary)
                            for node in st.session_state.active_nodes:
                                if node["node_id"] == "NODE-SEC-ALPHA-01":
                                    node["status"] = "QUARANTINED // HONEYNET_ISOLATED"
                                    node["quarantine_token"] = f"TOKEN-QT-{seq_hash[:8].upper()}"
                            status_verdict = "THREAT_INTERCEPTED (HONEY-NET REDIRECTED)"
                        else:
                            st.session_state.active_nodes = synchronize_mesh_ledger(
                                st.session_state.active_nodes, st.session_state.homomorphic_db_index
                            )
                            status_verdict = "NOMINAL_CLEARED"

                        # 4. Save to Latest Analysis and History
                        analysis_record = {
                            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "filename": filename_label,
                            "length": seq_len,
                            "sha256": seq_hash,
                            "matches_count": len(matches),
                            "matches": matches,
                            "similarity_score": similarity_score,
                            "safety_threshold": safety_threshold,
                            "has_hazard": has_hazard,
                            "status": status_verdict,
                            "duration_ms": parsed["elapsed_ms"] + exact_ms + kmer_ms + cosine_ms,
                            "exact_ms": exact_ms,
                            "cosine_ms": cosine_ms,
                        }
                        st.session_state.latest_analysis = analysis_record
                        st.session_state.analysis_history.insert(0, analysis_record)

                        # Append to audit logs
                        st.session_state.threat_logs.insert(
                            0,
                            {
                                "timestamp": analysis_record["timestamp"],
                                "channel": "LINE_RATE_GUARD",
                                "signature": f"SIEVE_{seq_hash[:8]}",
                                "detail": f"{filename_label} ({seq_len} bp) screened. Matches: {len(matches)}, Cosine Sim: {similarity_score:.4f}. Verdict: {status_verdict}",
                                "status": "QUARANTINED" if has_hazard else "CLEARED",
                            },
                        )

                res = st.session_state.latest_analysis
                bg_col = "#10243A" if res["has_hazard"] else "#EAF8FB"
                text_col = "#EAF8FB" if res["has_hazard"] else "#102D4D"
                border_col = "#1B3857" if res["has_hazard"] else "#D8EAF0"
                accent_col = "#69D9E8" if res["has_hazard"] else "#168FA1"
                route_str = "inert_sugar_blueprint.gcode (Honey-Net Decoy Override)" if res["has_hazard"] else "Hardware Synthesis Actuation Buffer"

                render_html(f"""
                <div style="background: {bg_col}; color: {text_col}; border: 1.5px solid {border_col}; border-radius: 16px; padding: 22px; margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-weight: 800; font-size: 1.05rem; color: {accent_col};">
                            ANALYSIS COMPLETE: {res['status']}
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.86rem;">
                            DURATION: {res['duration_ms']:.4f} ms
                        </span>
                    </div>
                    <div style="font-size: 0.94rem; line-height: 1.65;">
                        <div><strong>Sequence Length:</strong> {res['length']:,} base pairs | <strong>SHA-256 Digest:</strong> <span style="font-family: monospace;">{res['sha256'][:24]}...</span></div>
                        <div><strong>Exact Blacklist Matches:</strong> {res['matches_count']} found | <strong>Vector Cosine Similarity:</strong> {res['similarity_score']:.4f} (Gate: {res['safety_threshold']:.4f})</div>
                        <div><strong>Routing Destination:</strong> {route_str}</div>
                    </div>
                </div>
                """)

    # --------------------------------------------------------------------------
    # Feature Showcase (Four Layers. One Screening Workflow)
    # --------------------------------------------------------------------------
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    render_html("""
    <div style="text-align: center; margin-bottom: 32px;">
        <span class="section-eyebrow">MODULAR DEFENSE IN DEPTH</span>
        <h2 class="section-headline">
            Four layers. One screening workflow.
        </h2>
        <p class="section-description" style="margin: 0 auto;">
            Explore the components that make up the Bio-Sieve architecture.
        </p>
    </div>
    """)

    # Feature 01: Exact Match
    col_f1_text, col_f1_img = st.columns([1.2, 0.8], gap="medium")
    with col_f1_text:
        with st.container(border=True):
            render_html("""
            <span class="section-eyebrow">FEATURE 01</span>
            <h3 class="feature-title">
                High-Speed Exact Match Filtering
            </h3>
            <p class="feature-description">
                Aho–Corasick-based multi-pattern matching for efficient identification of configured reference patterns.
                Processes continuous nucleotide character sequences in strict linear O(N) time with zero backtracking overhead.
            </p>
            <div class="capability-highlight-badge">
                <span class="badge-dot pulse"></span>
                <span>CAPABILITY: <strong>IMPLEMENTED (O(N) AUTOMATON)</strong></span>
                <span class="badge-sep">/</span>
                <span>LATENCY: <strong>&lt; 0.05 MS</strong></span>
            </div>
            """)
            if st.button("Explore Exact Match", key="btn_exp_exact"):
                navigate_to("Exact Match")

    with col_f1_img:
        render_html(f"""
        <div class="feature-image-fused-container">
            <img src="{IMG_EXACT_MATCH}" alt="Exact Match DNA Strands" class="feature-fused-img" />
        </div>
        """)

    # Feature 02: Fuzzy Analysis (Alternating)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col_f2_img, col_f2_text = st.columns([0.8, 1.2], gap="medium")

    with col_f2_img:
        render_html(f"""
        <div class="feature-image-fused-container">
            <img src="{IMG_FUZZY_ANALYSIS}" alt="Fuzzy Similarity Matrix" class="feature-fused-img" />
        </div>
        """)

    with col_f2_text:
        with st.container(border=True):
            render_html("""
            <span class="section-eyebrow">FEATURE 02</span>
            <h3 class="feature-title">
                Fuzzy Semantic Sequence Matching
            </h3>
            <p class="feature-description">
                K-mer frequency analysis and vector similarity measurements to examine sequence-pattern resemblance beyond exact matches.
                Calculates Euclidean-normalized cosine distance between input token distributions and hazardous reference backbone models.
            </p>
            <div class="capability-highlight-badge">
                <span class="badge-dot pulse"></span>
                <span>CAPABILITY: <strong>IMPLEMENTED (32-BIT K-MER FREQUENCY COSINE VECTOR)</strong></span>
                <span class="badge-sep">/</span>
                <span>GATE: <strong>0.8500</strong></span>
            </div>
            """)
            if st.button("Explore Fuzzy Analysis", key="btn_exp_fuzzy"):
                navigate_to("Fuzzy Analysis")

    # Feature 03: Secure Enclave
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col_f3_text, col_f3_img = st.columns([1.2, 0.8], gap="medium")

    with col_f3_text:
        with st.container(border=True):
            render_html("""
            <span class="section-eyebrow">FEATURE 03</span>
            <h3 class="feature-title">
                Hardware Enclosure & Zero-Knowledge Verification (TEE)
            </h3>
            <p class="feature-description">
                A dedicated workspace for examining execution-isolation assumptions, verification evidence, trust boundaries, and security configuration.
                Illustrates software-level isolation boundaries while clearly identifying that hardware-backed TEE attestation requires specific server hardware.
            </p>
            <div class="capability-highlight-badge badge-warning">
                <span class="badge-dot-amber"></span>
                <span>STATUS: <strong>SOFTWARE EMULATION ONLY</strong></span>
                <span class="badge-sep">/</span>
                <span>HARDWARE ATTESTATION: <strong>SIMULATION DEMO</strong></span>
            </div>
            """)
            if st.button("Explore Secure Enclave", key="btn_exp_enclave"):
                navigate_to("Secure Enclave")

    with col_f3_img:
        render_html(f"""
        <div class="feature-image-fused-container">
            <img src="{IMG_SECURE_ENCLAVE}" alt="Hardware Enclave Silicon" class="feature-fused-img" />
        </div>
        """)

    # Feature 04: Homomorphic Sync
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col_f4_img, col_f4_text = st.columns([0.8, 1.2], gap="medium")

    with col_f4_img:
        render_html(f"""
        <div class="feature-image-fused-container">
            <img src="{IMG_HOMOMORPHIC_SYNC}" alt="Decentralized Cryptographic Mesh" class="feature-fused-img" />
        </div>
        """)

    with col_f4_text:
        with st.container(border=True):
            render_html("""
            <span class="section-eyebrow">FEATURE 04</span>
            <h3 class="feature-title">
                Homomorphic Updates & Ephemeral Honey-Nets
            </h3>
            <p class="feature-description">
                A workspace for reviewing reference-index updates, integrity checks, isolated decoy workflows, and update provenance.
                Simulates additive coefficient merges from one-way satellite streams and redirects detected hazards to inert carrier structures.
            </p>
            <div class="capability-highlight-badge badge-warning">
                <span class="badge-dot-amber"></span>
                <span>STATUS: <strong>SIMULATED ADDITIVE FHE MODEL</strong></span>
                <span class="badge-sep">/</span>
                <span>HONEY-NET: <strong>ACTIVE G-CODE OVERRIDE</strong></span>
            </div>
            """)
            if st.button("Explore Homomorphic Sync", key="btn_exp_sync"):
                navigate_to("Homomorphic Sync")

    # --------------------------------------------------------------------------
    # Architecture Diagram
    # --------------------------------------------------------------------------
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        render_html("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1.5px solid #D8EAF0;">
            <div>
                <span class="section-eyebrow">SYSTEM BLUEPRINT</span>
                <div class="card-title">Inside the Bio-Sieve architecture</div>
                <div class="card-subtitle">Transparent data flow separating core verified algorithmic pipelines from simulated hardware security boundaries.</div>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.84rem; color: #168FA1; font-weight: 700; background: #EAF8FB; padding: 5px 14px; border-radius: 9999px;">
                ZERO-TRUST AUDIT MODEL
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin: 24px 0; overflow-x: auto; padding: 12px 0;">
            <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 18px; flex: 1; text-align: center;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase;">1. Ingestion</div>
                <div style="font-size: 0.98rem; font-weight: 800; color: #102D4D; margin: 4px 0;">Sequence Input</div>
                <div style="font-size: 0.84rem; color: #536D82;">FASTA / Canonical Buffer</div>
            </div>
            <div style="display: flex; align-items: center; color: #168FA1;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#168FA1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </div>
            <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 18px; flex: 1; text-align: center;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase;">2. Parser</div>
                <div style="font-size: 0.98rem; font-weight: 800; color: #102D4D; margin: 4px 0;">Canonicalization</div>
                <div style="font-size: 0.84rem; color: #536D82;">SHA-256 Digest</div>
            </div>
            <div style="display: flex; align-items: center; color: #168FA1;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#168FA1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </div>
            <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 18px; flex: 1; text-align: center;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase;">3. Filtering</div>
                <div style="font-size: 0.98rem; font-weight: 800; color: #102D4D; margin: 4px 0;">Exact Match</div>
                <div style="font-size: 0.84rem; color: #536D82;">Aho-Corasick Automaton</div>
            </div>
            <div style="display: flex; align-items: center; color: #168FA1;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#168FA1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </div>
            <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 18px; flex: 1; text-align: center;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #168FA1; text-transform: uppercase;">4. Math Sieve</div>
                <div style="font-size: 0.98rem; font-weight: 800; color: #102D4D; margin: 4px 0;">Similarity Analysis</div>
                <div style="font-size: 0.84rem; color: #536D82;">3-Mer Cosine Vector</div>
            </div>
            <div style="display: flex; align-items: center; color: #168FA1;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#168FA1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </div>
            <div style="background: #10243A; color: #FFFFFF; border: 1.5px solid #1B3857; border-radius: 14px; padding: 18px; flex: 1.2; text-align: center;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #69D9E8; text-transform: uppercase;">5. Gating & Interlock</div>
                <div style="font-size: 0.98rem; font-weight: 800; color: #FFFFFF; margin: 4px 0;">Policy Evaluation</div>
                <div style="font-size: 0.84rem; color: #A0C0D8;">Synthesis or Honey-Net Decoy</div>
            </div>
        </div>
        <div style="background: #F7FCFD; border-radius: 12px; padding: 16px 20px; font-size: 0.90rem; color: #536D82; line-height: 1.65;">
            <strong>Architectural Note:</strong> Stages 1–4 are fully executed by native Python algorithmic implementations in memory.
            Stage 5 performs either safe synthesis buffer release or silent file override to <code>inert_sugar_blueprint.gcode</code>.
            Hardware Enclave boundaries and Satellite FHE Delta Streams are demonstration modules modeling production trust boundaries.
        </div>
        """)

    # Final CTA Section
    render_html("""
    <div style="background: linear-gradient(135deg, #102D4D 0%, #168FA1 100%); border-radius: 24px; padding: 48px; color: #FFFFFF; text-align: center; margin-top: 36px; box-shadow: 0 16px 40px rgba(16, 45, 77, 0.12);">
        <h2 style="font-size: 2.4rem; font-weight: 900; margin-bottom: 12px; letter-spacing: -0.02em;">
            Bring a sequence into the screening workflow.
        </h2>
        <p style="font-size: 1.08rem; color: #D1F7FC; max-width: 640px; margin: 0 auto; line-height: 1.65;">
            Evaluate genetic sequence payloads with deterministic linear-time inspection and privacy-preserving local execution.
        </p>
    </div>
    """)


# ==============================================================================
# 6. PAGE 2: HIGH-SPEED EXACT MATCH FILTERING
# ==============================================================================
def render_page_exact_match():
    """Renders the dedicated Exact Match Filtering analytical workspace."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">DIAGNOSTIC CHANNEL 01</span>
        <h1 class="section-headline">
            High-Speed Exact Match Filtering
        </h1>
        <p class="section-description">
            Aho–Corasick multi-pattern search automaton for deterministic O(N) pathogen signature identification.
        </p>
    </div>
    """)

    col_input, col_results = st.columns([1.1, 1.4], gap="medium")

    with col_input:
        with st.container(border=True):
            render_html("""
            <div class="card-title">Sequence Ingestion & Input</div>
            <div class="card-subtitle">Upload a valid FASTA sequence file or load configured test controls.</div>
            """)

            st.download_button(
                label="📥 Download Sample File for Ingestion",
                data=SAMPLE_SPECIMEN_FASTA,
                file_name="synthetic_biosecurity_specimen.fasta",
                mime="text/plain",
                type="primary",
                use_container_width=True,
                help="Download the verified synthetic FASTA specimen file for exact match screening.",
                key="exact_dl_sample_btn",
            )
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

            up_file_exact = st.file_uploader(
                "Upload FASTA File",
                type=["fasta", "fa", "txt"],
                key="exact_file_uploader",
            )

            if up_file_exact is not None:
                try:
                    file_text = up_file_exact.getvalue().decode("utf-8", errors="replace")
                    if file_text != st.session_state.get("sample_fasta", "") or up_file_exact.name != st.session_state.get("uploaded_filename", ""):
                        st.session_state.sample_fasta = file_text
                        st.session_state.uploaded_filename = up_file_exact.name
                        st.session_state.ml_sample_input = file_text
                        st.session_state.last_ml_result = None
                except Exception as e:
                    st.error(f"Error decoding uploaded file: {str(e)}")

            if st.session_state.get("uploaded_filename"):
                render_html(f"""
                <div style="background: #EAF8FB; border: 1.5px solid #168FA1; border-radius: 10px; padding: 10px 14px; margin: 10px 0 14px 0; font-size: 0.86rem; color: #102D4D;">
                    <strong>Active Specimen:</strong> <code>{st.session_state.uploaded_filename}</code> ({len(st.session_state.sample_fasta):,} bp)
                    <div style="font-size: 0.78rem; color: #536D82; margin-top: 2px;">Synchronized from Ingestion Gateway across all screening modules.</div>
                </div>
                """)

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Load Hazardous Specimen", key="btn_hazard_exact", use_container_width=True):
                    st.session_state.sample_fasta = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state["exact_text_area"] = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state.uploaded_filename = "Hazardous_Synthetic_Backbone.fasta"
                    st.session_state.ml_sample_input = HAZARDOUS_REFERENCE_BACKBONE
                    st.session_state.last_ml_result = None
                    st.rerun()
            with col_b2:
                if st.button("Load Benign Control", key="btn_benign_exact", use_container_width=True):
                    st.session_state.sample_fasta = SAMPLE_BENIGN_SEQUENCE
                    st.session_state["exact_text_area"] = SAMPLE_BENIGN_SEQUENCE
                    st.session_state.uploaded_filename = "Benign_Control_Actin1.fasta"
                    st.session_state.ml_sample_input = SAMPLE_BENIGN_SEQUENCE
                    st.session_state.last_ml_result = None
                    st.rerun()

            exact_fasta_input = st.text_area(
                "Canonical FASTA Input Buffer",
                value=st.session_state.get("exact_text_area") or st.session_state.get("sample_fasta", ""),
                height=180,
                key="exact_text_area",
            )

            col_run, col_reset = st.columns([1.5, 1.0])
            with col_run:
                run_exact_btn = st.button("Run Exact Match Analysis", type="primary", use_container_width=True, key="run_exact_btn")
            with col_reset:
                if st.button("Reset Input", use_container_width=True, key="reset_exact_btn"):
                    st.session_state.sample_fasta = ""
                    st.session_state["exact_text_area"] = ""
                    st.session_state.uploaded_filename = ""
                    st.session_state.ml_sample_input = ""
                    st.session_state.last_ml_result = None
                    st.rerun()

            render_html("""
            <div style="font-size: 0.88rem; color: #536D82; margin-top: 14px; line-height: 1.55;">
                [AIR-GAP SECURED] <strong>Privacy Assurance:</strong> Sequence data is parsed locally in volatile memory. No outbound API requests are made.
            </div>
            """)

    with col_results:
        # Pipeline Stepper Visualization
        render_html("""
        <div class="stepper-container">
            <div class="step-node active"><div class="step-circle">1</div>Input</div>
            <div class="step-node active"><div class="step-circle">2</div>Format</div>
            <div class="step-node active"><div class="step-circle">3</div>FASTA Parse</div>
            <div class="step-node active"><div class="step-circle">4</div>SHA-256</div>
            <div class="step-node active"><div class="step-circle">5</div>Aho-Corasick</div>
            <div class="step-node active"><div class="step-circle">6</div>Results</div>
        </div>
        """)

        seq_to_process = exact_fasta_input.strip() if exact_fasta_input.strip() else st.session_state.get("sample_fasta", "").strip()
        label_name = st.session_state.get("uploaded_filename") or "Direct_Buffer_Input"
        should_render_exact = run_exact_btn or (len(seq_to_process) > 0)

        if should_render_exact:
            if not seq_to_process.strip():
                st.warning("Please supply a valid sequence string or file.")
            else:
                parsed = parse_canonical_fasta(seq_to_process)
                if not parsed["is_valid"]:
                    st.error(f"Input Validation Failed: {parsed['error']}")
                else:
                    seq_str = parsed["sequence"]
                    seq_len = parsed["length"]
                    seq_hash = parsed["sha256"]

                    # Run exact match automaton
                    matches, latency_ms = search_aho_corasick(AUTOMATON_ROOT, seq_str)

                    # Update telemetry
                    st.session_state.performance_telemetry["fasta_parse_ms"] = parsed["elapsed_ms"]
                    st.session_state.performance_telemetry["automaton_ms"] = latency_ms

                    # Log to history if button was pressed or history empty
                    if run_exact_btn or not st.session_state.analysis_history:
                        record = {
                            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "filename": label_name,
                            "length": seq_len,
                            "sha256": seq_hash,
                            "matches_count": len(matches),
                            "matches": matches,
                            "status": f"{len(matches)} MATCHES IDENTIFIED" if matches else "0 MATCHES (CLEARED)",
                            "duration_ms": parsed["elapsed_ms"] + latency_ms,
                        }
                        if not any(h.get("sha256") == seq_hash and h.get("matches_count") == len(matches) for h in st.session_state.analysis_history[:2]):
                            st.session_state.analysis_history.insert(0, record)

                    # Render Metrics Row
                    c_m1, c_m2, c_m3 = st.columns(3)
                    with c_m1:
                        st.metric("SEQUENCE LENGTH", f"{seq_len:,} bp")
                    with c_m2:
                        st.metric("EXACT MATCHES", f"{len(matches)} found")
                    with c_m3:
                        st.metric("AUTOMATON SPEED", f"{latency_ms:.4f} ms")

                    # Cryptographic Digest Panel
                    render_html(f"""
                    <div class="diagnostic-panel" style="margin-top: 14px;">
                        <div class="diagnostic-panel-header">
                            <span>CRYPTOGRAPHIC SEQUENCE IDENTIFIER</span>
                            <span>SHA-256</span>
                        </div>
                        <div style="word-break: break-all; font-weight: 700; color: #FFFFFF;">
                            {seq_hash}
                        </div>
                    </div>
                    """)

                    # Results Table
                    if matches:
                        rows = "".join(
                            [
                                f"<tr>"
                                f"<td><strong>#{idx+1}</strong></td>"
                                f"<td style='font-family: monospace; font-weight: 800; color: #168FA1;'>{m['pattern']}</td>"
                                f"<td>{m['label']}</td>"
                                f"<td style='font-family: monospace;'>[{m['start_index']} : {m['end_index']}]</td>"
                                f"<td>{m['length']} bp</td>"
                                f"</tr>"
                                for idx, m in enumerate(matches)
                            ]
                        )

                        with st.container(border=True):
                            render_html(f"""
                            <div class="card-title">Identified Watchlist Signatures ({len(matches)})</div>
                            <div class="card-subtitle">Exact matching substrings found in linear scan across {len(HAZARDOUS_WATCHLIST)} configured references.</div>
                            <table class="bio-table">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>MATCHED MOTIF</th>
                                        <th>HAZARD CLASSIFICATION</th>
                                        <th>COORDINATES</th>
                                        <th>LENGTH</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {rows}
                                </tbody>
                            </table>
                            """)
                    else:
                        render_html(f"""
                        <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 16px; padding: 24px; text-align: center; color: #102D4D;">
                            <div style="font-size: 1.25rem; font-weight: 800; color: #168FA1; margin-bottom: 8px;">
                                ZERO WATCHLIST SIGNATURES DETECTED
                            </div>
                            <div style="font-size: 0.96rem; color: #536D82; line-height: 1.6;">
                                The Aho-Corasick automaton traversed all {seq_len:,} characters across {len(HAZARDOUS_WATCHLIST)} reference patterns in {latency_ms:.4f} ms with zero exact matches.
                            </div>
                        </div>
                        """)

                    # Export Report
                    report_dict = {
                        "audit_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "analysis_type": "Exact_Match_Aho_Corasick",
                        "input_label": label_name,
                        "sequence_length_bp": seq_len,
                        "sha256_digest": seq_hash,
                        "watchlist_size": len(HAZARDOUS_WATCHLIST),
                        "matches_found": len(matches),
                        "matches_detail": matches,
                        "execution_latency_ms": latency_ms,
                    }
                    st.download_button(
                        label="Download Analysis Report (JSON)",
                        data=json.dumps(report_dict, indent=2),
                        file_name=f"bio_sieve_exact_report_{seq_hash[:8]}.json",
                        mime="application/json",
                        key="dl_exact_report",
                    )
        else:
            with st.container(border=True):
                render_html("""
                <div style="text-align: center; padding: 36px;">
                    <div style="font-size: 1.20rem; font-weight: 800; color: #102D4D; margin-bottom: 8px;">
                        Awaiting Sequence Execution
                    </div>
                    <div style="font-size: 0.96rem; color: #536D82; max-width: 440px; margin: 0 auto; line-height: 1.6;">
                        Click <strong>Run Exact Match Analysis</strong> on the left panel to execute the Aho-Corasick linear-time screening automaton.
                    </div>
                </div>
                """)


# ==============================================================================
# 7. PAGE 3: FUZZY SEMANTIC SEQUENCE MATCHING
# ==============================================================================
def render_page_fuzzy_analysis():
    """Renders the transparent mathematical vector similarity workspace."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">DIAGNOSTIC CHANNEL 02</span>
        <h1 class="section-headline">
            Fuzzy Semantic Sequence Matching
        </h1>
        <p class="section-description">
            Examine sequence similarity through transparent mathematical analysis.
        </p>
    </div>
    <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 16px 22px; font-size: 0.92rem; color: #102D4D; margin-bottom: 24px; line-height: 1.6;">
        <strong>Important Scientific Clarification:</strong> K-mer frequency analysis is a mathematical comparison of sequence composition vectors.
        It does not constitute semantic biological understanding or certified pathogenicity risk determination on its own.
    </div>
    """)

    col_ctrl, col_math = st.columns([1.1, 1.4], gap="medium")

    with col_ctrl:
        with st.container(border=True):
            render_html("""
            <div class="card-title">Similarity Model Parameters</div>
            <div class="card-subtitle">Configure k-mer window geometry and reference baseline profile.</div>
            """)

            k_val = st.slider("K-Mer Token Window Size (k)", min_value=2, max_value=4, value=3, step=1)
            ref_model = st.selectbox(
                "Reference Target Baseline Profile",
                [
                    f"Restricted Pathogen Backbone Model (v{st.session_state.homomorphic_db_index:.1f})",
                    "Standard Calibration Reference Backbone (Static)",
                ],
            )

            sim_method = st.selectbox(
                "Vector Distance Metric",
                [
                    "Euclidean-Normalized Cosine Distance",
                ],
            )

            threshold_val = st.slider(
                "Tripwire Gate Threshold", min_value=0.50, max_value=0.99, value=0.85, step=0.01
            )

            active_name = st.session_state.get("uploaded_filename") or "Benign_Control_Actin1.fasta"
            active_seq = st.session_state.get("sample_fasta") or SAMPLE_BENIGN_SEQUENCE
            render_html(f"""
            <div style="background: #EAF8FB; border: 1.5px solid #168FA1; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-size: 0.86rem; color: #102D4D;">
                <strong>Active Specimen:</strong> <code>{active_name}</code> ({len(active_seq):,} bp)
                <div style="font-size: 0.78rem; color: #536D82; margin-top: 2px;">Synchronized from Ingestion Gateway across all screening modules.</div>
            </div>
            """)

            fuzzy_input_text = st.text_area(
                "FASTA Sequence Input",
                value=st.session_state.get("sample_fasta") or SAMPLE_BENIGN_SEQUENCE,
                height=150,
                key="fuzzy_text_area",
            )

            run_fuzzy_btn = st.button("Run Fuzzy Similarity Analysis", type="primary", use_container_width=True, key="run_fuzzy_btn")

    with col_math:
        seq_to_check = fuzzy_input_text.strip() if fuzzy_input_text.strip() else st.session_state.get("sample_fasta", "").strip()
        should_render_fuzzy = run_fuzzy_btn or (len(seq_to_check) > 0)

        if should_render_fuzzy:
            parsed = parse_canonical_fasta(seq_to_check)
            if not parsed["is_valid"]:
                st.error(f"Input Error: {parsed['error']}")
            else:
                seq_str = parsed["sequence"]
                seq_len = parsed["length"]
                seq_hash = parsed["sha256"]

                # Run K-mer tokenization
                kmer_counts, t_token_ms = tokenize_kmers(seq_str, k=k_val)
                total_kmers = sum(kmer_counts.values())
                unique_kmers = len(kmer_counts)

                # Compute Cosine Similarity
                sim_score, t_cosine_ms = compute_vector_cosine_similarity(
                    kmer_counts, st.session_state.reference_toxin_weights
                )
                margin = threshold_val - sim_score
                is_flagged = sim_score >= threshold_val

                # Update performance telemetry
                st.session_state.performance_telemetry["tokenizer_ms"] = t_token_ms
                st.session_state.performance_telemetry["cosine_math_ms"] = t_cosine_ms
                st.session_state.performance_telemetry["last_similarity_score"] = sim_score
                st.session_state.performance_telemetry["safety_margin"] = margin

                # Metrics row
                c_s1, c_s2, c_s3 = st.columns(3)
                with c_s1:
                    st.metric("SIMILARITY SCORE", f"{sim_score:.4f}")
                with c_s2:
                    st.metric("THRESHOLD GATE", f"{threshold_val:.4f}")
                with c_s3:
                    st.metric("SAFETY MARGIN", f"{margin:.4f}")

                # Status box
                flag_title = "[FLAGGED] SIMILARITY EXCEEDS SENSITIVITY GATE" if is_flagged else "[CLEARED] VECTOR SIMILARITY WITHIN SAFE TOLERANCE"
                flag_bg = "#10243A" if is_flagged else "#EAF8FB"
                flag_fg = "#EAF8FB" if is_flagged else "#102D4D"
                flag_acc = "#69D9E8" if is_flagged else "#168FA1"

                render_html(f"""
                <div style="background: {flag_bg}; color: {flag_fg}; border-radius: 16px; padding: 22px; margin: 16px 0;">
                    <div style="font-weight: 800; font-size: 1.05rem; color: {flag_acc}; margin-bottom: 8px;">
                        {flag_title}
                    </div>
                    <div style="font-size: 0.94rem; line-height: 1.65;">
                        Calculated vector cosine similarity: <strong>{sim_score:.4f}</strong> vs configured threshold <strong>{threshold_val:.4f}</strong>.
                        K-mer extraction: {total_kmers:,} overlapping tokens generated in {t_token_ms:.4f} ms.
                    </div>
                </div>
                """)

                # Feature Vector Breakdown Table
                top_tokens = kmer_counts.most_common(8)
                rows_k = "".join(
                    [
                        f"<tr>"
                        f"<td style='font-weight: 800; font-family: monospace;'>{k_tok}</td>"
                        f"<td>{cnt:,}</td>"
                        f"<td>{(cnt / total_kmers * 100.0):.2f}%</td>"
                        f"<td style='font-family: monospace;'>{(cnt / math.sqrt(sum(v*v for v in kmer_counts.values()))):.4f}</td>"
                        f"</tr>"
                        for k_tok, cnt in top_tokens
                    ]
                )

                with st.container(border=True):
                    render_html(f"""
                    <div class="card-title">K-Mer Distribution Vector Profile</div>
                    <div class="card-subtitle">Highest frequency tokens across canonical nucleotide vocabulary.</div>
                    <table class="bio-table">
                        <thead>
                            <tr>
                                <th>TOKEN (k={k_val})</th>
                                <th>RAW FREQUENCY</th>
                                <th>SHARE (%)</th>
                                <th>NORMALIZED L2 WEIGHT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_k}
                        </tbody>
                    </table>
                    """)

                # Export report
                fuzzy_report = {
                    "audit_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "analysis_type": "Fuzzy_Cosine_Vector_Screening",
                    "sequence_length": seq_len,
                    "sha256": seq_hash,
                    "k_value": k_val,
                    "total_tokens": total_kmers,
                    "unique_vocabulary": unique_kmers,
                    "similarity_score": sim_score,
                    "gate_threshold": threshold_val,
                    "is_flagged": is_flagged,
                    "duration_ms": t_token_ms + t_cosine_ms,
                }
                st.download_button(
                    label="Download Similarity Analysis Report (JSON)",
                    data=json.dumps(fuzzy_report, indent=2),
                    file_name=f"bio_sieve_fuzzy_report_{seq_hash[:8]}.json",
                    mime="application/json",
                    key="dl_fuzzy_report",
                )
        else:
            with st.container(border=True):
                render_html("""
                <div style="text-align: center; padding: 36px;">
                    <div style="font-size: 1.20rem; font-weight: 800; color: #102D4D; margin-bottom: 8px;">
                        Analytical Workspace Ready
                    </div>
                    <div style="font-size: 0.96rem; color: #536D82; max-width: 440px; margin: 0 auto; line-height: 1.6;">
                        Click <strong>Run Fuzzy Similarity Analysis</strong> to compute the Euclidean-normalized vector cosine similarity.
                    </div>
                </div>
                """)


# ==============================================================================
# 7B. PAGE: ML OPERATIONS & COMPUTATIONAL COMPLEXITY SIMULATION
# ==============================================================================
def render_page_ml_operations():
    """Renders the AI/ML & Computational Physics Subsystem Showcase for Judges."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">AI/ML & COMPUTATIONAL COMPLEXITY ENGINE</span>
        <h1 class="section-headline">
            ML Operations & Physics Simulator
        </h1>
        <p class="section-description">
            Fully offline, air-gapped machine learning and computational physics pipeline.
            Executes non-contiguous fragment affinity de-shuffling, microchannel thermal-fluidic simulation,
            and ephemeral honey-net molecular neutralization.
        </p>
    </div>
    """)

    # 1. Preset Selector & Sequence Input
    with st.container(border=True):
        render_html("""
        <div class="card-title">Sequence Ingestion & Simulation Controls</div>
        <div class="card-subtitle">Select a demonstration preset or submit an arbitrary nucleotide sequence for runtime mathematical evaluation.</div>
        """)

        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1:
            if st.button("Load Benign Control (Actin-1)", key="ml_p_benign", use_container_width=True):
                st.session_state.ml_sample_input = SAMPLE_BENIGN_SEQUENCE
                st.session_state["ml_seq_buffer"] = SAMPLE_BENIGN_SEQUENCE
                st.session_state.sample_fasta = SAMPLE_BENIGN_SEQUENCE
                st.session_state.uploaded_filename = "Benign_Control_Actin1.fasta"
                st.session_state.last_ml_result = None
                st.session_state.ml_physics.reset_interlock()
                st.rerun()
        with col_p2:
            if st.button("Load Interleaved Stego Payload", key="ml_p_stego", use_container_width=True):
                f1 = "ATGCGTACGTTAGCTACGTAGC"
                f2 = "CGTACGATCGATCGATCGATCG"
                stego_val = "".join(a + b for a, b in zip(f1, f2))
                st.session_state.ml_sample_input = stego_val
                st.session_state["ml_seq_buffer"] = stego_val
                st.session_state.sample_fasta = stego_val
                st.session_state.uploaded_filename = "Interleaved_Stego_Payload.fasta"
                st.session_state.last_ml_result = None
                st.rerun()
        with col_p3:
            if st.button("Load High-Stress Interlock Tripper", key="ml_p_trip", use_container_width=True):
                trip_val = "ACGT" * 400 + "GATC" * 300 + "TTAG" * 200 + "CCTA" * 150
                st.session_state.ml_sample_input = trip_val
                st.session_state["ml_seq_buffer"] = trip_val
                st.session_state.sample_fasta = trip_val
                st.session_state.uploaded_filename = "High_Stress_Tripper.fasta"
                st.session_state.last_ml_result = None
                st.rerun()
        with col_p4:
            if st.button("Load Hazardous Motif Specimen", key="ml_p_hazard", use_container_width=True):
                st.session_state.ml_sample_input = HAZARDOUS_REFERENCE_BACKBONE
                st.session_state["ml_seq_buffer"] = HAZARDOUS_REFERENCE_BACKBONE
                st.session_state.sample_fasta = HAZARDOUS_REFERENCE_BACKBONE
                st.session_state.uploaded_filename = "Hazardous_Synthetic_Backbone.fasta"
                st.session_state.last_ml_result = None
                st.rerun()

        if st.session_state.get("uploaded_filename"):
            render_html(f"""
            <div style="background: #EAF8FB; border: 1.5px solid #168FA1; border-radius: 10px; padding: 10px 14px; margin-top: 10px; font-size: 0.86rem; color: #102D4D;">
                <strong>Active Specimen:</strong> <code>{st.session_state.uploaded_filename}</code> ({len(st.session_state.sample_fasta):,} bp)
                <div style="font-size: 0.78rem; color: #536D82; margin-top: 2px;">Synchronized from Ingestion Gateway across all screening modules.</div>
            </div>
            """)

        default_input = st.session_state.get("ml_seq_buffer") or st.session_state.get("ml_sample_input") or st.session_state.get("sample_fasta") or SAMPLE_BENIGN_SEQUENCE
        seq_input = st.text_area(
            "Target Sequence Buffer",
            value=default_input,
            height=120,
            key="ml_seq_buffer",
            placeholder="Enter or paste FASTA sequence...",
        )
        st.session_state.ml_sample_input = seq_input

        col_run, col_reset, col_status = st.columns([1.5, 1.2, 2.5], vertical_alignment="center")
        with col_run:
            run_btn = st.button("Run Full ML & Physics Simulation", key="btn_run_ml_sim", type="primary", use_container_width=True)
        with col_reset:
            if st.button("Reset Interlock State", key="btn_reset_interlock_ml", use_container_width=True):
                st.session_state.ml_physics.reset_interlock()
                st.success("Interlock relay reset to ARMED // NOMINAL.")
                st.rerun()
        with col_status:
            current_state = st.session_state.ml_physics.interlock_state
            if current_state == InterlockState.TRIPPED:
                st.markdown("<span style='color: #DC2626; font-weight: 800; font-family: monospace;'>INTERLOCK: ENGAGED // TRIPPED (SAFETY OVERRIDE)</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: #168FA1; font-weight: 800; font-family: monospace;'>INTERLOCK: ARMED // NOMINAL (SAFETY ENVELOPE SECURE)</span>", unsafe_allow_html=True)

    # Process and Render Results
    clean_seq = "".join(line.strip() for line in seq_input.splitlines() if not line.strip().startswith(">"))
    if not clean_seq:
        clean_seq = "ATGC"

    if run_btn or st.session_state.last_ml_result is None:
        with st.spinner("Computing dynamic affinity matrix, microchannel fluidics, and validation tokens..."):
            aff_res = st.session_state.ml_analyzer.analyze(clean_seq)
            phys_res = st.session_state.ml_physics.simulate(
                input_length=aff_res.input_length,
                shannon_entropy=aff_res.stats.shannon_entropy,
                normalized_entropy=aff_res.stats.normalized_entropy,
            )
            val_res = st.session_state.ml_validation_engine.validate_and_process(
                raw_input=clean_seq,
                affinity_result=aff_res,
                telemetry=phys_res,
            )
            st.session_state.last_ml_result = {
                "affinity": aff_res,
                "telemetry": phys_res,
                "validation": val_res,
            }

    res = st.session_state.last_ml_result
    if res:
        aff = res["affinity"]
        phys = res["telemetry"]
        val = res["validation"]

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # DYNAMIC PIPELINE EXECUTION TELEMETRY
        # ----------------------------------------------------------------------
        total_pipeline_ms = round(aff.execution_time_ms + phys.execution_time_ms + val.execution_time_ms, 3)
        render_html(f"""
        <div style="background: #EAF8FB; border: 1.5px solid #69D9E8; border-radius: 12px; padding: 12px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; color: #102D4D;">
                <strong>REAL-TIME EXECUTION TIMING:</strong> Total Elapsed: <span style="color: #168FA1; font-weight: 800;">{total_pipeline_ms:.2f} ms</span>
                <span style="color: #94A3B8; margin: 0 8px;">|</span>
                Affinity Analyzer: <strong>{aff.execution_time_ms:.2f} ms</strong>
                <span style="color: #94A3B8; margin: 0 8px;">|</span>
                Physics Interlock: <strong>{phys.execution_time_ms:.2f} ms</strong>
                <span style="color: #94A3B8; margin: 0 8px;">|</span>
                Safe Spooler Engine: <strong>{val.execution_time_ms:.2f} ms</strong>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.80rem; background: #168FA1; color: #FFFFFF; padding: 4px 12px; border-radius: 6px; font-weight: 700;">
                AIR-GAPPED // ZERO EXTERNAL REQUESTS
            </div>
        </div>
        """)

        # ----------------------------------------------------------------------
        # SUBSYSTEM 1: FRAGMENT AFFINITY ANALYZER
        # ----------------------------------------------------------------------
        with st.container(border=True):
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1.5px solid #D8EAF0; padding-bottom: 10px;">
                <div>
                    <span class="section-eyebrow">MODULE 1 // COMPUTATIONAL COMPLEXITY</span>
                    <div class="card-title">Steganographic Fragment De-shuffler & Affinity Matrix</div>
                    <div class="card-subtitle">Non-contiguous window scanning, Shannon entropy, and dynamic token bonding affinity matrix.</div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; background: #EAF8FB; color: #168FA1; padding: 6px 14px; border-radius: 9999px; font-weight: 700;">
                    STRIDES: [1, 2, 3, 4, 5]
                </div>
            </div>
            """)

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Sequence Length", f"{aff.input_length:,} bp", help="Total input nucleotide count")
                st.metric("Shannon Entropy (H)", f"{aff.stats.shannon_entropy:.4f} bits", help="H = -sum(p * log2(p))")
            with col_m2:
                st.metric("Normalized Entropy", f"{aff.stats.normalized_entropy:.4f}", help="Entropy normalized to alphabet size")
                st.metric("Complexity Ratio", f"{aff.stats.compression_ratio:.4f}", help="Lempel-Ziv algorithmic complexity")
            with col_m3:
                st.metric("Mean Off-Diagonal Affinity", f"{aff.mean_affinity_score * 100.0:.2f}%", help="Average pair binding affinity")
                st.metric("Peak Affinity", f"{aff.max_affinity_score * 100.0:.2f}%", help="Maximum off-diagonal token affinity")
            with col_m4:
                st.metric("De-shuffle Confidence", f"{aff.reconstruction_confidence * 100.0:.2f}%", help="Reconstruction continuity score")
                st.metric("Matrix Dimensions", f"{aff.matrix_dimensions[0]} x {aff.matrix_dimensions[1]}", help="Derived dynamically at runtime")

            # Character Frequency Distribution Row
            freq_items = "".join(
                f"<span style='background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 6px; padding: 3px 8px; margin-right: 8px; font-family: monospace; font-size: 0.84rem; color: #0F172A;'><strong>'{tok}'</strong>: {pct:.1%} ({aff.stats.counts.get(tok, 0)})</span>"
                for tok, pct in list(aff.stats.frequencies.items())[:8]
            )
            render_html(f"""
            <div style="margin: 10px 0 14px 0; font-size: 0.88rem; color: #334155;">
                <span style="font-weight: 700; color: #102D4D; margin-right: 8px;">CHARACTER FREQUENCY DISTRIBUTION (|Σ| = {aff.stats.unique_tokens}):</span>
                {freq_items}
            </div>
            """)

            # Stego status banner
            if aff.is_fragmentation_detected:
                render_html("""
                <div style="background: #FEF3C7; border: 1.5px solid #F59E0B; border-radius: 12px; padding: 12px 18px; color: #92400E; font-weight: 700; margin: 14px 0; font-size: 0.92rem; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.2rem;">⚠️</span>
                    <span><strong>NON-CONTIGUOUS FRAGMENTATION DETECTED:</strong> Phased periodic offset slices detected across configured strides. Camouflage matrix stripped and target sequence reassembled.</span>
                </div>
                """)
            else:
                render_html("""
                <div style="background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 12px; padding: 12px 18px; color: #166534; font-weight: 700; margin: 14px 0; font-size: 0.92rem; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.2rem;">✓</span>
                    <span><strong>HOMOGENEOUS SEQUENCE FLOW:</strong> Zero phased steganographic fragment anomalies detected. Base continuity confirmed.</span>
                </div>
                """)

            # Dynamic Bonding Affinity Matrix Table
            st.markdown("<div style='font-size: 0.92rem; font-weight: 800; color: #102D4D; margin: 12px 0 6px 0;'>DYNAMIC TOKEN BONDING AFFINITY MATRIX (SAMPLE SLICE)</div>", unsafe_allow_html=True)
            dim = min(len(aff.token_labels), 6)
            if dim > 0:
                header_cols = "".join(f"<th style='text-align: center; padding: 8px 12px; background: #F8FAFC;'>{lbl}</th>" for lbl in aff.token_labels[:dim])
                rows_html = ""
                for r in range(dim):
                    r_lbl = aff.token_labels[r]
                    cells = "".join(
                        f"<td style='text-align: center; padding: 8px 12px; background: rgba(22, 143, 161, {max(0.05, min(0.45, aff.affinity_matrix[r][c]))}); font-weight: 700; font-family: monospace;'>{aff.affinity_matrix[r][c]:.2f}</td>"
                        for c in range(dim)
                    )
                    rows_html += f"<tr><td style='font-weight: 800; padding: 8px 12px; background: #F8FAFC;'>{r_lbl}</td>{cells}</tr>"

                render_html(f"""
                <div style="overflow-x: auto; border: 1.5px solid #D8EAF0; border-radius: 10px; margin-bottom: 12px;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                        <thead>
                            <tr><th style="padding: 8px 12px; background: #F8FAFC;">TOKEN</th>{header_cols}</tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
                """)

            with st.expander("Inspect Reconstructed Sequence & Fragment De-Shuffling", expanded=False):
                st.markdown(f"**Reconstructed Sequence Preview ({len(aff.reconstructed_string)} bp):**")
                st.code(aff.reconstructed_string[:800] + ("\n... [TRUNCATED DISPLAY]" if len(aff.reconstructed_string) > 800 else ""), language="text")
                st.caption("Demonstration of fragment grouping and reordering on synthetic, non-sensitive test strings. Payload is strictly not executed or activated.")

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # SUBSYSTEM 2: RUNTIME PHYSICS & INTERLOCK SIMULATOR
        # ----------------------------------------------------------------------
        with st.container(border=True):
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1.5px solid #D8EAF0; padding-bottom: 10px;">
                <div>
                    <span class="section-eyebrow">MODULE 2 // THERMAL-FLUIDIC PHYSICS</span>
                    <div class="card-title">Runtime Physics & Interlock Simulator (The Physics-AI Bridge)</div>
                    <div class="card-subtitle">Microsecond thermal, hydraulic, and kinetic conditions inside the physical compiler microchannel.</div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; background: #EAF8FB; color: #168FA1; padding: 6px 14px; border-radius: 9999px; font-weight: 700;">
                    L_CHANNEL: 50 μm · D_H: 12 μm
                </div>
            </div>
            """)

            col_ph1, col_ph2, col_ph3, col_ph4 = st.columns(4)
            with col_ph1:
                st.metric("Core Nozzle Temp", f"{phys.core_temp_c:.1f} °C", f"{phys.core_temp_k:.1f} K", help="Simulated core compiler nozzle temperature")
                st.metric("Ambient Temp", f"{phys.ambient_temp_c:.1f} °C", help="Chamber baseline reference temperature")
            with col_ph2:
                st.metric("Thermal Gradient (ΔT)", f"{phys.thermal_gradient_k_um:.4f} K/μm", help="Gradient threshold limit: 0.8500 K/μm")
                st.metric("Flow Velocity", f"{phys.flow_velocity_m_s:.4f} m/s", help="Scaled by sequence length and entropy")
            with col_ph3:
                st.metric("Reynolds Number (Re)", f"{phys.reynolds_number:.2f}", phys.flow_regime.value, help="Re = (rho * v * D_H) / mu")
                st.metric("Pressure Drop (ΔP)", f"{phys.pressure_drop_kpa:.3f} kPa", f"Total: {phys.total_pressure_kpa:.1f} kPa")
            with col_ph4:
                st.metric("Rearrangement Prob", f"{phys.rearrangement_probability * 100.0:.2f}%", help="Threshold safety ceiling: 82.00%")
                st.metric("Interlock State", phys.interlock_state.value, help="Hardware interlock relay state")

            # Relay Banner
            if phys.interlock_state == InterlockState.TRIPPED:
                trigger_items = "".join(f"<li><strong>{t.parameter_name}:</strong> {t.observed_value} {t.unit} (Limit: {t.threshold_value}) — <em>{t.description}</em></li>" for t in phys.trigger_records)
                render_html(f"""
                <div style="background: #FEF2F2; border: 2px solid #EF4444; border-radius: 12px; padding: 16px 20px; color: #991B1B; margin: 14px 0;">
                    <div style="font-weight: 900; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                        <span>🚨</span>
                        <span>HARDWARE INTERLOCK RELAY OVERRIDE: ENGAGED // TRIPPED</span>
                    </div>
                    <div style="font-size: 0.90rem; margin-top: 8px; line-height: 1.55;">
                        A safety threshold ceiling has been breached. Physical actuation relay locked in-memory.
                        <ul style="margin: 8px 0 0 18px; padding: 0;">
                            {trigger_items}
                        </ul>
                    </div>
                </div>
                """)
            else:
                render_html("""
                <div style="background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 12px; padding: 14px 20px; color: #166534; font-weight: 700; margin: 14px 0; font-size: 0.92rem; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.2rem;">🛡️</span>
                    <span><strong>HARDWARE INTERLOCK RELAY: ARMED // NOMINAL:</strong> All hydrodynamic, thermal gradient, and kinetic rearrangement variables remain safely enclosed within operating parameters.</span>
                </div>
                """)

            with st.expander("Inspect Microchannel Physical Parameters & Governing Equations", expanded=False):
                st.markdown("""
                **Explicit Channel Constants (Assumed Physical Environment):**
                - Microchannel Length ($L$): `50 μm`
                - Hydraulic Diameter ($D_H$): `12 μm`
                - Fluid Density ($\\rho$): `1,050 kg/m³`
                - Dynamic Viscosity ($\\mu$): `0.0012 Pa·s`
                - Ambient Reference Temperature ($T_{amb}$): `295.15 K` (`22.0 °C`)
                
                **Dynamically Inferred Variables at Runtime:**
                - Flow Velocity: $v = v_{base} \\times (1 + \\frac{L_{seq}}{1000}) \\times H_{norm}$
                - Flow Reynolds Number: $Re = \\frac{\\rho \\cdot v \\cdot D_H}{\\mu}$ (Laminar if $Re < 2000$, Turbulent if $Re > 4000$)
                - Core Thermal Gradient: $\\Delta T = \\frac{T_{core} - T_{amb}}{L}$ (Threshold limit: $0.8500\\ \\text{K}/\\mu\\text{m}$)
                - Microchannel Pressure Drop: $\\Delta P = \\frac{32 \\cdot \\mu \\cdot v \\cdot L}{D_H^2}$
                - Kinetic Rearrangement Probability: $P_{rearrange} = \\frac{1}{1 + e^{-k (T_{core} - T_{thresh})}}$ (Bounded in $[0.0, 1.0]$, Safety ceiling: $82.00\\%$)
                
                *Boundary Enforcement: The simulator calculates microchannel dynamics purely in-memory and never issues commands to real physical hardware.*
                """)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # SUBSYSTEM 3: EPHEMERAL HONEY-NET VALIDATION ENGINE
        # ----------------------------------------------------------------------
        with st.container(border=True):
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1.5px solid #D8EAF0; padding-bottom: 10px;">
                <div>
                    <span class="section-eyebrow">MODULE 3 // EPHEMERAL VALIDATION</span>
                    <div class="card-title">Ephemeral Honey-Net Invalidation Engine (The Safe Spooler)</div>
                    <div class="card-subtitle">Active parameters override, inert sugar blueprint generation, and peer-registry mesh routing.</div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; background: #EAF8FB; color: #168FA1; padding: 6px 14px; border-radius: 9999px; font-weight: 700;">
                    STATUS: SECURE ISOLATION ACTIVE
                </div>
            </div>
            """)

            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1:
                st.metric("Spooler Status", val.spooler_status.split("--")[-1].strip() if "--" in val.spooler_status else val.spooler_status, help=val.spooler_status)
                st.metric("Validation Verdict", val.validation_verdict)
            with col_v2:
                st.metric("Isolation Token", val.isolation_id[:18] + "...", help=val.isolation_id)
                st.metric("Decoy G-Code Size", f"{val.audit_record.gcode_size_bytes:,} Bytes", help=f"Harmless sucrose lattice coordinates generated on disk at {val.gcode_file_path}")
            with col_v3:
                st.metric("Payload Hash (SHA-256)", f"{val.audit_record.input_sha256[:10]}...", help=f"Full SHA-256: {val.audit_record.input_sha256}")
                st.metric("Mesh Audits Recorded", f"{val.in_memory_mesh_count} entries", help="In-memory peer ledger entries")


            # Transparent Safety Failure Alert Box
            if val.failed_checks:
                failed_items = "".join(f"<li>{chk}</li>" for chk in val.failed_checks)
                render_html(f"""
                <div style="background: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 12px; padding: 14px 18px; color: #B45309; margin: 12px 0; font-size: 0.90rem;">
                    <strong>SAFETY CHECKS FLAGGED (TRANSPARENT AUDIT TRAIL):</strong>
                    <ul style="margin: 6px 0 0 16px; padding: 0;">
                        {failed_items}
                    </ul>
                </div>
                """)

            render_html(f"""
            <div style="background: #0F172A; border: 1.5px solid #1E293B; border-radius: 12px; padding: 14px 18px; margin: 14px 0; color: #38BDF8; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; line-height: 1.6;">
                <div><strong>[SPOOLER DISPATCH]:</strong> {val.spooler_status}</div>
                <div><strong>[SECURITY TOKEN]:</strong> {val.isolation_id}</div>
                <div><strong>[ACTIVE OVERRIDE]:</strong> Target manufacturing output hijacked -> inert sucrose matrix G-code generated on disk.</div>
                <div><strong>[DECOY PATH]:</strong> {val.gcode_file_path} ({val.audit_record.gcode_size_bytes} bytes)</div>
            </div>
            """)

            with st.expander("Inspect Generated Decoy G-Code (`inert_sugar_blueprint.gcode`)", expanded=False):
                st.code(val.gcode_content[:1200] + ("\n... [TRUNCATED SAFE COORDINATES]" if len(val.gcode_content) > 1200 else ""), language="gcode")

            with st.expander("Inspect In-Memory Peer Registry Mesh Ledger", expanded=False):
                mesh_records = st.session_state.ml_mesh_registry.get_ledger()
                if mesh_records:
                    st.dataframe(
                        [
                            {
                                "Isolation Token": r.isolation_id,
                                "Timestamp (UTC)": r.timestamp_utc,
                                "Input Length": f"{r.input_length} bp",
                                "Verdict": r.validation_verdict,
                                "Interlock": r.interlock_state,
                                "G-Code Size": f"{r.gcode_size_bytes} B",
                            }
                            for r in mesh_records[-8:]
                        ],
                        use_container_width=True,
                    )

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # TERMINAL MONOCHROME TELEMETRY DASHBOARD
        # ----------------------------------------------------------------------
        with st.expander("Inspect Terminal Monochrome Telemetry Dashboard (Pure Standard Library Render)", expanded=False):
            terminal_view = MonochromeTerminalDashboard(ascii_mode=True, line_width=86).render(
                raw_input=clean_seq,
                affinity_result=aff,
                telemetry=phys,
                validation_report=val,
            )
            st.code(terminal_view, language="text")
            st.caption("Standard library terminal telemetry renderer output. All metrics are derived 100% dynamically at runtime.")



# ==============================================================================
# 8. PAGE 4: HARDWARE ENCLOSURE & ZERO-KNOWLEDGE VERIFICATION
# ==============================================================================

def render_page_secure_enclave():
    """Renders the Secure Enclave trust boundary & honest attestation status workspace."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">SECURITY ARCHITECTURE</span>
        <h1 class="section-headline">
            Hardware Enclosure & Zero-Knowledge Verification
        </h1>
        <p class="section-description">
            Inspect execution-isolation assumptions, verification evidence, trust boundaries, and security configuration.
        </p>
    </div>
    <div style="background: #FFF8E6; border: 1.5px solid #F0D499; border-radius: 16px; padding: 20px 26px; color: #73510D; font-size: 0.96rem; margin-bottom: 24px; line-height: 1.6;">
        <strong>Hardware Attestation Disclosure:</strong> Hardware-backed attestation is not configured in this environment.
        The current system operates under local Python process memory isolation. Silicon-level hardware attestation (e.g. Intel SGX / AMD SEV)
        requires dedicated certified processor extensions and attestation services. Parameters below represent architectural emulation models.
    </div>
    """)

    col_tb, col_att = st.columns([1.2, 1.2], gap="medium")

    with col_tb:
        with st.container(border=True):
            render_html("""
            <div class="card-title">Trust Boundary Topology</div>
            <div class="card-subtitle">Layered protection rings separating sequence ingest from system buses.</div>
            <table class="bio-table">
                <thead>
                    <tr>
                        <th>BOUNDARY LAYER</th>
                        <th>ISOLATION MECHANISM</th>
                        <th>SECURITY STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>APPLICATION PROCESS</strong></td>
                        <td>Host Operating System Sandbox</td>
                        <td>ACTIVE</td>
                    </tr>
                    <tr>
                        <td><strong>SEQUENCE MEMORY RING</strong></td>
                        <td>Volatile Buffer / Zero Persistence</td>
                        <td>ISOLATED</td>
                    </tr>
                    <tr>
                        <td><strong>REFERENCE DATA BOUNDARY</strong></td>
                        <td>In-Memory Read-Only Shard</td>
                        <td>LOCKED</td>
                    </tr>
                    <tr>
                        <td><strong>NETWORK EGRESS INTERFACE</strong></td>
                        <td>Physical Air-Gap / Zero TCP Sockets</td>
                        <td>AIR-GAPPED</td>
                    </tr>
                    <tr>
                        <td><strong>HARDWARE ROOT ATTESTATION</strong></td>
                        <td>Silicon Co-Processor Interface</td>
                        <td>SIMULATED ONLY</td>
                    </tr>
                </tbody>
            </table>
            """)

    with col_att:
        with st.container(border=True):
            render_html(f"""
            <div class="card-title">Runtime Environment & Verification State</div>
            <div class="card-subtitle">Verified parameters derived directly from the running host.</div>
            <table class="bio-table">
                <tbody>
                    <tr>
                        <td><strong>HOST RUNTIME</strong></td>
                        <td>Python 3.14 Local Execution Engine</td>
                    </tr>
                    <tr>
                        <td><strong>ISOLATION MODE</strong></td>
                        <td>Software Emulation (Air-Gapped)</td>
                    </tr>
                    <tr>
                        <td><strong>HARDWARE TEE SUPPORT</strong></td>
                        <td>Not Configured / Unavailable</td>
                    </tr>
                    <tr>
                        <td><strong>AUDIT TRAIL INTEGRITY</strong></td>
                        <td>Local In-Memory SHA-256 Digest Chain</td>
                    </tr>
                    <tr>
                        <td><strong>POLICY LEDGER INDEX</strong></td>
                        <td>v{st.session_state.homomorphic_db_index:.1f} (Synchronized)</td>
                    </tr>
                </tbody>
            </table>
            """)

    # Verification Primer
    with st.container(border=True):
        render_html("""
        <div class="card-title">Conceptual Verification Primer</div>
        <div class="card-subtitle">Understanding the technical distinction between TEEs, Zero-Knowledge Proofs, and Software Isolation.</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div style="background: #F7FCFD; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 20px;">
                <div style="font-size: 0.98rem; font-weight: 800; color: #168FA1; margin-bottom: 8px;">Trusted Execution Environments (TEE)</div>
                <div style="font-size: 0.90rem; color: #536D82; line-height: 1.6;">
                    Hardware-enforced secure enclaves where code and memory are encrypted by dedicated processor silicon, preventing inspection even from the host OS or hypervisor.
                </div>
            </div>
            <div style="background: #F7FCFD; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 20px;">
                <div style="font-size: 0.98rem; font-weight: 800; color: #168FA1; margin-bottom: 8px;">Zero-Knowledge Verification (ZKP)</div>
                <div style="font-size: 0.90rem; color: #536D82; line-height: 1.6;">
                    Cryptographic mathematical protocols allowing one party to prove that a sequence meets compliance policy without revealing the sequence itself.
                </div>
            </div>
            <div style="background: #F7FCFD; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 20px;">
                <div style="font-size: 0.98rem; font-weight: 800; color: #168FA1; margin-bottom: 8px;">Software Process Isolation</div>
                <div style="font-size: 0.90rem; color: #536D82; line-height: 1.6;">
                    Operating system level sandboxing and in-memory execution boundaries that isolate applications from external networks and disk persistence.
                </div>
            </div>
        </div>
        """)

    # Audit Events Stream
    rows_log = "".join(
        [
            f"<tr>"
            f"<td>{l['timestamp']}</td>"
            f"<td><strong>{l['channel']}</strong></td>"
            f"<td style='font-family: monospace;'>{l['signature']}</td>"
            f"<td>{l['detail']}</td>"
            f"<td><span style='background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;'>{l['status']}</span></td>"
            f"</tr>"
            for l in st.session_state.threat_logs
        ]
    )

    with st.container(border=True):
        render_html(f"""
        <div class="card-title">Local System Audit Events</div>
        <div class="card-subtitle">Real-time local event records logged during platform operation.</div>
        <table class="bio-table">
            <thead>
                <tr>
                    <th>TIMESTAMP (UTC)</th>
                    <th>SUBSYSTEM</th>
                    <th>SIGNATURE</th>
                    <th>AUDIT DETAIL</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
                {rows_log}
            </tbody>
        </table>
        """)


# ==============================================================================
# 9. PAGE 5: HOMOMORPHIC UPDATES & EPHEMERAL HONEY-NETS
# ==============================================================================
def render_page_homomorphic_sync():
    """Renders the Reference-Index Management & Honey-Net Decoy Workspace."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">CRYPTOGRAPHIC UPDATES & DECOYS</span>
        <h1 class="section-headline">
            Homomorphic Updates & Ephemeral Honey-Nets
        </h1>
        <p class="section-description">
            Reference-index management, integrity verification, update provenance, and decoy-workflow status.
        </p>
    </div>
    """)

    col_upd, col_hn = st.columns([1.2, 1.2], gap="medium")

    with col_upd:
        with st.container(border=True):
            render_html(f"""
            <div class="card-title">Reference-Index Management</div>
            <div class="card-subtitle">Active homomorphic model shard version: <strong>v{st.session_state.homomorphic_db_index:.1f}</strong></div>
            <p style="font-size: 0.94rem; color: #536D82; line-height: 1.6; margin: 12px 0;">
                Ingest simulated one-way satellite broadcast packages containing encrypted vector deltas <code>Enc(ΔV)</code>.
                Mathematical addition shifts vector weights without decrypting plaintexts.
            </p>
            """)

            if st.button("Ingest Sat-Broadcast Encrypted Delta Package (FHE)", type="primary", use_container_width=True, key="btn_ingest_fhe"):
                with st.spinner("Processing satellite encrypted broadcast package..."):
                    raw_payload = generate_sat_broadcast_payload(st.session_state.homomorphic_db_index)
                    new_weights, fhe_telemetry = homomorphic_blind_delta_merge(
                        st.session_state.reference_toxin_weights, raw_payload
                    )
                    st.session_state.reference_toxin_weights = new_weights
                    new_idx = round(st.session_state.homomorphic_db_index + 0.1, 1)
                    st.session_state.homomorphic_db_index = new_idx
                    st.session_state.active_nodes = synchronize_mesh_ledger(st.session_state.active_nodes, new_idx)

                    st.session_state.last_fhe_update = {
                        "duration_ms": fhe_telemetry["elapsed_ms"],
                        "new_index": new_idx,
                        "log_string": fhe_telemetry["log_string"],
                        "ciphertext_hash": fhe_telemetry["ciphertext_hash"],
                        "bytes_ingested": fhe_telemetry["bytes_ingested"],
                    }

                    st.session_state.threat_logs.insert(
                        0,
                        {
                            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "channel": "HOMOMORPHIC_INDEX",
                            "signature": f"FHE_DELTA_{fhe_telemetry['ciphertext_hash'][:8]}",
                            "detail": f"Satellite delta Enc(Delta_V) merged into DB Index v{new_idx:.1f}. 0 keys exposed.",
                            "status": "FHE_MERGED",
                        },
                    )
                st.rerun()

            if st.session_state.last_fhe_update:
                fhe = st.session_state.last_fhe_update
                render_html(f"""
                <div style="background: #F7FCFD; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 16px; margin-top: 14px; font-size: 0.90rem; line-height: 1.65;">
                    <div><strong>Processing Duration:</strong> {fhe['duration_ms']:.4f} ms</div>
                    <div><strong>New Policy Ledger:</strong> v{fhe['new_index']:.1f}</div>
                    <div><strong>Structural Log:</strong> {fhe['log_string']}</div>
                    <div><strong>Digest:</strong> <code>{fhe['ciphertext_hash'][:24]}...</code></div>
                </div>
                """)

    with col_hn:
        with st.container(border=True):
            render_html("""
            <div class="card-title">Honey-Net Decoy Workspace</div>
            <div class="card-subtitle">Silent printer target override rendering biological output completely non-viable.</div>
            <p style="font-size: 0.94rem; color: #536D82; line-height: 1.6; margin: 12px 0;">
                When sequence screening intercepts hazardous signatures, the system generates an inert sucrose matrix
                carrier file (<code>inert_sugar_blueprint.gcode</code>), preventing synthesis while spoofing pipeline success.
            </p>
            """)

            gcode_path = os.path.join(os.getcwd(), "inert_sugar_blueprint.gcode")
            if os.path.exists(gcode_path):
                with open(gcode_path, "r", encoding="utf-8") as f:
                    gcode_sample = f.read()[:500] + "\n... [Remaining G-Code suppressed for display]"
                st.code(gcode_sample, language="gcode")
            else:
                st.info("No honey-net decoy file generated yet. Execute a hazardous sequence in Exact Match to trigger.")

    # Cryptographic Status Table
    with st.container(border=True):
        render_html("""
        <div class="card-title">Cryptographic Capability Matrix</div>
        <div class="card-subtitle">Transparent disclosure of verified vs. simulation capabilities.</div>
        <table class="bio-table">
            <thead>
                <tr>
                    <th>SUBSYSTEM</th>
                    <th>SPECIFICATION</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>ENCRYPTION SCHEME</strong></td>
                    <td>Simulated Ring-LWE Additive Homomorphism</td>
                    <td><span style="background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;">DEMONSTRATION</span></td>
                </tr>
                <tr>
                    <td><strong>KEY MANAGEMENT</strong></td>
                    <td>Local Ephemeral Enclave Memory</td>
                    <td><span style="background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;">IN-MEMORY ONLY</span></td>
                </tr>
                <tr>
                    <td><strong>PACKAGE SIGNATURE VERIFICATION</strong></td>
                    <td>SHA-256 Digest Verification</td>
                    <td><span style="background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;">IMPLEMENTED</span></td>
                </tr>
                <tr>
                    <td><strong>DECOY REDIRECTION ENGINE</strong></td>
                    <td>Inert Sugar Blueprint G-Code Generator</td>
                    <td><span style="background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;">IMPLEMENTED</span></td>
                </tr>
            </tbody>
        </table>
        """)


# ==============================================================================
# 10. PAGE 6: ANALYSIS HISTORY
# ==============================================================================
def render_page_analysis_history():
    """Renders the privacy-conscious local analysis history."""
    render_html("""
    <div style="margin-bottom: 24px;">
        <span class="section-eyebrow">LOCAL-FIRST AUDIT RECORDS</span>
        <h1 class="section-headline">
            Analysis History
        </h1>
        <p class="section-description">
            Locally retained analysis records and reports, subject to the application's privacy settings.
        </p>
    </div>
    <div style="background: #EAF8FB; border: 1.5px solid #D8EAF0; border-radius: 14px; padding: 16px 22px; font-size: 0.92rem; color: #102D4D; margin-bottom: 24px; line-height: 1.6;">
        <strong>Privacy Policy:</strong> Raw biological sequences are never persisted to disk by default.
        Only cryptographic digests, timestamps, analysis methods, and quantitative scores are retained in local session memory.
    </div>
    """)

    if not st.session_state.analysis_history:
        st.info("No screening analyses recorded in the current session. Execute an analysis in Overview or Exact Match to populate history.")
    else:
        history_rows = "".join(
            [
                f"<tr>"
                f"<td>{h['timestamp']}</td>"
                f"<td><strong>{h.get('filename', 'Direct_Buffer')}</strong></td>"
                f"<td>{h['length']:,} bp</td>"
                f"<td style='font-family: monospace; font-size: 0.84rem;'>{h['sha256'][:16]}...</td>"
                f"<td>{h.get('duration_ms', 0.0):.4f} ms</td>"
                f"<td><span style='background: #EAF8FB; color: #168FA1; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.84rem;'>{h['status']}</span></td>"
                f"</tr>"
                for h in st.session_state.analysis_history
            ]
        )

        with st.container(border=True):
            render_html(f"""
            <div class="card-title">Session Analysis Log ({len(st.session_state.analysis_history)} records)</div>
            <div class="card-subtitle">Chronological ledger of screening executions performed in this session.</div>
            <table class="bio-table">
                <thead>
                    <tr>
                        <th>TIMESTAMP (UTC)</th>
                        <th>IDENTIFIER / FILE</th>
                        <th>LENGTH</th>
                        <th>SHA-256 DIGEST</th>
                        <th>DURATION</th>
                        <th>RESULT STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    {history_rows}
                </tbody>
            </table>
            """)

            col_dl_h, col_clr_h = st.columns([1.5, 1.0])
            with col_dl_h:
                st.download_button(
                    label="Download Full Session History (JSON)",
                    data=json.dumps(st.session_state.analysis_history, indent=2),
                    file_name="bio_sieve_session_history.json",
                    mime="application/json",
                    key="dl_history_json",
                )
            with col_clr_h:
                if st.button("Clear Session History", key="btn_clear_hist"):
                    st.session_state.analysis_history = []
                    st.rerun()


# ==============================================================================
# 11. SHARED FOOTER
# ==============================================================================
def render_footer():
    """Renders the NovaCell-inspired Biotechnology Footer."""
    render_html("""
    <div class="biotech-footer">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 900; color: #102D4D; font-size: 1.08rem;">THE BIO-SIEVE PROTOCOL</span>
                <span style="color: #168FA1; font-weight: 700; font-size: 0.95rem;">v5.0.0-PROD</span>
            </div>
            <div style="color: #536D82; font-size: 0.88rem;">
                LOCAL-FIRST BIOSECURITY SCREENING PLATFORM · ZERO EXTERNAL TELEMETRY
            </div>
        </div>
        <div style="color: #536D82; font-size: 0.85rem; line-height: 1.6;">
            <strong>Technical Disclaimer:</strong> This application demonstrates local sequence analysis architectures,
            Aho-Corasick exact pattern matching, and k-mer vector similarity algorithms. Hardware enclave attestation and
            fully homomorphic encryption features are simulated demonstration models.
        </div>
    </div>
    """)


# ==============================================================================
# 12. MAIN APPLICATION ROUTER
# ==============================================================================
def main():
    # Render top announcement strip and rectangular top navbar
    render_header_and_navbar()

    # Dispatch to active page
    current = st.session_state.active_page
    if current == "Overview":
        render_page_overview()
    elif current == "Exact Match":
        render_page_exact_match()
    elif current == "Fuzzy Analysis":
        render_page_fuzzy_analysis()
    elif current == "ML Operations":
        render_page_ml_operations()
    elif current == "Secure Enclave":
        render_page_secure_enclave()
    elif current == "Homomorphic Sync":
        render_page_homomorphic_sync()
    elif current == "Analysis History":
        render_page_analysis_history()
    else:
        render_page_overview()

    # Render shared biotechnology footer
    render_footer()


if __name__ == "__main__":
    main()
