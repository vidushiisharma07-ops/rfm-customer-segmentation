import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="RFM Customer Segmentation", layout="wide", page_icon="🛍️", initial_sidebar_state="expanded")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #0f1117; }
[data-testid="stSidebar"] { background-color: #1a1d27; }
[data-testid="stSidebar"] * { color: #ffffff !important; }
.kpi-card { background: #1a1d27; border-radius: 12px; padding: 20px 24px; border: 1px solid #2a2d3e; }
.kpi-label { font-size: 13px; color: #8b8fa8; margin-bottom: 6px; }
.kpi-value { font-size: 28px; font-weight: 600; color: #ffffff; }
.kpi-sub { font-size: 12px; color: #4ade80; margin-top: 4px; }
.section-title { font-size: 16px; font-weight: 600; color: #ffffff; margin-bottom: 12px; }
div[data-testid="metric-container"] { background: #1a1d27; border-radius: 12px; padding: 16px; border: 1px solid #2a2d3e; }
</style>
""", unsafe_allow_html=True)

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(base, 'data', 'rfm_segments.csv'))

seg_colors = {
    'Champion': '#4ade80',
    'Loyal Customer': '#60a5fa',
    'New Customer': '#a78bfa',
    'Promising': '#fbbf24',
    'At Risk': '#f87171',
    'Cannot Lose Them': '#f472b6',
    'Lost': '#6b7280'
}

st.sidebar.markdown("## 🛍️ RFM Dashboard")
st.sidebar.markdown("**Online Retail II · 2009–2011**")
st.sidebar.markdown("---")
all_segments = df['Segment'].unique().tolist()
selected = st.sidebar.multiselect("Filter by Segment", all_segments, default=all_segments)
df = df[df['Segment'].isin(selected)]

st.markdown("<h1 style='color:white; font-size:28px; font-weight:700;'>RFM Customer Segmentation</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b8fa8; margin-top:-12px;'>Consumer behaviour analytics · UK e-commerce · 2009–2011</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='kpi-card'><div class='kpi-label'>Total Customers</div>
    <div class='kpi-value'>{len(df):,}</div>
    <div class='kpi-sub'>↑ active base</div></div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card'><div class='kpi-label'>Champions</div>
    <div class='kpi-value'>{len(df[df['Segment']=='Champion']):,}</div>
    <div class='kpi-sub'>{len(df[df['Segment']=='Champion'])/len(df)*100:.1f}% of base</div></div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card'><div class='kpi-label'>Avg Monetary Value</div>
    <div class='kpi-value'>£{df['Monetary'].mean():,.0f}</div>
    <div class='kpi-sub'>median spend</div></div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card'><div class='kpi-label'>At Risk</div>
    <div class='kpi-value' style='color:#f87171'>{len(df[df['Segment']=='At Risk']):,}</div>
    <div class='kpi-sub' style='color:#f87171;'>need re-engagement</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='section-title'>Segment Distribution</div>", unsafe_allow_html=True)
    seg_count = df['Segment'].value_counts().reset_index()
    seg_count.columns = ['Segment', 'Count']
    fig1 = px.pie(seg_count, names='Segment', values='Count', color='Segment',
                  color_discrete_map=seg_colors, hole=0.5)
    fig1.update_layout(paper_bgcolor='#1a1d27', plot_bgcolor='#1a1d27',
                       font_color='white', margin=dict(t=10, b=10),
                       legend=dict(font=dict(color='white')))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-title'>Revenue by Segment</div>", unsafe_allow_html=True)
    seg_rev = df.groupby('Segment')['Monetary'].sum().reset_index()
    seg_rev.columns = ['Segment', 'Revenue']
    seg_rev = seg_rev.sort_values('Revenue', ascending=True)
    fig2 = px.bar(seg_rev, x='Revenue', y='Segment', orientation='h',
                  color='Segment', color_discrete_map=seg_colors)
    fig2.update_layout(paper_bgcolor='#1a1d27', plot_bgcolor='#1a1d27',
                       font_color='white', margin=dict(t=10, b=10),
                       showlegend=False,
                       xaxis=dict(gridcolor='#2a2d3e'),
                       yaxis=dict(gridcolor='#2a2d3e'))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='section-title'>Recency vs Monetary Value</div>", unsafe_allow_html=True)
fig3 = px.scatter(df, x='Recency', y='Monetary', color='Segment',
                  color_discrete_map=seg_colors,
                  hover_data=['Customer ID', 'Frequency'], opacity=0.7)
fig3.update_layout(paper_bgcolor='#1a1d27', plot_bgcolor='#1a1d27',
                   font_color='white', margin=dict(t=10, b=10),
                   xaxis=dict(gridcolor='#2a2d3e'),
                   yaxis=dict(gridcolor='#2a2d3e'),
                   legend=dict(font=dict(color='white')))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("<div class='section-title'>Customer Table</div>", unsafe_allow_html=True)
st.dataframe(df[['Customer ID', 'Segment', 'Recency', 'Frequency', 'Monetary']].sort_values('Monetary', ascending=False).reset_index(drop=True), use_container_width=True)