import streamlit as st
import pandas as pd
from styles.theme import page_header
from utils.database import get_all_resumes

def show():
    page_header(
        "Candidate History",
        "View and filter all previously analyzed candidate resumes from the database."
    )
    
    rows = get_all_resumes()
    if not rows:
        st.info("No candidate history available yet. Upload resumes to see them here.")
        return
        
    # Remove any rows where "filename" might be null or blank
    df = pd.DataFrame(rows)
    df = df.dropna(subset=["filename"])
    
    # Use exact keys returned by get_all_resumes() -> database.py
    # id, filename, role_selected, score, skills_count, experience_score, achievement_score, job_match_score, created_at
    if "filename" not in df.columns:
        st.info("No valid candidate history available yet.")
        return
        
    display_df = df[["filename", "role_selected", "score", "created_at"]].copy()
    display_df.columns = ["Filename", "Role", "Score", "Analysis Date"]
    display_df["Score"] = pd.to_numeric(display_df["Score"]).fillna(0).astype(float)
    
    try:
        display_df["Analysis Date"] = pd.to_datetime(display_df["Analysis Date"])
    except:
        pass # Will keep string format if parsing fails
    
    st.markdown("### Filter Candidates")
    
    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        roles = ["All"] + sorted(list(display_df["Role"].unique()))
        sel_role = st.selectbox("🎯 Filter by Role", roles)
        
    with col_f2:
        max_val = float(display_df["Score"].max()) if not display_df.empty else 10.0
        min_score, max_score = st.slider("📊 Score Range", 0.0, 10.0, (0.0, max_val), 0.5)
        
    with col_f3:
        date_sort = st.selectbox("🕑 Sort by Date", ["Newest First", "Oldest First"])
        
    st.markdown("<br>", unsafe_allow_html=True)
        
    # Apply filters
    filtered_df = display_df.copy()
    
    # Filter by Role
    if sel_role != "All":
        filtered_df = filtered_df[filtered_df["Role"] == sel_role]
        
    # Filter by Score
    filtered_df = filtered_df[(filtered_df["Score"] >= min_score) & (filtered_df["Score"] <= max_score)]
    
    # Apply Sorting
    if "Analysis Date" in filtered_df.columns:
        if date_sort == "Newest First":
            filtered_df = filtered_df.sort_values(by="Analysis Date", ascending=False)
        else:
            filtered_df = filtered_df.sort_values(by="Analysis Date", ascending=True)
            
        try:
            filtered_df["Analysis Date"] = filtered_df["Analysis Date"].dt.strftime('%Y-%m-%d %H:%M')
        except:
            filtered_df["Analysis Date"] = filtered_df["Analysis Date"].astype(str)
    
    # Format Score
    filtered_df["Score"] = filtered_df["Score"].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
