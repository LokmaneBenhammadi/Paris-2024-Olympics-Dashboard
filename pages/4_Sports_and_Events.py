import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sports and Events", page_icon="🏟️", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        schedules = pd.read_csv('data/schedules.csv')
        medals = pd.read_csv('data/medals.csv')
        venues = pd.read_csv('data/venues.csv')
        events = pd.read_csv('data/events.csv')
        return schedules, medals, venues, events
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

schedules, medals, venues, events = load_data()

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

if events is not None:
    all_sports = sorted(events['sport'].dropna().unique()) if 'sport' in events.columns else []
    selected_sports = st.sidebar.multiselect("Select Sports", options=all_sports, default=[])
    
    st.sidebar.subheader("Medal Types")
    show_gold = st.sidebar.checkbox("🥇 Gold", value=True)
    show_silver = st.sidebar.checkbox("🥈 Silver", value=True)
    show_bronze = st.sidebar.checkbox("🥉 Bronze", value=True)

# Main content
st.title("🏟️ Sports and Events - The Competition Arena")
st.markdown("Explore event schedules, medal distributions, and Olympic venues")

# 1. Event Schedule (Timeline/Gantt Chart)
st.header("📅 Event Schedule Timeline")

if schedules is not None:
    # Convert dates
    schedules['start_date'] = pd.to_datetime(schedules['start_date'], errors='coerce')
    schedules['end_date'] = pd.to_datetime(schedules['end_date'], errors='coerce')
    
    # Filter by selected sports
    filtered_schedule = schedules.copy()
    if selected_sports:
        filtered_schedule = filtered_schedule[filtered_schedule['discipline'].isin(selected_sports)]
    
    # Sport selector for detailed view
    sport_for_timeline = st.selectbox(
        "Select a sport for detailed schedule",
        options=['All Sports'] + (all_sports if 'all_sports' in locals() else [])
    )
    
    if sport_for_timeline != 'All Sports':
        timeline_data = filtered_schedule[filtered_schedule['discipline'] == sport_for_timeline].copy()
    else:
        # Show top 10 sports by event count
        top_sports = filtered_schedule['discipline'].value_counts().head(10).index
        timeline_data = filtered_schedule[filtered_schedule['discipline'].isin(top_sports)].copy()
    
    if not timeline_data.empty:
        # Prepare data for Gantt chart
        timeline_data = timeline_data[timeline_data['start_date'].notna() & timeline_data['end_date'].notna()]
        
        if not timeline_data.empty:
            fig_timeline = px.timeline(
                timeline_data,
                x_start='start_date',
                x_end='end_date',
                y='event',
                color='discipline',
                hover_data=['venue', 'phase'],
                labels={'event': 'Event', 'discipline': 'Sport'}
            )
            fig_timeline.update_yaxes(categoryorder='total ascending')
            fig_timeline.update_layout(height=600)
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No complete schedule data available for the selected sport")
    else:
        st.info("No schedule data available for the selected filters")
else:
    st.warning("Schedule data not available")

st.divider()

# 2. Medal Count by Sport (Treemap)
st.header("🎯 Medal Distribution by Sport")

if medals is not None:
    # Filter medals by type
    filtered_medals = medals.copy()
    
    medal_types = []
    if show_gold:
        medal_types.append('Gold Medal')
    if show_silver:
        medal_types.append('Silver Medal')
    if show_bronze:
        medal_types.append('Bronze Medal')
    
    if medal_types:
        filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(medal_types)]
    
    # Filter by selected sports
    if selected_sports:
        filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_sports)]
    
    if not filtered_medals.empty:
        # Prepare data for treemap
        sport_medals = filtered_medals.groupby(['discipline', 'event']).size().reset_index(name='medal_count')
        
        fig_treemap = px.treemap(
            sport_medals,
            path=['discipline', 'event'],
            values='medal_count',
            color='medal_count',
            color_continuous_scale='Viridis',
            labels={'medal_count': 'Medal Count'}
        )
        fig_treemap.update_layout(height=600)
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Additional bar chart for sport comparison
        st.subheader("📊 Medal Count Comparison by Sport")
        
        sport_totals = filtered_medals.groupby('discipline').size().reset_index(name='total_medals')
        sport_totals = sport_totals.sort_values('total_medals', ascending=True).tail(20)
        
        fig_sport_bar = px.bar(
            sport_totals,
            x='total_medals',
            y='discipline',
            orientation='h',
            color='total_medals',
            color_continuous_scale='Blues',
            labels={'total_medals': 'Total Medals', 'discipline': 'Sport'}
        )
        fig_sport_bar.update_layout(height=600)
        st.plotly_chart(fig_sport_bar, use_container_width=True)
    else:
        st.info("No medal data available for the selected filters")

