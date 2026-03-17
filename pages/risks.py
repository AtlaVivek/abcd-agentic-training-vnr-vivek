import streamlit as st
from styles.theme import page_header
from utils.scoring import generate_risks


def show():
    page_header("Risk & Weakness Insights", "AI-detected resume risks with actionable remediation guidance")

    if "result" not in st.session_state:
        st.info("⬅️  Please upload a resume on the **Resume Upload** page first.")
        return

    r = st.session_state["result"]
    risks = generate_risks(r)

    severity_cfg = {
        "High":   {"color": "#EF4444", "bg": "#FEF2F2", "icon": "🔴", "class": ""},
        "Medium": {"color": "#F59E0B", "bg": "#FFFBEB", "icon": "🟡", "class": "medium"},
        "Low":    {"color": "#3B82F6", "bg": "#EFF6FF", "icon": "🔵", "class": "low"},
    }

    # Summary bar
    high_c   = sum(1 for r_ in risks if r_["severity"] == "High")
    med_c    = sum(1 for r_ in risks if r_["severity"] == "Medium")
    low_c    = sum(1 for r_ in risks if r_["severity"] == "Low")

    s1, s2, s3, _ = st.columns([1, 1, 1, 2])
    s1.metric("🔴 High Risk",   high_c)
    s2.metric("🟡 Medium Risk", med_c)
    s3.metric("🔵 Low Risk",    low_c)

    st.markdown("---")

    for issue in risks:
        cfg = severity_cfg.get(issue["severity"], severity_cfg["Low"])
        st.markdown(f"""
        <div class="risk-card {cfg['class']}" style="border-left-color:{cfg['color']};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div style="font-size:15px;font-weight:700;color:#0A2342;">
                    {cfg['icon']} {issue['title']}
                </div>
                <span style="background:{cfg['bg']};color:{cfg['color']};
                             padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;">
                    {issue['severity']} Risk
                </span>
            </div>
            <div style="font-size:13px;color:#374151;margin-bottom:10px;">
                <strong>Issue:</strong> {issue['explanation']}
            </div>
            <div style="background:{cfg['bg']};border-radius:8px;padding:10px 14px;margin-bottom:6px;">
                <div style="font-size:12px;font-weight:700;color:{cfg['color']};margin-bottom:4px;">
                    💡 Recommended Fix
                </div>
                <div style="font-size:13px;color:#374151;">{issue['fix']}</div>
            </div>
            <div style="font-size:11px;color:#94A3B8;">Score Impact: <strong>{issue['impact']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border-radius:12px;
                padding:18px 24px;border:1px solid #BBF7D0;">
        <strong style="color:#065F46;font-size:14px;">📈 Next Steps</strong><br>
        <span style="font-size:13px;color:#374151;">
        Address High-risk items first to maximise score improvement. After revision,
        re-upload the updated resume to track your new score.
        </span>
    </div>
    """, unsafe_allow_html=True)
