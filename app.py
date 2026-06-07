import streamlit as st
import re

# ── 1. Production-Ready Module Isolation ──────────────────────────────────────
# Pulling imports to the top level prevents setup errors from swallowing real stack traces
import agents as _agents
import pipeline as _pipeline
from pipeline import run_research_pipeline

# ── 2. Page Configuration & Dynamic Branding ──────────────────────────────────
# Modern, minimal SVG combining data layers with an abstract document brief
DATABRIEF_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<line x1="16" y1="13" x2="8" y2="13"></line>'
    '<line x1="16" y1="17" x2="8" y2="17"></line>'
    '<polyline points="10 9 9 9 8 9"></polyline>'
    '</svg>'
)

st.set_page_config(
    page_title="DataBrief · Multi-Agent AI",
    page_icon="https://img.icons8.com/neon/96/document.png", # Premium minimal SaaS document asset URL
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 3. Custom Presentation Stylesheet ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:      #0a0c10;
    --surface: #111318;
    --border:  #1e2230;
    --accent:  #00e5ff;
    --accent2: #7c3aed;
    --text:    #e2e8f0;
    --muted:   #64748b;
    --search:  #00e5ff;
    --reader:  #a78bfa;
    --writer:  #34d399;
    --critic:  #fb923c;
    --danger:  #f43f5e;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 999px;
    padding: 0.35rem 1.2rem;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4.2rem);
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.8rem;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

[data-testid="stTextInput"] > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.08) !important;
}

/* Form Action Trigger Layout (No Icon Modification) */
[data-testid="stFormSubmitButton"] > button, [data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent2), var(--accent)) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
[data-testid="stFormSubmitButton"] > button:hover, [data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    max-width: 900px;
    margin: 0 auto 2.5rem;
}
@media (max-width: 700px) {
    .pipeline-grid { grid-template-columns: repeat(2, 1fr); }
}
.step-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1rem;
    text-align: center;
    transition: border-color 0.35s, box-shadow 0.35s;
    position: relative;
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--step-color, var(--border));
    border-radius: 14px 14px 0 0;
}
.step-card.active {
    border-color: var(--step-color, var(--accent));
    box-shadow: 0 0 24px -4px var(--step-color, var(--accent));
}
.step-card.failed {
    border-color: var(--danger) !important;
    box-shadow: 0 0 24px -4px rgba(244,63,94,0.3) !important;
}

.step-icon { 
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.6rem; 
    color: var(--muted);
    transition: color 0.3s ease;
}
.step-icon svg {
    stroke: currentColor;
    fill: none;
}
.step-card.active .step-icon { color: var(--step-color); }
.step-card.done .step-icon { color: var(--writer); }
.step-card.failed .step-icon { color: var(--danger); }

.step-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
}
.step-card.active .step-label,
.step-card.done .step-label,
.step-card.failed .step-label { color: var(--text); }

.step-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    margin-top: 0.45rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
}
.step-status svg {
    stroke: currentColor;
    fill: none;
}
.step-card.active .step-status { color: var(--step-color, var(--accent)); }
.step-card.done .step-status  { color: var(--writer); }
.step-card.failed .step-status { color: var(--danger) !important; }

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.animate-spin {
    animation: spin 1s linear infinite;
}

.result-block {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-left: 4px solid var(--block-color, var(--accent));
    border-radius: 0 12px 12px 0;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.result-block h3 {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--block-color, var(--accent));
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.result-block h3 svg {
    stroke: currentColor;
    fill: none;
}
.result-container {
    margin-top: 0.8rem;
}
.result-block pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
    margin: 0;
    line-height: 1.7;
}

[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, var(--accent2), var(--accent)) !important;
    border-radius: 999px !important;
}
</style>
""", unsafe_allow_html=True)

# ── 4. Static SVG Layout Assets ───────────────────────────────────────────────
SVG_ICONS = {
    "search": '<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
    "reader": '<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>',
    "writer": '<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>',
    "critic": '<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
    "check": '<svg width="12" height="12" viewBox="0 0 24 24" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>',
    "spinner": '<svg class="animate-spin" width="12" height="12" viewBox="0 0 24 24" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="16"></circle></svg>',
    "idle": '<svg width="12" height="12" viewBox="0 0 24 24" stroke-width="2"><circle cx="12" cy="12" r="10"></circle></svg>',
    "cross": '<svg width="12" height="12" viewBox="0 0 24 24" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>'
}

STEPS = [
    {"icon": SVG_ICONS["search"], "label": "Search Agent", "color": "var(--search)", "key": "search"},
    {"icon": SVG_ICONS["reader"], "label": "Reader Agent", "color": "var(--reader)", "key": "reader"},
    {"icon": SVG_ICONS["writer"], "label": "Writer Chain", "color": "var(--writer)", "key": "writer"},
    {"icon": SVG_ICONS["critic"], "label": "Critic Chain", "color": "var(--critic)", "key": "critic"},
]

# ── 5. Advanced Pipeline UI State Engine ──────────────────────────────────────
def render_steps(status_list=None):
    """
    Renders step cards based on an explicit status mapping dictionary.
    Statuses can be: 'idle', 'running', 'complete', or 'failed'
    """
    if status_list is None:
        status_list = {s["key"]: "idle" for s in STEPS}
        
    cards = ""
    for s in STEPS:
        state = status_list.get(s["key"], "idle")
        
        if state == "complete":
            cls = "done"
            status_text = f"{SVG_ICONS['check']} complete"
        elif state == "running":
            cls = "active"
            status_text = f"{SVG_ICONS['spinner']} running..."
        elif state == "failed":
            cls = "failed"
            status_text = f"{SVG_ICONS['cross']} failed"
        else:
            cls = ""
            status_text = f"{SVG_ICONS['idle']} idle"
            
        cards += f"""
        <div class="step-card {cls}" style="--step-color:{s['color']}">
            <div class="step-icon">{s['icon']}</div>
            <div class="step-label">{s['label']}</div>
            <div class="step-status">{status_text}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-grid">{cards}</div>', unsafe_allow_html=True)

