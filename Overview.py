"""
Page 1: Overview - The Command Center
High-level summary of Paris 2024 Olympic Games
"""

import streamlit as st
from pathlib import Path
import pandas as pd
from config.config import COLORS, PAGE_CONFIG, MEDAL_COLORS
from utils.data_loader import load_athletes, load_medals_total, load_nocs, load_events, load_medals, load_medallists, load_all_sport_results
from utils.data_processor import add_continent_to_dataframe, normalize_medal_columns
from utils.filters import create_sidebar_filters, apply_filters, show_filter_summary
from utils.metrics import (
    calculate_total_athletes, calculate_total_countries, calculate_total_sports,
    calculate_total_medals, calculate_total_events, calculate_medal_distribution
)
from utils.visualizations import create_medal_distribution_pie, create_top_countries_bar

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Load custom CSS
css_file = Path("assets/styles.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
logo_path = Path("assets/logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(logo_path))
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<h1 style='text-align: center; color: {COLORS['paris_green']}; font-size: 2.5rem; margin: 0;'>
    Paris 2024 Olympics Dashboard
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    🏠 The Command Center - Your Gateway to Olympic Excellence
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
<div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['paris_green']}; margin-bottom: 20px;'>
    <p style='color: {COLORS['text']}; font-size: 1.1rem; margin: 0;'>
        Welcome to the <strong>Paris 2024 Olympics Dashboard</strong>! 🔥<br><br>
        This interactive command center provides comprehensive insights into the Paris 2024 Olympic Games.
        Explore athlete performances, medal distributions, global trends, and event schedules.<br><br>
        <strong>👈 Use the sidebar</strong> to navigate between pages and apply filters!
    </p>
</div>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_all_overview_data():
    """Load and prepare all data for overview page."""
    athletes_df = load_athletes()
    medals_total_df = load_medals_total()
    nocs_df = load_nocs()
    events_df = load_events()
    medals_df = load_medals()
    medallists_df = load_medallists()
    all_results = load_all_sport_results()
    
    # Normalize and add continent info
    if not medals_total_df.empty:
        medals_total_df = normalize_medal_columns(medals_total_df)
        medals_total_df = add_continent_to_dataframe(medals_total_df)
    
    # Add continent to medallists for filtering
    if not medallists_df.empty:
        from utils.continent_mapper import add_continent_column
        medallists_df = add_continent_column(medallists_df, 'country_code')
    
    return athletes_df, medals_total_df, nocs_df, events_df, medals_df, medallists_df, all_results

athletes_df, medals_total_df, nocs_df, events_df, medals_df, medallists_df, all_results = load_all_overview_data()

# Helper function to normalize sport names (same as Follow Your Country)
def normalize_sport_name(name: str) -> str:
    return str(name).strip().lower() if name is not None else ""

# Function to calculate total sports based on actual participation (same logic as Follow Your Country)
def calculate_total_sports_with_participation(medallists_df, all_results, filters=None):
    """
    Calculate total sports based on actual participation in medallists and results files.
    This matches the logic used in Follow Your Country page.
    """
    sports_from_medals = set()
    sports_from_results = set()
    
    # Get filtered countries from filters
    country_codes_to_check = None
    if filters:
        if 'countries' in filters and "All" not in filters.get('countries', ["All"]):
            # Filters use country names, need to convert to codes for results files
            if not medallists_df.empty:
                country_codes_to_check = set()
                for country_name in filters['countries']:
                    # Try to find matching country codes
                    matching = medallists_df[medallists_df['country'] == country_name]
                    if not matching.empty:
                        country_codes_to_check.update(matching['country_code'].dropna().unique())
                    else:
                        # If not found, assume it's already a code
                        country_codes_to_check.add(country_name)
        elif 'continents' in filters and "All" not in filters.get('continents', ["All"]):
            # Get country codes from continents
            from utils.continent_mapper import get_countries_by_continent
            country_codes_to_check = set()
            for continent in filters['continents']:
                country_codes_to_check.update(get_countries_by_continent(continent))
    
    # Get sports from medallists (respecting filters)
    if not medallists_df.empty and "discipline" in medallists_df.columns:
        filtered_medallists = medallists_df.copy()
        
        # Apply filters if provided
        if filters:
            # Apply continent filter
            if 'continents' in filters and "All" not in filters.get('continents', ["All"]):
                if 'continent' not in filtered_medallists.columns:
                    from utils.continent_mapper import add_continent_column
                    filtered_medallists = add_continent_column(filtered_medallists, 'country_code')
                if 'continent' in filtered_medallists.columns:
                    filtered_medallists = filtered_medallists[filtered_medallists['continent'].isin(filters['continents'])]
            
            # Apply country filter
            if 'countries' in filters and "All" not in filters.get('countries', ["All"]):
                country_col = 'country' if 'country' in filtered_medallists.columns else 'country_code'
                if country_col in filtered_medallists.columns:
                    filtered_medallists = filtered_medallists[filtered_medallists[country_col].isin(filters['countries'])]
            
            # Apply gender filter
            if 'gender' in filters and filters.get('gender') != "All":
                gender_col = 'gender' if 'gender' in filtered_medallists.columns else None
                if gender_col:
                    filtered_medallists = filtered_medallists[filtered_medallists[gender_col].str.strip().str.title() == filters['gender']]
        
        sports_from_medals = set(filtered_medallists["discipline"].dropna().unique())
    
    # Get sports from results files (respecting filters)
    if all_results:
        # Check each sport's results file
        for sport_key, df in all_results.items():
            if not df.empty and "participant_country_code" in df.columns:
                if country_codes_to_check:
                    # Check if any filtered country participated
                    if df["participant_country_code"].isin(country_codes_to_check).any():
                        sports_from_results.add(sport_key)
                else:
                    # No country filter, include all sports with results
                    sports_from_results.add(sport_key)
    
    # Combine and normalize (same as Follow Your Country)
    all_sports = {normalize_sport_name(s) for s in sports_from_medals} | {normalize_sport_name(s) for s in sports_from_results}
    return len(all_sports)

# ===== FILTERS =====
filters = create_sidebar_filters(athletes_df, medallists_df, events_df, show_sport=False)

# For gender/athlete-specific filters, we need to filter medallists and aggregate
if filters.get('gender') != "All" or filters.get('age_range') is not None:
    # Filter medallists based on gender/age
    filtered_medallists = apply_filters(medallists_df, filters) if not medallists_df.empty else medallists_df
    
    # Aggregate filtered medallists to create medals_total-like data
    if not filtered_medallists.empty:
        # IMPORTANT: Remove duplicates for team events
        # Each medal should be counted once per country, not once per athlete
        # Group by country, medal_type, discipline, event to get unique medals
        unique_medals = filtered_medallists.groupby(
            ['country_code', 'country', 'medal_type', 'discipline', 'event']
        ).first().reset_index()
        
        # Now count medals by country
        country_col = 'country' if 'country' in unique_medals.columns else 'country_code'
        
        # Count each medal type
        medal_counts = unique_medals.groupby([country_col, 'medal_type']).size().unstack(fill_value=0)
        
        # Create base dataframe with country
        filtered_medals_total = pd.DataFrame({country_col: medal_counts.index})
        
        # Add country name if we have country_code
        if country_col == 'country_code' and 'country' in unique_medals.columns:
            country_names = unique_medals[['country_code', 'country']].drop_duplicates()
            filtered_medals_total = filtered_medals_total.merge(country_names, on='country_code', how='left')
        
        # Add medal type columns
        for medal in ['Gold Medal', 'Silver Medal', 'Bronze Medal']:
            col_name = medal.split()[0]  # 'Gold', 'Silver', 'Bronze'
            if medal in medal_counts.columns:
                filtered_medals_total[col_name] = medal_counts[medal].values
            else:
                filtered_medals_total[col_name] = 0
        
        # Ensure numeric types
        filtered_medals_total[['Gold', 'Silver', 'Bronze']] = filtered_medals_total[['Gold', 'Silver', 'Bronze']].fillna(0).astype(int)
        
        # Calculate Total
        filtered_medals_total['Total'] = filtered_medals_total[['Gold', 'Silver', 'Bronze']].sum(axis=1)
        
        # Add continent info
        from utils.continent_mapper import add_continent_column
        if 'continent' not in filtered_medals_total.columns:
            # Use the appropriate column for continent mapping
            continent_col = 'country_code' if 'country_code' in filtered_medals_total.columns else 'country'
            filtered_medals_total = add_continent_column(filtered_medals_total, continent_col)
        
        # Sort by Total medals
        filtered_medals_total = filtered_medals_total.sort_values('Total', ascending=False).reset_index(drop=True)
    else:
        filtered_medals_total = pd.DataFrame()
else:
    # No gender/age filter, use pre-aggregated medals_total
    filtered_medals_total = apply_filters(medals_total_df, filters) if not medals_total_df.empty else medals_total_df

filtered_athletes = apply_filters(athletes_df, filters) if not athletes_df.empty else athletes_df
filtered_events = apply_filters(events_df, filters) if not events_df.empty else events_df

# Show filter summary in sidebar
show_filter_summary(filters, filtered_medals_total, medals_total_df)



# ===== KPI METRICS =====
st.header("📊 Key Performance Indicators")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Real-time metrics that respond to your filter selections</p>", unsafe_allow_html=True)

kpi_data = [
    ("👥", "Total Athletes", calculate_total_athletes(filtered_athletes), COLORS['paris_green']),
    ("🌍", "Total Countries", calculate_total_countries(filtered_medals_total), COLORS['secondary']),
    ("🏃", "Total Sports", calculate_total_sports_with_participation(medallists_df, all_results, filters), COLORS['warning']),
    ("🏅", "Total Medals", calculate_total_medals(filtered_medals_total), COLORS['gold']),
    ("🎯", "Number of Events", calculate_total_events(filtered_events), COLORS['danger'])
]

cols = st.columns(5)
for col, (icon, label, value, color) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['secondary_bg']} 100%);
                    padding: 25px; border-radius: 15px; text-align: center;
                    border: 2px solid {color}; transition: transform 0.3s;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>{icon}</div>
            <h2 style='color: {color}; margin: 10px 0; font-size: 2.5rem;'>{value:,}</h2>
            <p style='color: {COLORS['text']}; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ===== VISUALIZATIONS =====