st.divider()

# 3. Venue Map
st.header("🗺️ Olympic Venues in Paris")

if venues is not None:
    st.subheader("📍 Venue Information")
    
    # Display venues in an organized way
    venue_display = venues[['venue', 'sports']].copy() if 'venue' in venues.columns and 'sports' in venues.columns else venues
    
    # Filter by selected sports if applicable
    if selected_sports and 'sports' in venue_display.columns:
        venue_display = venue_display[venue_display['sports'].apply(
            lambda x: any(sport in str(x) for sport in selected_sports) if pd.notna(x) else False
        )]
    
    if not venue_display.empty:
        st.dataframe(venue_display, use_container_width=True)
        
        # Paris coordinates for approximate venue locations
        paris_venues = {
            'Stade de France': {'lat': 48.9244, 'lon': 2.3601},
            'Parc des Princes': {'lat': 48.8414, 'lon': 2.2530},
            'Roland Garros': {'lat': 48.8467, 'lon': 2.2526},
            'Bercy Arena': {'lat': 48.8387, 'lon': 2.3794},
            'Grand Palais': {'lat': 48.8661, 'lon': 2.3124},
            'Eiffel Tower': {'lat': 48.8584, 'lon': 2.2945},
            'Invalides': {'lat': 48.8567, 'lon': 2.3125},
            'Champ de Mars': {'lat': 48.8556, 'lon': 2.2986},
            'Trocadero': {'lat': 48.8620, 'lon': 2.2877},
            'Versailles': {'lat': 48.8049, 'lon': 2.1204}
        }
        
        # Create map data
        map_data = []
        for venue_name, coords in paris_venues.items():
            # Check if venue exists in our data
            venue_info = venue_display[venue_display['venue'].str.contains(venue_name, case=False, na=False)]
            if not venue_info.empty:
                sports_list = venue_info.iloc[0]['sports'] if 'sports' in venue_info.columns else 'Various'
                map_data.append({
                    'venue': venue_name,
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'sports': sports_list
                })
        
        if map_data:
            map_df = pd.DataFrame(map_data)
            
            fig_map = px.scatter_mapbox(
                map_df,
                lat='lat',
                lon='lon',
                hover_name='venue',
                hover_data=['sports'],
                zoom=10,
                height=600,
                color_discrete_sequence=['#FF6B6B']
            )
            
            fig_map.update_layout(
                mapbox_style='open-street-map',
                mapbox=dict(
                    center=dict(lat=48.8566, lon=2.3522),  # Paris center
                    zoom=10
                )
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Venue location data not available for mapping")
    else:
        st.info("No venue data available for the selected filters")
else:
    st.warning("Venue data not available")

st.divider()

# Additional Statistics
st.header("📊 Event Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if events is not None:
        total_events = len(events)
        if selected_sports:
            total_events = len(events[events['sport'].isin(selected_sports)])
        st.metric("Total Events", total_events)

with col2:
    if medals is not None:
        total_medals = len(filtered_medals) if 'filtered_medals' in locals() else len(medals)
        st.metric("Total Medals Awarded", total_medals)

with col3:
    if venues is not None:
        total_venues = len(venues)
        st.metric("Total Venues", total_venues)