"""
Page 4: Sports and Events - The Competition Arena
Analyze sports, events, schedules, and venues
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.config import COLORS, PAGE_CONFIG
from utils.data_loader import load_events, load_medallists, load_athletes
from utils.filters import create_sidebar_filters, apply_filters, show_filter_summary
from utils.visualizations import create_enhanced_treemap, create_gantt_chart

# Page configuration
st.set_page_config(
    page_title="Sports and Events - Paris 2024",
    page_icon="🏟️",
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
    🏟️ Sports and Events - The Competition Arena
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    Event Schedules, Medal Distributions, and Olympic Venues
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_sports_data():
    """Load and prepare data for sports and events analysis."""
    try:
        schedules_df = pd.read_csv('data/schedules.csv')
        venues_df = pd.read_csv('data/venues.csv')
        medallists_df = pd.read_csv('data/medallists.csv')
        events_df = load_events()
        
        # Parse dates
        if not schedules_df.empty:
            schedules_df['start_date'] = pd.to_datetime(schedules_df['start_date'], errors='coerce')
            schedules_df['end_date'] = pd.to_datetime(schedules_df['end_date'], errors='coerce')
        
        if not venues_df.empty and 'date_start' in venues_df.columns:
            venues_df['date_start'] = pd.to_datetime(venues_df['date_start'], errors='coerce')
            venues_df['date_end'] = pd.to_datetime(venues_df['date_end'], errors='coerce')
        
        return schedules_df, venues_df, medallists_df, events_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

schedules_df, venues_df, medallists_df, events_df = load_sports_data()

# ===== FILTERS =====
filters = create_sidebar_filters(None, medallists_df, events_df)

# Apply filters to medallists
filtered_medallists = apply_filters(medallists_df, filters) if not medallists_df.empty else medallists_df

# Show filter summary
show_filter_summary(filters, filtered_medallists, medallists_df)

# ===== KEY METRICS =====
st.header("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sports = events_df['sport'].nunique() if not events_df.empty and 'sport' in events_df.columns else 0
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['paris_green']}20);
                border-radius: 15px; border: 3px solid {COLORS['paris_green']}; box-shadow: 0 5px 20px rgba(0,0,0,0.3);'>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>Total Sports</p>
        <p style='color: {COLORS['paris_green']}; margin: 10px 0; font-size: 2.5rem; font-weight: bold;'>{total_sports}</p>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Disciplines</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_events = len(events_df) if not events_df.empty else 0
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['secondary']}20);
                border-radius: 15px; border: 3px solid {COLORS['secondary']}; box-shadow: 0 5px 20px rgba(0,0,0,0.3);'>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>Total Events</p>
        <p style='color: {COLORS['secondary']}; margin: 10px 0; font-size: 2.5rem; font-weight: bold;'>{total_events}</p>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Competitions</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_venues = len(venues_df) if not venues_df.empty else 0
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['warning']}20);
                border-radius: 15px; border: 3px solid {COLORS['warning']}; box-shadow: 0 5px 20px rgba(0,0,0,0.3);'>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>Venues</p>
        <p style='color: {COLORS['warning']}; margin: 10px 0; font-size: 2.5rem; font-weight: bold;'>{total_venues}</p>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Locations</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_medals = len(filtered_medallists) if not filtered_medallists.empty else 0
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['gold']}20);
                border-radius: 15px; border: 3px solid {COLORS['gold']}; box-shadow: 0 5px 20px rgba(0,0,0,0.3);'>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;'>Medals Awarded</p>
        <p style='color: {COLORS['gold']}; margin: 10px 0; font-size: 2.5rem; font-weight: bold;'>{total_medals}</p>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Total</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===== 1. EVENT SCHEDULE TIMELINE (GANTT CHART) =====
st.header("📅 Event Schedule Timeline")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Interactive Gantt chart showing event schedules by sport and venue</p>", unsafe_allow_html=True)

if not schedules_df.empty:
    # Sport/Venue selector
    col1, col2 = st.columns(2)
    
    with col1:
        view_by = st.radio("View schedule by:", ["Sport", "Venue"], horizontal=True)
    
    with col2:
        if view_by == "Sport":
            all_sports = sorted(schedules_df['discipline'].dropna().unique())
            selected_item = st.selectbox("Select Sport:", options=['Top 10 Sports'] + all_sports)
        else:
            all_venues = sorted(schedules_df['venue'].dropna().unique())
            selected_item = st.selectbox("Select Venue:", options=['Top 10 Venues'] + all_venues)
    
    # Filter data
    if selected_item.startswith('Top 10'):
        if view_by == "Sport":
            top_items = schedules_df['discipline'].value_counts().head(10).index
            timeline_data = schedules_df[schedules_df['discipline'].isin(top_items)]
            color_col = 'discipline'
        else:
            top_items = schedules_df['venue'].value_counts().head(10).index
            timeline_data = schedules_df[schedules_df['venue'].isin(top_items)]
            color_col = 'venue'
    else:
        if view_by == "Sport":
            timeline_data = schedules_df[schedules_df['discipline'] == selected_item]
            color_col = 'event'
        else:
            timeline_data = schedules_df[schedules_df['venue'] == selected_item]
            color_col = 'discipline'
    
    # Remove rows with missing dates
    timeline_data = timeline_data[timeline_data['start_date'].notna() & timeline_data['end_date'].notna()]
    
    if not timeline_data.empty:
        # Limit to 50 events for performance
        if len(timeline_data) > 50:
            timeline_data = timeline_data.head(50)
            st.info(f"Showing first 50 events out of {len(timeline_data)} total")
        
        # Create Gantt chart
        fig_gantt = px.timeline(
            timeline_data,
            x_start='start_date',
            x_end='end_date',
            y='event',
            color=color_col,
            hover_data=['discipline', 'venue', 'phase', 'gender'],
            labels={'event': 'Event', 'discipline': 'Sport', 'venue': 'Venue'},
            title=f"Event Schedule - {selected_item}"
        )
        
        fig_gantt.update_layout(
            height=600,
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], family='Arial Black'),
            xaxis_title='Date',
            yaxis_title='Event',
            yaxis={'categoryorder': 'total ascending'},
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.info("No schedule data available for the selected filters")
else:
    st.warning("Schedule data not available")

st.markdown("---")

# ===== 2. MEDAL COUNT BY SPORT (TREEMAP) =====
st.header("🎯 Medal Distribution by Sport")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Interactive treemap showing medal distribution across sports and events</p>", unsafe_allow_html=True)

if not filtered_medallists.empty and 'discipline' in filtered_medallists.columns:
    # Prepare treemap data
    sport_event_medals = filtered_medallists.groupby(['discipline', 'event']).size().reset_index(name='medals')
    
    if not sport_event_medals.empty:
        # Create enhanced treemap
        fig_treemap = create_enhanced_treemap(
            sport_event_medals,
            path_cols=['discipline', 'event'],
            value_col='medals',
            title="Medal Distribution: Sport → Event"
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Sport comparison bar chart
        st.subheader("📊 Top 20 Sports by Medal Count")
        
        sport_totals = filtered_medallists.groupby('discipline').size().reset_index(name='total_medals')
        sport_totals = sport_totals.sort_values('total_medals', ascending=False).head(20)
        
        fig_sport_bar = go.Figure()
        
        fig_sport_bar.add_trace(go.Bar(
            x=sport_totals['total_medals'],
            y=sport_totals['discipline'],
            orientation='h',
            marker=dict(
                color=sport_totals['total_medals'],
                colorscale=[
                    [0, COLORS['secondary']],
                    [0.5, COLORS['paris_green']],
                    [1, COLORS['gold']]
                ],
                line=dict(color=COLORS['background'], width=2)
            ),
            text=sport_totals['total_medals'],
            textposition='inside',
            textfont=dict(size=14, color='white', family='Arial Black'),
            hovertemplate='<b>%{y}</b><br>Medals: %{x}<extra></extra>'
        ))
        
        fig_sport_bar.update_layout(
            title=dict(
                text="<b>Top 20 Sports by Medal Count</b>",
                font=dict(size=18, color=COLORS['paris_green'], family='Arial Black'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], family='Arial Black'),
            height=600,
            xaxis_title='Total Medals',
            yaxis_title='',
            yaxis={'categoryorder': 'total ascending'},
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False
        )
        
        st.plotly_chart(fig_sport_bar, use_container_width=True)
    else:
        st.info("No medal data available for the selected filters")
else:
    st.info("Medal data not available")

st.markdown("---")

# ===== 3. VENUE MAP (SCATTER MAPBOX) =====
st.header("🗺️ Olympic Venues Map")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Interactive map of Paris 2024 Olympic venues</p>", unsafe_allow_html=True)

if not venues_df.empty:
    # Paris area coordinates (approximate for main venues)
    venue_coordinates = {
        'Stade de France': {'lat': 48.9244, 'lon': 2.3601},
        'Parc des Princes': {'lat': 48.8414, 'lon': 2.2530},
        'Eiffel Tower Stadium': {'lat': 48.8584, 'lon': 2.2945},
        'Grand Palais': {'lat': 48.8661, 'lon': 2.3122},
        'Invalides': {'lat': 48.8566, 'lon': 2.3122},
        'Champ de Mars Arena': {'lat': 48.8556, 'lon': 2.2986},
        'Trocadéro': {'lat': 48.8620, 'lon': 2.2876},
        'Bercy Arena': {'lat': 48.8394, 'lon': 2.3791},
        'La Concorde': {'lat': 48.8656, 'lon': 2.3212},
        'Aquatics Centre': {'lat': 48.9279, 'lon': 2.3601},
        'Porte de La Chapelle Arena': {'lat': 48.8978, 'lon': 2.3594},
        'South Paris Arena': {'lat': 48.8204, 'lon': 2.3660},
        'Roland-Garros': {'lat': 48.8467, 'lon': 2.2510},
        'Yves-du-Manoir Stadium': {'lat': 48.9309, 'lon': 2.2522},
        'Vaires-sur-Marne Nautical Stadium': {'lat': 48.8767, 'lon': 2.6380},
        'Château de Versailles': {'lat': 48.8049, 'lon': 2.1204},
        'Elancourt Hill': {'lat': 48.7725, 'lon': 1.9610},
        'Marina de Marseille': {'lat': 43.2780, 'lon': 5.3566},
        'Teahupo\'o': {'lat': -17.8333, 'lon': -149.2667}
    }
    
    # Create map data
    map_data = []
    for venue in venues_df['venue'].unique():
        # Try to match venue name
        coords = None
        for venue_name, coord in venue_coordinates.items():
            if venue_name.lower() in venue.lower():
                coords = coord
                break
        
        if coords:
            venue_info = venues_df[venues_df['venue'] == venue].iloc[0]
            sports = venue_info.get('sports', 'Unknown')
            
            # Parse sports list if it's a string
            if isinstance(sports, str) and sports.startswith('['):
                import ast
                try:
                    sports_list = ast.literal_eval(sports)
                    sports_display = ', '.join(sports_list)
                except:
                    sports_display = sports
            else:
                sports_display = sports
            
            map_data.append({
                'venue': venue,
                'lat': coords['lat'],
                'lon': coords['lon'],
                'sports': sports_display,
                'size': 15
            })
    
    if map_data:
        map_df = pd.DataFrame(map_data)
        
        # Create scatter mapbox
        fig_map = px.scatter_mapbox(
            map_df,
            lat='lat',
            lon='lon',
            hover_name='venue',
            hover_data={'sports': True, 'lat': False, 'lon': False, 'size': False},
            size='size',
            zoom=10,
            height=700,
            color_discrete_sequence=[COLORS['paris_green']]
        )
        
        fig_map.update_layout(
            mapbox_style='carto-darkmatter',
            mapbox=dict(
                center=dict(lat=48.8566, lon=2.3522),  # Paris center
                zoom=10
            ),
            title=dict(
                text="<b>Paris 2024 Olympic Venues</b>",
                font=dict(size=20, color=COLORS['paris_green'], family='Arial Black'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Venue list
        st.subheader("📋 Venue Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<h4 style='color: {COLORS['paris_green']};'>Main Venues</h4>", unsafe_allow_html=True)
            for idx, row in map_df.head(len(map_df)//2).iterrows():
                st.markdown(f"""
                <div style='background: {COLORS['card_bg']}; padding: 10px; border-radius: 8px; margin: 8px 0;
                            border-left: 3px solid {COLORS['paris_green']};'>
                    <strong style='color: {COLORS['text']};'>{row['venue']}</strong><br>
                    <span style='color: {COLORS['text_secondary']}; font-size: 0.85rem;'>{row['sports']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if len(map_df) > len(map_df)//2:
                st.markdown(f"<h4 style='color: {COLORS['paris_green']};'>Additional Venues</h4>", unsafe_allow_html=True)
                for idx, row in map_df.tail(len(map_df) - len(map_df)//2).iterrows():
                    st.markdown(f"""
                    <div style='background: {COLORS['card_bg']}; padding: 10px; border-radius: 8px; margin: 8px 0;
                                border-left: 3px solid {COLORS['secondary']};'>
                        <strong style='color: {COLORS['text']};'>{row['venue']}</strong><br>
                        <span style='color: {COLORS['text_secondary']}; font-size: 0.85rem;'>{row['sports']}</span>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Venue location data not available for mapping")
else:
    st.warning("Venue data not available")

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