st.header("📈 Key Visualizations")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 Global Medal Distribution")
    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 15px;'>Breakdown of Gold, Silver, and Bronze medals awarded</p>", unsafe_allow_html=True)
    
    if not filtered_medals_total.empty:
        fig_pie = create_medal_distribution_pie(filtered_medals_total)
        if fig_pie.data:
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Medal counts below
            medal_dist = calculate_medal_distribution(filtered_medals_total)
            m1, m2, m3 = st.columns(3)
            m1.metric("🥇 Gold", f"{medal_dist['Gold']:,}")
            m2.metric("🥈 Silver", f"{medal_dist['Silver']:,}")
            m3.metric("🥉 Bronze", f"{medal_dist['Bronze']:,}")
        else:
            st.warning("No medal data available for the selected filters.")
    else:
        st.info("No data available. Please adjust your filters.")

with col_right:
    st.subheader("🏆 Top 10 Medal Standings")
    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 15px;'>Countries leading the medal race</p>", unsafe_allow_html=True)
    
    if not filtered_medals_total.empty:
        fig_bar = create_top_countries_bar(filtered_medals_total, n=10)
        if fig_bar.data:
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Podium
            top_3 = filtered_medals_total.nlargest(3, 'Total')
            if len(top_3) >= 3:
                country_col = 'country' if 'country' in top_3.columns else 'country_code'
                p1, p2, p3 = st.columns(3)
                
                # Silver (2nd)
                with p1:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; 
                                border-radius: 15px; border: 3px solid {COLORS['silver']}; 
                                box-shadow: 0 0 20px {COLORS['silver']}50;'>
                        <div style='font-size: 3rem; margin-bottom: 10px;'>🥈</div>
                        <h3 style='color: {COLORS['silver']}; margin: 10px 0; font-size: 1.3rem;'>{top_3.iloc[1][country_col]}</h3>
                        <p style='color: {COLORS['text']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{int(top_3.iloc[1]['Total'])}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Gold (1st)
                with p2:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 25px; background: {COLORS['card_bg']}; 
                                border-radius: 15px; border: 4px solid {COLORS['gold']}; 
                                box-shadow: 0 0 30px {COLORS['gold']}80; transform: scale(1.08);'>
                        <div style='font-size: 4rem; margin-bottom: 10px;'>🥇</div>
                        <h3 style='color: {COLORS['gold']}; margin: 10px 0; font-size: 1.5rem;'>{top_3.iloc[0][country_col]}</h3>
                        <p style='color: {COLORS['text']}; margin: 0; font-size: 2rem; font-weight: bold;'>{int(top_3.iloc[0]['Total'])}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Bronze (3rd)
                with p3:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; 
                                border-radius: 15px; border: 3px solid {COLORS['bronze']}; 
                                box-shadow: 0 0 20px {COLORS['bronze']}50;'>
                        <div style='font-size: 3rem; margin-bottom: 10px;'>🥉</div>
                        <h3 style='color: {COLORS['bronze']}; margin: 10px 0; font-size: 1.3rem;'>{top_3.iloc[2][country_col]}</h3>
                        <p style='color: {COLORS['text']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{int(top_3.iloc[2]['Total'])}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>medals</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Could not generate chart. Check data columns.")
    else:
        st.info("No data available. Please adjust your filters.")

