"""
Page 2: Global Analysis - The World View
Geographical and hierarchical perspective of Olympic performance
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.config import COLORS, PAGE_CONFIG, MEDAL_COLORS
from utils.data_loader import load_medals, load_nocs
from utils.filters import create_sidebar_filters, apply_filters
from utils.continent_mapper import add_continent_column

# Page configuration
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path("assets/styles.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown(f"""
<h1 style='text-align: center; color: {COLORS['paris_green']}; font-size: 2.5rem; margin: 0;'>
    🗺️ Global Analysis - The World View
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    Geographical and Hierarchical Perspective of Olympic Performance
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_global_data():
    """Load and prepare data for global analysis."""
    medals_df = load_medals()
    nocs_df = load_nocs()
    
    # Add continent info for medals
    if not medals_df.empty and 'country_code' in medals_df.columns:
        medals_df = add_continent_column(medals_df, 'country_code')
    
    return medals_df, nocs_df

medals_df, nocs_df = load_global_data()

# ===== SIDEBAR FILTERS =====
filters = create_sidebar_filters(
    medals_df=medals_df,
    show_sport=False  # Sport filtering done in other pages
)

# Apply filters to medals data
filtered_medals = apply_filters(medals_df, filters)

# Calculate aggregated totals from filtered individual medals (medals.csv)
if not filtered_medals.empty:
    # Group by country to get totals
    medals_by_country = filtered_medals.groupby(['country_code', 'country', 'continent']).agg(
        Gold=('medal_type', lambda x: (x == 'Gold Medal').sum()),
        Silver=('medal_type', lambda x: (x == 'Silver Medal').sum()),
        Bronze=('medal_type', lambda x: (x == 'Bronze Medal').sum())
    ).reset_index()
    
    # Calculate display total based on selected medal types
    medals_by_country['Display_Total'] = 0
    if 'Gold' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze']):
        medals_by_country['Display_Total'] += medals_by_country['Gold']
    if 'Silver' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze']):
        medals_by_country['Display_Total'] += medals_by_country['Silver']
    if 'Bronze' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze']):
        medals_by_country['Display_Total'] += medals_by_country['Bronze']
    
    # Remove countries with 0 medals after filtering
    medals_by_country = medals_by_country[medals_by_country['Display_Total'] > 0]
    medals_by_country['Total'] = medals_by_country['Gold'] + medals_by_country['Silver'] + medals_by_country['Bronze']
else:
    medals_by_country = pd.DataFrame()

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Showing data for **{len(medals_by_country)}** countries")

# ===== 1. WORLD MEDAL MAP =====
st.header("🌍 World Medal Map")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Global distribution of Olympic medals by country</p>", unsafe_allow_html=True)

if not medals_by_country.empty:
    fig_map = px.choropleth(
        medals_by_country,
        locations='country_code',
        locationmode='ISO-3',
        color='Display_Total',
        hover_name='country',
        hover_data={
            'country_code': False,
            'continent': True,
            'Display_Total': True,
            'Gold': True,
            'Silver': True,
            'Bronze': True
        },
        color_continuous_scale=[
            [0, COLORS['background']],
            [0.3, COLORS['secondary']],
            [0.6, COLORS['paris_green']],
            [1, COLORS['gold']]
        ],
        labels={'Display_Total': 'Total Medals'},
        template='plotly_dark'
    )
    
    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor=COLORS['background'],
            landcolor=COLORS['card_bg'],
            oceancolor=COLORS['background']
        ),
        height=550,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

st.markdown("---")

# ===== 2. MEDAL HIERARCHY BY CONTINENT =====
st.header("🎯 Medal Hierarchy by Continent")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Drill-down view: Continent → Country → Sport → Medals</p>", unsafe_allow_html=True)

from utils.visualizations import create_enhanced_sunburst, create_enhanced_treemap

tab1, tab2 = st.tabs(["📊 Sunburst Chart", "🗂️ Treemap"])

# Prepare hierarchy data from filtered medals
grouped = None
sport_col = None

