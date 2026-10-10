"""

A clean, modern, and easy-to-use web dashboard to analyze social media
engagement across platforms and content formats.
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Social Media Content Analyzer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Clean CSS
st.markdown("""
<style>
    /* Metric Cards */
    .metric-box {
        background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        text-align: left;
    }
    .metric-title {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-sub {
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
    }
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    /* Simulator Card */
    .sim-card {
        background-color: #f1f5f9;
        border-left: 5px solid #6366f1;
        border-radius: 10px;
        padding: 16px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# 2. Data Loading & Metrics Computation
# -------------------------------------------------------------
@st.cache_data
def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "dataset", "social_media_data.csv")
    if not os.path.exists(file_path):
        st.error("Dataset file not found! Please check dataset/social_media_data.csv.")
        st.stop()
    df = pd.read_csv(file_path)
    
    # Calculate Engagement & Engagement Rate
    df["Engagement"] = df["Likes"] + df["Comments"] + df["Shares"]
    df["Engagement_Rate"] = ((df["Engagement"] / df["Views"]) * 100).round(2)
    return df


df_raw = get_data()


# -------------------------------------------------------------
# 3. Sidebar Filters
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Filter Posts")
    
    # Platform Filter
    platforms = ["All Platforms"] + sorted(df_raw["Platform"].unique().tolist())
    selected_platform = st.selectbox("Platform", platforms)

    # Content Type Filter
    content_types = ["All Content Types"] + sorted(df_raw["Content_Type"].unique().tolist())
    selected_content = st.selectbox("Content Type", content_types)

    st.markdown("---")
    st.markdown("### 📌 About This Tool")
    st.info(
        "A simple, lightweight analytics tool that compares social media engagement "
        "across Reels, Videos, Images, and Text posts.\n\n"
        "• **Total Posts:** 30\n"
        "• **Platforms:** 5\n"
        "• **Metric:** Likes + Comments + Shares"
    )


# Apply filters
df = df_raw.copy()
if selected_platform != "All Platforms":
    df = df[df["Platform"] == selected_platform]
if selected_content != "All Content Types":
    df = df[df["Content_Type"] == selected_content]


# -------------------------------------------------------------
# 4. Header & Top Summary Cards
# -------------------------------------------------------------
st.title("📱 Social Media Content Analyzer")
st.caption("Understand what content performs best with simple, clear engagement metrics.")

# Key Performance Indicators (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_posts = len(df)
total_views = int(df["Views"].sum()) if total_posts > 0 else 0
total_engagement = int(df["Engagement"].sum()) if total_posts > 0 else 0
avg_rate = df["Engagement_Rate"].mean() if total_posts > 0 else 0.0

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Posts Analyzed</div>
        <div class="metric-value">{total_posts}</div>
        <div class="metric-sub">Sample Records</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Total Views</div>
        <div class="metric-value">{total_views:,}</div>
        <div class="metric-sub">Combined Reach</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Total Engagement</div>
        <div class="metric-value">{total_engagement:,}</div>
        <div class="metric-sub">Likes + Comments + Shares</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Avg Engagement Rate</div>
        <div class="metric-value">{avg_rate:.2f}%</div>
        <div class="metric-sub">Engagement / Views</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# 5. Interactive Charts Section
# -------------------------------------------------------------
if total_posts == 0:
    st.warning("No posts match the current filter selection. Please reset your filters.")
else:
    tab1, tab2, tab3 = st.tabs(["📊 Performance Charts", "⚡ Post Simulator", "📋 Raw Data"])

    # --- TAB 1: CHARTS ---
    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("<div class='section-header'>Average Engagement by Content Type</div>", unsafe_allow_html=True)
            content_avg = (
                df.groupby("Content_Type")["Engagement"]
                .mean()
                .reset_index()
                .sort_values(by="Engagement", ascending=False)
            )
            fig_content = px.bar(
                content_avg,
                x="Content_Type",
                y="Engagement",
                color="Content_Type",
                text_auto=".0f",
                color_discrete_sequence=["#4F46E5", "#06B6D4", "#10B981", "#F59E0B"],
                labels={"Content_Type": "Content Type", "Engagement": "Avg Engagement"}
            )
            fig_content.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=340,
                xaxis_title="",
                yaxis_title="Engagement (Likes + Comments + Shares)"
            )
            st.plotly_chart(fig_content, use_container_width=True)

        with c2:
            st.markdown("<div class='section-header'>Average Views by Platform</div>", unsafe_allow_html=True)
            platform_avg = (
                df.groupby("Platform")["Views"]
                .mean()
                .reset_index()
                .sort_values(by="Views", ascending=False)
            )
            fig_platform = px.bar(
                platform_avg,
                x="Platform",
                y="Views",
                color="Platform",
                text_auto=",.0f",
                color_discrete_sequence=px.colors.qualitative.Prism,
                labels={"Platform": "Platform", "Views": "Avg Views"}
            )
            fig_platform.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=340,
                xaxis_title="",
                yaxis_title="Views"
            )
            st.plotly_chart(fig_platform, use_container_width=True)

        # Row 2 Charts
        c3, c4 = st.columns(2)

        with c3:
            st.markdown("<div class='section-header'>Engagement Breakdown (Likes, Comments, Shares)</div>", unsafe_allow_html=True)
            breakdown = df.groupby("Content_Type")[["Likes", "Comments", "Shares"]].mean().reset_index()
            fig_breakdown = go.Figure()
            fig_breakdown.add_trace(go.Bar(name='Likes', x=breakdown['Content_Type'], y=breakdown['Likes'], marker_color='#3B82F6'))
            fig_breakdown.add_trace(go.Bar(name='Comments', x=breakdown['Content_Type'], y=breakdown['Comments'], marker_color='#10B981'))
            fig_breakdown.add_trace(go.Bar(name='Shares', x=breakdown['Content_Type'], y=breakdown['Shares'], marker_color='#F59E0B'))
            fig_breakdown.update_layout(
                barmode='stack',
                height=320,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_breakdown, use_container_width=True)

        with c4:
            st.markdown("<div class='section-header'>Content Format Share</div>", unsafe_allow_html=True)
            counts = df["Content_Type"].value_counts().reset_index()
            counts.columns = ["Content_Type", "Count"]
            fig_pie = px.pie(
                counts,
                values="Count",
                names="Content_Type",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(
                height=320,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 2: INTERACTIVE SIMULATOR ---
    with tab2:
        st.markdown("<div class='section-header'>⚡ Quick Post Engagement Simulator</div>", unsafe_allow_html=True)
        st.write("Estimate how much engagement a new post could receive based on historical averages.")

        sim_col1, sim_col2 = st.columns([1, 1])

        with sim_col1:
            sim_format = st.selectbox("Select Content Format", ["Reel", "Video", "Image", "Text"], key="sim_format")
            sim_platform = st.selectbox("Select Platform", ["Instagram", "YouTube", "Facebook", "LinkedIn", "Twitter"], key="sim_platform")
            sim_views = st.slider("Estimated Views", min_value=500, max_value=25000, value=5000, step=500)

        # Calculate benchmark rates based on historical data
        hist_benchmark = df_raw[df_raw["Content_Type"] == sim_format]
        if len(hist_benchmark) > 0:
            avg_rate_val = hist_benchmark["Engagement_Rate"].mean() / 100
            likes_ratio = hist_benchmark["Likes"].sum() / hist_benchmark["Views"].sum()
            comments_ratio = hist_benchmark["Comments"].sum() / hist_benchmark["Views"].sum()
            shares_ratio = hist_benchmark["Shares"].sum() / hist_benchmark["Views"].sum()
        else:
            avg_rate_val, likes_ratio, comments_ratio, shares_ratio = 0.08, 0.06, 0.01, 0.01

        est_likes = int(sim_views * likes_ratio)
        est_comments = int(sim_views * comments_ratio)
        est_shares = int(sim_views * shares_ratio)
        est_total = est_likes + est_comments + est_shares
        est_rate_pct = round((est_total / sim_views) * 100, 2)

        with sim_col2:
            st.markdown(f"""
            <div class="sim-card">
                <h4 style="margin-top:0; color:#4338ca;">Predicted Performance for {sim_format} on {sim_platform}</h4>
                <div style="font-size: 1.6rem; font-weight: bold; color: #1e1b4b; margin: 8px 0;">
                    {est_total:,} <span style="font-size: 1rem; font-weight: normal; color: #6b7280;">estimated engagements</span>
                </div>
                <p style="margin: 4px 0; color: #374151;">❤️ <b>Estimated Likes:</b> {est_likes:,}</p>
                <p style="margin: 4px 0; color: #374151;">💬 <b>Estimated Comments:</b> {est_comments:,}</p>
                <p style="margin: 4px 0; color: #374151;">🚀 <b>Estimated Shares:</b> {est_shares:,}</p>
                <hr style="margin: 10px 0;">
                <p style="margin: 0; color: #047857; font-weight: 600;">📈 <b>Projected Engagement Rate:</b> {est_rate_pct}%</p>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 3: DATA EXPLORER ---
    with tab3:
        st.markdown("<div class='section-header'>📋 Dataset Explorer</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        # Download CSV button
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered Data as CSV",
            data=csv_data,
            file_name="social_media_filtered.csv",
            mime="text/csv",
        )

# -------------------------------------------------------------
# 6. Footer
# -------------------------------------------------------------
st.markdown("---")
st.caption("Built with Python & Streamlit | Social Media Content Analyzer")