st.markdown("---")

# ===== QUICK INSIGHTS =====
st.header("💡 Quick Insights")

if not filtered_medals_total.empty and 'Total' in filtered_medals_total.columns:
    i1, i2, i3 = st.columns(3)
    
    with i1:
        country_col = 'country' if 'country' in filtered_medals_total.columns else 'country_code'
        leading = filtered_medals_total.iloc[0]
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['secondary_bg']}); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid {COLORS['paris_green']}; height: 100%;'>
            <h4 style='color: {COLORS['paris_green']}; margin: 0 0 15px 0; font-size: 1.1rem;'>🥇 Leading Nation</h4>
            <p style='color: {COLORS['text']}; font-size: 2rem; font-weight: bold; margin: 0;'>{leading[country_col]}</p>
            <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 1.1rem;'>{int(leading['Total'])} total medals</p>
            <p style='color: {COLORS['text_secondary']}; margin: 5px 0 0 0; font-size: 0.9rem;'>
                🥇 {int(leading['Gold'])} | 🥈 {int(leading['Silver'])} | 🥉 {int(leading['Bronze'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with i2:
        medal_dist = calculate_medal_distribution(filtered_medals_total)
        most_common = max(medal_dist.items(), key=lambda x: x[1])
        icon_map = {'Gold': '🥇', 'Silver': '🥈', 'Bronze': '🥉'}
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['secondary_bg']}); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid {COLORS['secondary']}; height: 100%;'>
            <h4 style='color: {COLORS['secondary']}; margin: 0 0 15px 0; font-size: 1.1rem;'>🏅 Most Common Medal</h4>
            <p style='color: {COLORS['text']}; font-size: 2rem; font-weight: bold; margin: 0;'>{icon_map[most_common[0]]} {most_common[0]}</p>
            <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 1.1rem;'>{most_common[1]:,} medals awarded</p>
            <p style='color: {COLORS['text_secondary']}; margin: 5px 0 0 0; font-size: 0.9rem;'>
                {(most_common[1]/sum(medal_dist.values())*100):.1f}% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with i3:
        avg_medals = filtered_medals_total['Total'].mean()
        median_medals = filtered_medals_total['Total'].median()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['secondary_bg']}); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid {COLORS['warning']}; height: 100%;'>
            <h4 style='color: {COLORS['warning']}; margin: 0 0 15px 0; font-size: 1.1rem;'>📊 Average per Country</h4>
            <p style='color: {COLORS['text']}; font-size: 2rem; font-weight: bold; margin: 0;'>{avg_medals:.1f}</p>
            <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0; font-size: 1.1rem;'>medals per nation</p>
            <p style='color: {COLORS['text_secondary']}; margin: 5px 0 0 0; font-size: 0.9rem;'>
                Median: {median_medals:.0f} medals</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ===== DATA TABLE =====