if not filtered_medals.empty and 'continent' in filtered_medals.columns:
    # Determine sport column
    sport_col = 'discipline' if 'discipline' in filtered_medals.columns else 'sport'
    
    # Group for hierarchy - count individual medals
    if sport_col in filtered_medals.columns:
        try:
            grouped = filtered_medals.groupby(['continent', 'country', sport_col]).size().reset_index(name='medal_count')
        except Exception as e:
            st.error(f"Error creating hierarchy: {str(e)}")

with tab1:
    if grouped is not None and not grouped.empty:
        fig_sunburst = create_enhanced_sunburst(
            grouped, 
            ['continent', 'country', sport_col], 
            'medal_count',
            title="Interactive Medal Hierarchy"
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Stats below
        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Continents", grouped['continent'].nunique())
        col2.metric("🌎 Countries", grouped['country'].nunique())
        col3.metric("🏅 Sports", grouped[sport_col].nunique())
    else:
        st.info("No hierarchical data available for the selected filters.")

with tab2:
    if grouped is not None and not grouped.empty:
        fig_treemap = create_enhanced_treemap(
            grouped,
            ['continent', 'country', sport_col],
            'medal_count',
            title="Medal Distribution Treemap"
        )
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Top performer
        top_country = grouped.groupby('country')['medal_count'].sum().nlargest(1)
        if not top_country.empty:
            st.success(f"🏆 **Top Performer:** {top_country.index[0]} with **{top_country.values[0]:,}** medals")
    else:
        st.info("No hierarchical data available for the selected filters.")

st.markdown("---")

# ===== 3. CONTINENT VS MEDALS BAR CHART =====
st.header("📊 Continent vs. Medals Comparison")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Medal distribution across continents</p>", unsafe_allow_html=True)

from utils.visualizations import create_grouped_bar_chart

if not medals_by_country.empty:
    continent_medals = medals_by_country.groupby('continent')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    continent_medals['Total'] = continent_medals['Gold'] + continent_medals['Silver'] + continent_medals['Bronze']
    continent_medals = continent_medals.sort_values('Total', ascending=False)
    
    # Determine which medals to show based on filters
    show_gold = 'Gold' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    show_silver = 'Silver' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    show_bronze = 'Bronze' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    
    fig_continent = create_grouped_bar_chart(
        continent_medals,
        show_gold=show_gold,
        show_silver=show_silver,
        show_bronze=show_bronze,
        title="Continental Medal Showdown",
        orientation='v'
    )
    st.plotly_chart(fig_continent, use_container_width=True)
    
    # Continent insights
    col1, col2 = st.columns(2)
    with col1:
        leading_continent = continent_medals.iloc[0]
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['paris_green']}20);
                    padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['paris_green']};'>
            <h4 style='color: {COLORS['paris_green']}; margin: 0 0 10px 0;'>🌟 Leading Continent</h4>
            <p style='color: {COLORS['text']}; font-size: 1.8rem; font-weight: bold; margin: 0;'>{leading_continent['continent']}</p>
            <p style='color: {COLORS['text_secondary']}; margin: 5px 0 0 0;'>{int(leading_continent['Total'])} total medals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_continents = len(continent_medals)
        total_medals_all = continent_medals['Total'].sum()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['secondary']}20);
                    padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['secondary']};'>
            <h4 style='color: {COLORS['secondary']}; margin: 0 0 10px 0;'>📊 Global Stats</h4>
            <p style='color: {COLORS['text']}; font-size: 1.5rem; font-weight: bold; margin: 0;'>{total_continents} Continents</p>
            <p style='color: {COLORS['text_secondary']}; margin: 5px 0 0 0;'>{int(total_medals_all):,} medals distributed</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No data available for the selected filters.")

st.markdown("---")

# ===== 4. TOP 20 COUNTRIES VS MEDALS =====
st.header("🏆 Top 20 Countries Medal Rankings")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Elite nations leading the Olympic medal race</p>", unsafe_allow_html=True)

