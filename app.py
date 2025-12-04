import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
from config.config import COLORS, PAGE_CONFIG, WELCOME_TEXT

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Hide Streamlit menu and deploy button
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Load custom CSS
css_file = Path("assets/styles.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header with logo
st.markdown("<div style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
logo_path = Path("assets/logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(logo_path), use_container_width=True)
else:
    st.title("🔥 Paris 2024 Olympics Dashboard")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### LA28 Volunteer Selection Challenge")
st.markdown("---")

# Welcome section
st.markdown(WELCOME_TEXT)

# Quick stats section
st.header("📊 Quick Overview")

# Try to load real data, fall back to sample if not available
@st.cache_data
def load_data():
    try:
        # Try to load real data
        medals_total = pd.read_csv("data/medals_total.csv")
        return medals_total, True
    except:
        # Fallback sample data
        sample = {
            'country_code': ['USA', 'CHN', 'JPN', 'GBR', 'FRA'],
            'country': ['United States', 'China', 'Japan', 'Great Britain', 'France'],
            'Gold': [40, 40, 20, 14, 16],
            'Silver': [44, 27, 12, 22, 26],
            'Bronze': [42, 24, 13, 29, 22]
        }
        df = pd.DataFrame(sample)
        df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
        return df, False

medals_df, real_data = load_data()

# Determine country column name
country_col = 'country' if 'country' in medals_df.columns else 'country_code'
if country_col not in medals_df.columns:
    country_col = medals_df.columns[0]

# Display metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                border: 2px solid {COLORS['gold']}; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);'>
        <h3 style='color: {COLORS['gold']}; margin: 0;'>🌍</h3>
        <h2 style='color: {COLORS['gold']}; margin: 10px 0;'>{len(medals_df)}</h2>
        <p style='color: {COLORS['text']}; margin: 0;'>Countries</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_gold = medals_df['Gold'].sum() if 'Gold' in medals_df.columns else 0
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                border: 2px solid {COLORS['gold']}; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);'>
        <h3 style='color: {COLORS['gold']}; margin: 0;'>🥇</h3>
        <h2 style='color: {COLORS['gold']}; margin: 10px 0;'>{total_gold}</h2>
        <p style='color: {COLORS['text']}; margin: 0;'>Gold Medals</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_silver = medals_df['Silver'].sum() if 'Silver' in medals_df.columns else 0
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                border: 2px solid {COLORS['silver']}; box-shadow: 0 0 20px rgba(192, 192, 192, 0.3);'>
        <h3 style='color: {COLORS['silver']}; margin: 0;'>🥈</h3>
        <h2 style='color: {COLORS['silver']}; margin: 10px 0;'>{total_silver}</h2>
        <p style='color: {COLORS['text']}; margin: 0;'>Silver Medals</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_bronze = medals_df['Bronze'].sum() if 'Bronze' in medals_df.columns else 0
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                border: 2px solid {COLORS['bronze']}; box-shadow: 0 0 20px rgba(205, 127, 50, 0.3);'>
        <h3 style='color: {COLORS['bronze']}; margin: 0;'>🥉</h3>
        <h2 style='color: {COLORS['bronze']}; margin: 10px 0;'>{total_bronze}</h2>
        <p style='color: {COLORS['text']}; margin: 0;'>Bronze Medals</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    total_medals = total_gold + total_silver + total_bronze
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                border: 2px solid {COLORS['primary']}; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);'>
        <h3 style='color: {COLORS['primary']}; margin: 0;'>🏆</h3>
        <h2 style='color: {COLORS['primary']}; margin: 10px 0;'>{total_medals}</h2>
        <p style='color: {COLORS['text']}; margin: 0;'>Total Medals</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Data preview
st.header("🏆 Medal Standings")

# Display top countries
top_n = 10 if real_data else 5
top_countries = medals_df.head(top_n).copy()
st.dataframe(top_countries, use_container_width=True, hide_index=True)

# Visualizations
st.header("📊 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Medal Distribution by Country")
    
    # Reshape data for grouped bar chart
    top_for_chart = top_countries.copy()
    chart_data = []
    for _, row in top_for_chart.iterrows():
        country_name = row[country_col]
        chart_data.append({'Country': country_name, 'Medal Type': 'Gold', 'Count': row.get('Gold', 0)})
        chart_data.append({'Country': country_name, 'Medal Type': 'Silver', 'Count': row.get('Silver', 0)})
        chart_data.append({'Country': country_name, 'Medal Type': 'Bronze', 'Count': row.get('Bronze', 0)})
    
    chart_df = pd.DataFrame(chart_data)
    
    fig_bar = px.bar(
        chart_df,
        x='Country',
        y='Count',
        color='Medal Type',
        title=f"Top {len(top_for_chart)} Countries - Medal Count",
        labels={'Count': 'Number of Medals'},
        color_discrete_map={
            'Gold': COLORS['gold'], 
            'Silver': COLORS['silver'], 
            'Bronze': COLORS['bronze']
        },
        template='plotly_dark',
        barmode='group'
    )
    fig_bar.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Total Medals Distribution")
    medal_totals = pd.DataFrame({
        'Medal Type': ['Gold', 'Silver', 'Bronze'],
        'Count': [total_gold, total_silver, total_bronze]
    })
    fig_pie = px.pie(
        medal_totals,
        values='Count',
        names='Medal Type',
        title='Overall Medal Distribution',
        color='Medal Type',
        color_discrete_map={
            'Gold': COLORS['gold'],
            'Silver': COLORS['silver'],
            'Bronze': COLORS['bronze']
        },
        template='plotly_dark'
    )
    fig_pie.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Navigation section
st.markdown("---")
st.header("🗺️ Explore More")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['primary']}; text-align: center;'>
        <h3>🏠 Overview</h3>
        <p>Key metrics and highlights</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['secondary']}; text-align: center;'>
        <h3>🗺️ Global Analysis</h3>
        <p>Geographical insights</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['success']}; text-align: center;'>
        <h3>👤 Athletes</h3>
        <p>Performance analysis</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['warning']}; text-align: center;'>
        <h3>🏟️ Sports & Events</h3>
        <p>Competition schedules</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['danger']}; text-align: center;'>
        <h3>🎯 Advanced Analytics</h3>
        <p>Deep dive insights</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                border: 2px solid {COLORS['accent']}; text-align: center;'>
        <h3>⚔️ Country Comparison</h3>
        <p>Head-to-head analysis</p>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 Use the sidebar to navigate to different pages and apply filters!")

# Data status
st.markdown("---")
if real_data:
    st.success("✅ Real Paris 2024 Olympic data loaded successfully!")
else:
    st.warning("⚠️ Using sample data. Place CSV files in the `data/` folder to load real data.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
if logo_path.exists():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(str(logo_path), width=150)
st.markdown(f"""
<p style='color: {COLORS['text_secondary']}; text-align: center;'>
    Built with ❤️ for LA28 Volunteer Selection<br>
    <strong>ESI-SBA</strong> | Instructor: Dr. Belkacem KHALDI
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)