st.header("📋 Detailed Medal Table")

if not filtered_medals_total.empty:
    display_df = filtered_medals_total[['country', 'country_code', 'continent', 'Gold', 'Silver', 'Bronze', 'Total']].copy() if all(c in filtered_medals_total.columns for c in ['country', 'country_code', 'continent', 'Gold', 'Silver', 'Bronze', 'Total']) else filtered_medals_total
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'country': 'Country',
            'country_code': 'Code',
            'continent': 'Continent',
            'Gold': st.column_config.NumberColumn('🥇 Gold', format='%d'),
            'Silver': st.column_config.NumberColumn('🥈 Silver', format='%d'),
            'Bronze': st.column_config.NumberColumn('🥉 Bronze', format='%d'),
            'Total': st.column_config.NumberColumn('🏆 Total', format='%d')
        }
    )
    
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Medal Data (CSV)",
        data=csv,
        file_name="paris2024_medals.csv",
        mime="text/csv"
    )
else:
    st.info("No data to display. Please adjust your filters.")

# ===== FOOTER =====
st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='padding: 15px; background: {COLORS['card_bg']}; border-radius: 8px; text-align: center;'>
    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.75rem;'>
        Built for <strong>LA28 Volunteer Selection</strong><br>
        ESI-SBA | Dr. Belkacem KHALDI
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align: center; padding: 30px; background: {COLORS['card_bg']}; border-radius: 10px; margin-top: 40px;'>
    <p style='color: {COLORS['text_secondary']}; font-size: 0.9rem;'>
        Built for LA28 Volunteer Selection Challenge<br>
        <strong>ESI-SBA</strong> | Instructor: Dr. Belkacem KHALDI<br>
        Team: BENHAMMADI Lokmane AND BELKAID Abderrahmane yassine hamza
    </p>
</div>
""", unsafe_allow_html=True)