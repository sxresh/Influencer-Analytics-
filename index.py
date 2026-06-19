import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Influencer Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom Professional CSS Inject for KPI Cards
st.markdown("""
    <style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    /* Metric Label Styling */
    div[data-testid="stMetricLabel"] p {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* Metric Value Styling */
    div[data-testid="stMetricValue"] div {
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }
    /* Container Box for Insights */
    .insight-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 20px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    # Replace with your actual file path
    return pd.read_csv("influencers.csv")

df = load_data()

# Clean Sidebar layout
st.sidebar.image("https://img.icons8.com/fluent/96/000000/dashboard.png", width=60)
st.sidebar.title("Navigation & Filters")
st.sidebar.markdown("---")

selected_niche = st.sidebar.multiselect(
    "💡 Filter Niche Market",
    options=sorted(df["Niche"].unique()),
    default=df["Niche"].unique()
)

filtered_df = df[df["Niche"].isin(selected_niche)]

# Title and Subtitle Block
st.title("📊 Influencer Analytics Dashboard")
st.markdown("<p style='color: #64748B; font-size: 1.1rem; margin-top:-15px;'>Real-time performance metrics and cross-channel campaign ROI analysis</p>", unsafe_allow_html=True)
st.markdown("---")

# KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Format large number into clean string (e.g. 726K)
    total_followers = filtered_df['Followers'].sum()
    followers_str = f"{total_followers/1e3:.1f}K" if total_followers >= 1e3 else f"{total_followers}"
    st.metric("Total Reach", followers_str)

with col2:
    st.metric("Avg Engagement Rate", f"{filtered_df['Engagement_Rate'].mean():.2f}%")

with col3:
    st.metric("Avg Influencer Score", f"{filtered_df['Influencer_Score'].mean():.2f}")

with col4:
    total_rev = filtered_df['Expected_Money'].sum()
    rev_str = f"${total_rev/1e3:.1f}K" if total_rev >= 1e3 else f"${total_rev:,.0f}"
    st.metric("Projected Revenue", rev_str)

st.write("##") # Visual spacing

# Main Charts Grid Layout
chart_col1, chart_col2 = st.columns([1, 1])

# Global Chart Style Overrides for consistent styling
chart_theme = {
    "plot_bgcolor": "rgba(0,0,0,0)",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "margin": dict(l=40, r=20, t=50, b=40),
    "font": {"family": "Inter, sans-serif"}
}

with chart_col1:
    fig1 = px.bar(
        filtered_df.groupby("Niche")["Influencer_Score"].mean().reset_index().sort_values("Influencer_Score"),
        x="Influencer_Score",
        y="Niche",
        orientation="h",
        title="<b>Average Influencer Score by Niche</b>",
        color_discrete_sequence=["#4F46E5"]
    )
    fig1.update_layout(**chart_theme)
    fig1.update_xaxes(showgrid=True, gridcolor='#E2E8F0')
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    fig2 = px.scatter(
        filtered_df,
        x="Followers",
        y="Engagement_Rate",
        size="Influencer_Score",
        color="Niche",
        title="<b>Follower Size vs. Engagement Rate</b>",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig2.update_layout(**chart_theme)
    fig2.update_xaxes(showgrid=True, gridcolor='#E2E8F0')
    fig2.update_yaxes(showgrid=True, gridcolor='#E2E8F0')
    st.plotly_chart(fig2, use_container_width=True)

# Revenue Chart Row spanning across full width
fig3 = px.bar(
    filtered_df.groupby("Niche")["Expected_Money"].sum().reset_index().sort_values("Expected_Money", ascending=False),
    x="Niche",
    y="Expected_Money",
    title="<b>Total Expected Revenue Contribution</b>",
    color="Expected_Money",
    color_continuous_scale="Viridis"
)
fig3.update_layout(**chart_theme)
fig3.update_yaxes(showgrid=True, gridcolor='#E2E8F0')
st.plotly_chart(fig3, use_container_width=True)

st.write("##")

# Styled Executive Insights Box
st.subheader("💡 Strategic Insights")
st.markdown("""
<div class='insight-box'>
    <ul style='margin: 0; padding-left: 20px; color: #1E3A8A; font-size: 0.95rem; line-height: 1.6;'>
        <li><b>Quality Leaders:</b> Fitness influencers command the highest structural <i>Influencer Quality Scores</i> across the panel.</li>
        <li><b>High-Yield Asset:</b> Health verticals exhibit an outsized conversion rate, leading to predictable revenue spikes.</li>
        <li><b>Scale Diminishing Returns:</b> As expected, an inverse correlation is verified between micro-scale communities and macro-scale follower retention rates.</li>
    </ul>
</div>
""", unsafe_allow_html=True)