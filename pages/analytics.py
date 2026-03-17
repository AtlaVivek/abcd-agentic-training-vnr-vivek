import streamlit as st
from styles.theme import page_header
from components.charts import feature_importance_chart
from utils.scoring import get_model_analytics


def show():
    page_header("Model Analytics", "Random Forest model performance metrics & feature importance")

    analytics = get_model_analytics()

    # ── Metric cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("RMSE",          analytics["rmse"],    help="Root Mean Squared Error")
    c2.metric("MAE",           analytics["mae"],     help="Mean Absolute Error")
    c3.metric("R² Score",      analytics["r2"],      help="Coefficient of determination")
    c4.metric("CV Mean Score", analytics["cv_mean"], help="5-Fold Cross-validation mean")

    st.markdown("---")

    col_feat, col_cv = st.columns([1.6, 1])

    with col_feat:
        st.markdown('<div class="section-header">Feature Importance (Random Forest)</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(
            feature_importance_chart(analytics["features"], analytics["importance"]),
            use_container_width=True, config={"displayModeBar": False}
        )

    with col_cv:
        st.markdown('<div class="section-header">Cross-Validation Results</div>',
                    unsafe_allow_html=True)
        for i, score in enumerate(analytics["cv_scores"], 1):
            bar_pct = int(score * 100)
            color   = "#10B981" if score >= 0.88 else "#3B82F6"
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;
                            color:#374151;margin-bottom:4px;">
                    <span>Fold {i}</span><strong style="color:{color};">{score:.4f}</strong>
                </div>
                <div style="background:#F1F5F9;border-radius:6px;height:8px;">
                    <div style="background:{color};border-radius:6px;height:8px;width:{bar_pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:16px;margin-top:10px;
                    box-shadow:0 2px 8px rgba(10,35,66,0.07);">
            <div style="font-size:12px;color:#64748B;margin-bottom:6px;">CV Summary</div>
            <div style="font-size:20px;font-weight:800;color:#0A2342;">{analytics['cv_mean']:.4f}</div>
            <div style="font-size:11px;color:#94A3B8;">Mean ± {analytics['cv_std']:.4f} std</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Technical notes ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="background:#F8FAFC;border-radius:12px;padding:20px;border:1px solid #E2E8F0;">
        <div style="font-size:13px;font-weight:700;color:#0A2342;margin-bottom:10px;">🔬 Model Architecture Notes</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px;color:#64748B;">
            <div>• Algorithm: Random Forest Regressor (n_estimators=200)</div>
            <div>• Feature Engineering: TF-IDF + structured extraction</div>
            <div>• Training Set: 12,000+ labelled resumes</div>
            <div>• Validation: Stratified 5-Fold CV</div>
            <div>• Hyperparameter tuning: GridSearchCV</div>
            <div>• Output: Continuous score 1–9 (regression)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
