import streamlit as st
import random
from styles.theme import page_header, kpi_card
from components.charts import score_distribution_chart


def show():
    page_header(
        "Executive Overview",
        "Enterprise AI-Powered Resume Intelligence Dashboard — Corporate Edition"
    )

    # ── KPI Row ──────────────────────────────────────────────────────────────
    from utils.database import get_all_resumes
    history = get_all_resumes()
    
    total   = max(len(history), 1) if len(history) > 0 else 0
    
    # Calculate averages from DB data
    if history:
        # DB uses "score" instead of "final_score", and "job_match_score" instead of "job_match_pct"
        avg_score = round(sum((r.get("score") or 0) for r in history) / len(history), 1)
        high_pct  = round(len([r for r in history if (r.get("score") or 0) >= 7.5]) / len(history) * 100, 1)
        avg_match = round(sum((r.get("job_match_score") or 0) for r in history) / len(history), 1)
    else:
        avg_score, high_pct, avg_match = 0.0, 0.0, 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Total Resumes Processed", str(len(history)), "Lifetime", "#1A73E8")
    with c2: kpi_card("Average Resume Score",    f"{avg_score}/9",          "AI Weighted", "#10B981")
    with c3: kpi_card("High-Quality Candidates", f"{high_pct}%",            "Score ≥ 7.5", "#8B5CF6")
    with c4: kpi_card("Avg Job Match",            f"{avg_match}%",           "Role Alignment", "#F59E0B")

    st.markdown("---")

    # ── Score Distribution + Summary ─────────────────────────────────────────
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
        demo_scores = [(r.get("score") or 0) for r in history] if history else [
            random.uniform(2, 9) for _ in range(40)
        ]
        st.plotly_chart(score_distribution_chart(demo_scores), use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown('<div class="section-header">Platform Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(10,35,66,0.07);font-size:14px;color:#374151;line-height:1.8;">
        The <strong>AI Resume Intelligence Platform</strong> leverages an ensemble Random Forest model
        to score candidate resumes across four weighted dimensions:<br><br>
        🔵 <strong>Skills Strength</strong> — Keyword & domain match<br>
        🟣 <strong>Experience Depth</strong> — Years & progression<br>
        🟢 <strong>Achievement Impact</strong> — Quantified results<br>
        🟡 <strong>Job Similarity</strong> — Role alignment index<br><br>
        Scores are normalized to a <strong>1–9 scale</strong> with categorical classification
        from <em>Poor</em> to <em>Excellent</em>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Status Banner ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:12px;
                padding:18px 24px;border:1px solid #BFDBFE;display:flex;align-items:center;gap:12px;">
        <span style="font-size:22px;">💡</span>
        <div>
            <strong style="color:#1E40AF;font-size:14px;">Getting Started</strong><br>
            <span style="color:#374151;font-size:13px;">
            Navigate to <strong>Resume Upload</strong> in the sidebar to analyse your first candidate.
            All results persist across pages within the current session.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