def result_block(title: str, icon_name: str, color: str, content: str):
    safe = content.replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f"""
    <div class="result-block" style="--block-color:{color}">
        <h3>{SVG_ICONS[icon_name]} {title}</h3>
        <div class="result-container">
            <pre>{safe}</pre>
        </div>
    </div>""", unsafe_allow_html=True)

# ── 6. Header/Hero Rendering ──────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">{DATABRIEF_SVG} Synthesized Market Intelligence</div>
    <h1>DataBrief</h1>
    <p>Four specialised AI agents collaborate — searching, scraping, writing, and critiquing — to deliver a polished research report on any topic.</p>
</div>
""", unsafe_allow_html=True)

# ── 7. Input Interface Context ────────────────────────────────────────────────
_, col_mid, _ = st.columns([1, 2.5, 1])
with col_mid:
    with st.form(key="research_pipeline_form", clear_on_submit=False):
        topic = st.text_input(
            label="topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025 …",
            label_visibility="collapsed",
        )
        form_submitted = st.form_submit_button("Run Research Pipeline", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Initialize trackable execution states inside active runtime memory
if "pipeline_status" not in st.session_state:
    st.session_state.pipeline_status = {s["key"]: "idle" for s in STEPS}

# ── 8. Live Pipeline Execution Logic ──────────────────────────────────────────
if form_submitted:
    # Reset all statuses back to clean baseline on a brand new form run
    st.session_state.pipeline_status = {s["key"]: "idle" for s in STEPS}
    current_running_node = "search"
    
    try:
        if not topic.strip():
            st.warning("Please enter a research topic first.")
            st.stop()

        progress = st.progress(0, text="Initialising pipeline…")
        step_slot = st.empty()
        result_area = st.container()

        # --- NODE 1: SEARCH AGENT ---
        current_running_node = "search"
        st.session_state.pipeline_status[current_running_node] = "running"
        with step_slot:
            render_steps(st.session_state.pipeline_status)

        progress.progress(5, text="Search agent finding sources…")
        search_agent = _agents.build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        search_results = search_result["messages"][-1].content

        with result_area:
            result_block("Search Results", "search", "var(--search)", search_results)

        st.session_state.pipeline_status["search"] = "complete"
        progress.progress(30, text="Search complete — launching Reader…")

        # --- NODE 2: READER AGENT ---
        current_running_node = "reader"
        st.session_state.pipeline_status[current_running_node] = "running"
        with step_slot:
            render_steps(st.session_state.pipeline_status)

        reader_agent = _agents.build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{search_results[:800]}"
            )]
        })
        scraped_content = reader_result["messages"][-1].content

        with result_area:
            result_block("Scraped Content", "reader", "var(--reader)", scraped_content)

        st.session_state.pipeline_status["reader"] = "complete"
        progress.progress(55, text="Reader complete — Writer drafting…")

        # --- NODE 3: WRITER CHAIN ---
        current_running_node = "writer"
        st.session_state.pipeline_status[current_running_node] = "running"
        with step_slot:
            render_steps(st.session_state.pipeline_status)

        research_combined = (
            f"SEARCH RESULTS:\n{search_results}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
        )
        found_urls = re.findall(r'https?://[^\s\)\]\,\"\'<>]+', research_combined)
        urls_str = "\n".join(found_urls) if found_urls else "(none)"

        report = _agents.writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
            "urls": urls_str,
        })

        with result_area:
            result_block("Draft Report", "writer", "var(--writer)", report)

        st.session_state.pipeline_status["writer"] = "complete"
        progress.progress(78, text="Report drafted — Critic reviewing…")

        # --- NODE 4: CRITIC CHAIN ---
        current_running_node = "critic"
        st.session_state.pipeline_status[current_running_node] = "running"
        with step_slot:
            render_steps(st.session_state.pipeline_status)

        feedback = _agents.critic_chain.invoke({"report": report})

        with result_area:
            result_block("Critic Feedback", "critic", "var(--critic)", feedback)

        st.session_state.pipeline_status["critic"] = "complete"
        progress.progress(100, text="Pipeline complete!")
        
        with step_slot:
            render_steps(st.session_state.pipeline_status)

        st.success("All four agents finished.")

    except Exception as e:
        # Halt execution, clear running status from active node, and apply 'failed' state layout
        st.session_state.pipeline_status[current_running_node] = "failed"
        with step_slot:
            render_steps(st.session_state.pipeline_status)
            
        if "rate_limit" in str(e) or "429" in str(e):
            st.error("Model is busy or rate-limited. Please try again later.")
        else:
            st.error(f"Pipeline Execution Blocked at [{current_running_node.upper()}]: {str(e)}")
        st.stop()

else:
    # On first load prior to active submission, cards render as completely idle
    render_steps(st.session_state.pipeline_status)
    st.markdown(
        "<p style='text-align:center;color:var(--muted);font-size:0.85rem;font-family:JetBrains Mono,monospace;'>Enter a topic to begin.</p>",
        unsafe_allow_html=True,
    )