if not medals_by_country.empty:
    top_20 = medals_by_country.nlargest(20, 'Display_Total')
    
    # Determine which medals to show based on filters
    show_gold = 'Gold' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    show_silver = 'Silver' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    show_bronze = 'Bronze' in filters.get('medal_types', ['Gold', 'Silver', 'Bronze'])
    
    fig_top20 = create_grouped_bar_chart(
        top_20,
        show_gold=show_gold,
        show_silver=show_silver,
        show_bronze=show_bronze,
        title="Top 20 Medal Champions",
        orientation='h',
        n=20
    )
    # Make it stacked for horizontal
    fig_top20.update_layout(barmode='stack')
    st.plotly_chart(fig_top20, use_container_width=True)
    
    # Podium display
    if len(top_20) >= 3:
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['paris_green']}; margin: 30px 0 20px 0;'>🏅 Olympic Podium</h3>", unsafe_allow_html=True)
        
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.markdown(f"""
            <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['silver']}20);
                        border-radius: 15px; border: 3px solid {COLORS['silver']}; 
                        box-shadow: 0 5px 30px {COLORS['silver']}40; transform: translateY(20px);'>
                <div style='font-size: 4rem; margin-bottom: 10px;'>🥈</div>
                <h3 style='color: {COLORS['silver']}; margin: 10px 0; font-size: 1.5rem; font-family: Arial Black;'>{top_20.iloc[1]['country']}</h3>
                <p style='color: {COLORS['text']}; margin: 0; font-size: 2rem; font-weight: bold;'>{int(top_20.iloc[1]['Display_Total'])}</p>
                <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>Total Medals</p>
                <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 0.95rem;'>
                    🥇 {int(top_20.iloc[1]['Gold'])} | 🥈 {int(top_20.iloc[1]['Silver'])} | 🥉 {int(top_20.iloc[1]['Bronze'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with p2:
            st.markdown(f"""
            <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['gold']}30);
                        border-radius: 15px; border: 4px solid {COLORS['gold']}; 
                        box-shadow: 0 8px 40px {COLORS['gold']}60; transform: scale(1.1);'>
                <div style='font-size: 5rem; margin-bottom: 10px;'>🥇</div>
                <h3 style='color: {COLORS['gold']}; margin: 10px 0; font-size: 1.8rem; font-family: Arial Black;'>{top_20.iloc[0]['country']}</h3>
                <p style='color: {COLORS['text']}; margin: 0; font-size: 2.5rem; font-weight: bold;'>{int(top_20.iloc[0]['Display_Total'])}</p>
                <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1.1rem;'>Total Medals</p>
                <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 1rem;'>
                    🥇 {int(top_20.iloc[0]['Gold'])} | 🥈 {int(top_20.iloc[0]['Silver'])} | 🥉 {int(top_20.iloc[0]['Bronze'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with p3:
            st.markdown(f"""
            <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['bronze']}20);
                        border-radius: 15px; border: 3px solid {COLORS['bronze']}; 
                        box-shadow: 0 5px 30px {COLORS['bronze']}40; transform: translateY(20px);'>
                <div style='font-size: 4rem; margin-bottom: 10px;'>🥉</div>
                <h3 style='color: {COLORS['bronze']}; margin: 10px 0; font-size: 1.5rem; font-family: Arial Black;'>{top_20.iloc[2]['country']}</h3>
                <p style='color: {COLORS['text']}; margin: 0; font-size: 2rem; font-weight: bold;'>{int(top_20.iloc[2]['Display_Total'])}</p>
                <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>Total Medals</p>
                <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 0.95rem;'>
                    🥇 {int(top_20.iloc[2]['Gold'])} | 🥈 {int(top_20.iloc[2]['Silver'])} | 🥉 {int(top_20.iloc[2]['Bronze'])}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No data available for the selected filters.")

# ===== FOOTER =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 30px; background: {COLORS['card_bg']}; border-radius: 10px; margin-top: 40px;'>
    <p style='color: {COLORS['text_secondary']}; font-size: 0.9rem;'>
        Built for LA28 Volunteer Selection Challenge<br>
        <strong>ESI-SBA</strong> | Instructor: Dr. Belkacem KHALDI<br>
        Team: BENHAMMADI Lokmane AND BELKAID Abderrahmane yassine hamza
    </p>
</div>
""", unsafe_allow_html=True)