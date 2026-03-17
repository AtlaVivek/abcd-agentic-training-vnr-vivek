import streamlit as st
import pandas as pd
import plotly.express as px
from styles.theme import page_header
from utils.database import (
    get_resume_stats,
    get_role_distribution,
    get_score_distribution,
    get_all_resumes
)

def show():
    page_header(
        "Admin Dashboard",
        "Executive oversight and analytics for candidate applications."
    )
    
    # Overview Metrics
    stats = get_resume_stats()
    
    # Card-based analytics layout for KPIs
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="font-size:18px;font-weight:700;color:#0A2342;margin-bottom:12px;">📈 Key Performance Metrics</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resumes Analyzed", stats["total"])
    with col2:
        st.metric("Average Candidate Score", f"{stats['avg_score']:.1f}")
    with col3:
        st.metric("Highest Candidate Score", f"{stats['max_score']:.1f}")
    with col4:
        roles_dist = get_role_distribution()
        most_common_role = max(roles_dist.items(), key=lambda x: x[1])[0] if roles_dist else "—"
        st.metric("Most Common Role", most_common_role)
    
    st.markdown("<hr style='border:none;border-top:1px solid #E2E8F0;margin:24px 0;'>", unsafe_allow_html=True)
    
    # Charts section
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="font-size:18px;font-weight:700;color:#0A2342;margin-bottom:12px;">📊 Distribution Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#334155;margin-bottom:8px;'>Resume Score Distribution</div>", unsafe_allow_html=True)
        scores = get_score_distribution()
        if scores:
            fig1 = px.histogram(
                x=scores, 
                nbins=10, 
                labels={"x": "Score", "y": "Count"}, 
                color_discrete_sequence=['#1A73E8']
            )
            fig1.update_layout(
                showlegend=False, 
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No score data available.")
            
    with col_chart2:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#334155;margin-bottom:8px;'>Job Role Distribution</div>", unsafe_allow_html=True)
        roles = get_role_distribution()
        if roles:
            fig2 = px.pie(
                names=list(roles.keys()), 
                values=list(roles.values()), 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig2.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No role data available.")
            
    st.markdown("<hr style='border:none;border-top:1px solid #E2E8F0;margin:24px 0;'>", unsafe_allow_html=True)
    
    # Leaderboard section
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="font-size:18px;font-weight:700;color:#0A2342;margin-bottom:12px;">🏆 Candidate Leaderboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    rows = get_all_resumes()
    if rows:
        df = pd.DataFrame(rows)
        # Drop rows missing the required 'filename' or 'score' column completely 
        df = df.dropna(subset=["filename"])
        
        if df.empty or "filename" not in df.columns:
            st.info("No valid resumes found in the database. When candidates upload their resumes, they will appear here.")
            return

        # Rename columns for display
        display_df = df[["filename", "role_selected", "score", "created_at"]].copy()
        display_df.columns = ["Filename", "Role", "Score", "Upload Date"]
        
        # Sort and format
        display_df["Score"] = pd.to_numeric(display_df["Score"]).apply(lambda x: f"{x:.2f}")
        try:
            display_df["Upload Date"] = pd.to_datetime(display_df["Upload Date"]).dt.strftime('%Y-%m-%d %H:%M')
        except:
            pass # Keep as string if parsing fails
            
        # Leaderboard should automatically be sorted by top score
        display_df["_ScoreFloat"] = display_df["Score"].astype(float)
        display_df = display_df.sort_values(by="_ScoreFloat", ascending=False).drop(columns=["_ScoreFloat"])
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No resumes found in the database. When candidates upload their resumes, they will appear here.")
