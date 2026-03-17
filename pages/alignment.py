import streamlit as st
from styles.theme import page_header
from components.charts import skill_match_bar
from utils.scoring import JOB_ROLES, compute_score


def show():
    page_header("Job Alignment Analysis", "Skill-level gap analysis against selected role requirements")

    if "result" not in st.session_state:
        st.info("⬅️  Please upload a resume on the **Resume Upload** page first.")
        return

    r = st.session_state["result"]

    # Role selector (can override)
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        new_role = st.selectbox("Compare Against Role", list(JOB_ROLES.keys()),
                                index=list(JOB_ROLES.keys()).index(r["selected_role"]))
    if new_role != r["selected_role"]:
        r = compute_score(st.session_state.get("resume_text", ""), new_role)
        st.session_state["result"] = r

    st.markdown("---")

    # ── Match overview ────────────────────────────────────────────────────────
    col_match, col_chart = st.columns([1, 1.5])

    with col_match:
        pct = r["job_match_pct"]
        bar_color = "#10B981" if pct >= 70 else "#F59E0B" if pct >= 45 else "#EF4444"
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:28px;
                    box-shadow:0 2px 12px rgba(10,35,66,0.08);text-align:center;">
            <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;
                        letter-spacing:.8px;margin-bottom:10px;">Overall Job Match</div>
            <div style="font-size:64px;font-weight:900;color:{bar_color};line-height:1;">{pct:.0f}%</div>
            <div style="background:#F1F5F9;border-radius:8px;height:12px;margin:16px 0 8px;">
                <div style="background:{bar_color};border-radius:8px;height:12px;width:{pct}%;
                             transition:width .4s ease;"></div>
            </div>
            <div style="font-size:12px;color:#94A3B8;">{r['selected_role']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(skill_match_bar(r["matching_skills"], r["missing_skills"]),
                        use_container_width=True, config={"displayModeBar": False})

    with col_chart:
        # Matched skills
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:22px;
                    box-shadow:0 2px 8px rgba(10,35,66,0.07);margin-bottom:16px;">
            <div style="font-size:14px;font-weight:700;color:#065F46;margin-bottom:12px;">
                ✅ Matched Skills ({len(r['matching_skills'])})
            </div>
            <div>{"".join(f'<span class="skill-tag-match">{s}</span>' for s in r["matching_skills"])
                  if r["matching_skills"] else '<span style="color:#94A3B8;font-size:13px;">None detected</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Missing skills
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:22px;
                    box-shadow:0 2px 8px rgba(10,35,66,0.07);margin-bottom:16px;">
            <div style="font-size:14px;font-weight:700;color:#991B1B;margin-bottom:12px;">
                ❌ Missing Skills ({len(r['missing_skills'])})
            </div>
            <div>{"".join(f'<span class="skill-tag-miss">{s}</span>' for s in r["missing_skills"])
                  if r["missing_skills"] else '<span style="color:#94A3B8;font-size:13px;">All skills matched!</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Experience gap
        req_exp = JOB_ROLES[r["selected_role"]]["min_experience"]
        gap = max(0, req_exp - r["exp_years"])
        gap_color = "#10B981" if gap == 0 else "#F59E0B" if gap <= 1 else "#EF4444"
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:22px;
                    box-shadow:0 2px 8px rgba(10,35,66,0.07);">
            <div style="font-size:14px;font-weight:700;color:#0A2342;margin-bottom:10px;">
                🏢 Experience Gap
            </div>
            <div style="font-size:13px;color:#374151;">
                Detected: <strong>{r['exp_years']:.0f} yrs</strong> &nbsp;|&nbsp;
                Required: <strong>{req_exp} yrs</strong> &nbsp;|&nbsp;
                Gap: <strong style="color:{gap_color};">
                    {"None ✅" if gap == 0 else f"{gap:.0f} yr(s) ⚠️"}
                </strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
