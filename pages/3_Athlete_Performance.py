import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Athlete Performance", page_icon="👤", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        athletes = pd.read_csv('data/athletes.csv')
        coaches = pd.read_csv('data/coaches.csv')
        medals = pd.read_csv('data/medals.csv')
        teams = pd.read_csv('data/teams.csv')
        return athletes, coaches, medals, teams
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

athletes, coaches, medals, teams = load_data()

# Calculate age from birth_date
if athletes is not None and 'birth_date' in athletes.columns:
    athletes['birth_date'] = pd.to_datetime(athletes['birth_date'], errors='coerce')
    current_year = 2024
    athletes['age'] = current_year - athletes['birth_date'].dt.year

# Continent mapping
continent_mapping = {
    'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
    'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'THA': 'Asia',
    'GBR': 'Europe', 'FRA': 'Europe', 'GER': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe',
    'NED': 'Europe', 'SUI': 'Europe', 'POL': 'Europe', 'UKR': 'Europe',
    'AUS': 'Oceania', 'NZL': 'Oceania',
    'BRA': 'South America', 'ARG': 'South America', 'COL': 'South America',
    'RSA': 'Africa', 'EGY': 'Africa', 'KEN': 'Africa', 'ETH': 'Africa', 'NGR': 'Africa'
}

if athletes is not None:
    athletes['continent'] = athletes['country_code'].map(continent_mapping).fillna('Other')

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

if athletes is not None:
    all_countries = sorted(athletes['country'].dropna().unique())
    selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=[])
    
    all_continents = sorted(athletes['continent'].unique())
    selected_continents = st.sidebar.multiselect("🌍 Select Continents", options=all_continents, default=[])
    
    all_sports = sorted(athletes['disciplines'].dropna().unique()) if 'disciplines' in athletes.columns else []
    selected_sports = st.sidebar.multiselect("Select Sports", options=all_sports, default=[])

# Main content
st.title("👤 Athlete Performance - The Human Story")
st.markdown("Discover insights about Olympic athletes and their achievements")

if athletes is not None:
    # Apply filters
    filtered_athletes = athletes.copy()
    
    if selected_countries:
        filtered_athletes = filtered_athletes[filtered_athletes['country'].isin(selected_countries)]
    
    if selected_continents:
        filtered_athletes = filtered_athletes[filtered_athletes['continent'].isin(selected_continents)]
    
    if selected_sports:
        filtered_athletes = filtered_athletes[filtered_athletes['disciplines'].isin(selected_sports)]
    
    # 1. Athlete Detailed Profile Card
    st.header("🔍 Athlete Profile Search")
    
    athlete_names = sorted(filtered_athletes['name'].dropna().unique())
    
    col_search1, col_search2 = st.columns([3, 1])
    
    with col_search1:
        selected_athlete = st.selectbox(
            "Search and select an athlete",
            options=[''] + athlete_names,
            index=0
        )
    
    if selected_athlete:
        athlete_info = filtered_athletes[filtered_athletes['name'] == selected_athlete].iloc[0]
        
        st.subheader(f"📋 Profile: {selected_athlete}")
        
        # Create profile card
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            # Placeholder for athlete image
            st.markdown("### 📸")
            st.info("Photo unavailable")
        
        with col2:
            st.markdown("### 📊 Basic Information")
            st.write(f"**Full Name:** {athlete_info['name']}")
            st.write(f"**Country:** {athlete_info['country']} {athlete_info.get('country_code', '')}")
            
            if pd.notna(athlete_info.get('gender')):
                st.write(f"**Gender:** {athlete_info['gender']}")
            
            if pd.notna(athlete_info.get('birth_date')):
                st.write(f"**Birth Date:** {athlete_info['birth_date'].strftime('%Y-%m-%d') if pd.notna(athlete_info['birth_date']) else 'N/A'}")
            
            if pd.notna(athlete_info.get('age')):
                st.write(f"**Age:** {int(athlete_info['age'])} years")
        
        with col3:
            st.markdown("### 🏃 Athletic Details")
            
            if pd.notna(athlete_info.get('height')):
                st.write(f"**Height:** {athlete_info['height']} cm")
            
            if pd.notna(athlete_info.get('weight')):
                st.write(f"**Weight:** {athlete_info['weight']} kg")
            
            if pd.notna(athlete_info.get('disciplines')):
                st.write(f"**Sport(s):** {athlete_info['disciplines']}")
            
            if pd.notna(athlete_info.get('events')):
                st.write(f"**Event(s):** {athlete_info['events']}")
            
            # Try to find coach information
            if pd.notna(athlete_info.get('coach')):
                st.write(f"**Coach:** {athlete_info['coach']}")
            elif teams is not None:
                # Try to find from teams data
                athlete_code = athlete_info.get('code')
                if pd.notna(athlete_code):
                    team_info = teams[teams['athletes_codes'].str.contains(str(athlete_code), na=False)]
                    if not team_info.empty:
                        coach_info = team_info.iloc[0].get('coaches')
                        if pd.notna(coach_info):
                            st.write(f"**Coach:** {coach_info}")
    
    st.divider()
    
    # 2. Athlete Age Distribution
    st.header("📊 Athlete Age Distribution")
    
    tab1, tab2 = st.tabs(["By Sport", "By Gender"])
    
    with tab1:
        if 'age' in filtered_athletes.columns and 'disciplines' in filtered_athletes.columns:
            age_sport_data = filtered_athletes[filtered_athletes['age'].notna() & filtered_athletes['disciplines'].notna()]
            
            if not age_sport_data.empty:
                # Get top 10 sports by athlete count
                top_sports = age_sport_data['disciplines'].value_counts().head(10).index
                age_sport_data = age_sport_data[age_sport_data['disciplines'].isin(top_sports)]
                
                fig_age_sport = px.box(
                    age_sport_data,
                    x='disciplines',
                    y='age',
                    color='disciplines',
                    labels={'age': 'Age (years)', 'disciplines': 'Sport'}
                )
                fig_age_sport.update_layout(height=500, showlegend=False)
                fig_age_sport.update_xaxes(tickangle=45)
                st.plotly_chart(fig_age_sport, use_container_width=True)
            else:
                st.info("No age data available for the selected filters")
    
    with tab2:
        if 'age' in filtered_athletes.columns and 'gender' in filtered_athletes.columns:
            age_gender_data = filtered_athletes[filtered_athletes['age'].notna() & filtered_athletes['gender'].notna()]
            
            if not age_gender_data.empty:
                fig_age_gender = px.violin(
                    age_gender_data,
                    x='gender',
                    y='age',
                    color='gender',
                    box=True,
                    labels={'age': 'Age (years)', 'gender': 'Gender'}
                )
                fig_age_gender.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig_age_gender, use_container_width=True)
    
    st.divider()
    
    # 3. Gender Distribution by Continent and Country
    st.header("⚖️ Gender Distribution Analysis")
    
    view_option = st.radio("Select View", ["World", "By Continent", "By Country"], horizontal=True)
    
    if 'gender' in filtered_athletes.columns:
        gender_data = filtered_athletes[filtered_athletes['gender'].notna()]
        
        if view_option == "World":
            gender_counts = gender_data['gender'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_gender_pie = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title="Global Gender Distribution",
                    color_discrete_map={'Male': '#4169E1', 'Female': '#FF69B4'}
                )
                st.plotly_chart(fig_gender_pie, use_container_width=True)
            
            with col2:
                fig_gender_bar = px.bar(
                    x=gender_counts.index,
                    y=gender_counts.values,
                    labels={'x': 'Gender', 'y': 'Count'},
                    title="Athlete Count by Gender",
                    color=gender_counts.index,
                    color_discrete_map={'Male': '#4169E1', 'Female': '#FF69B4'}
                )
                st.plotly_chart(fig_gender_bar, use_container_width=True)
        
        elif view_option == "By Continent":
            continent_gender = gender_data.groupby(['continent', 'gender']).size().reset_index(name='count')
            
            fig_continent_gender = px.bar(
                continent_gender,
                x='continent',
                y='count',
                color='gender',
                barmode='group',
                labels={'count': 'Number of Athletes', 'continent': 'Continent'},
                color_discrete_map={'Male': '#4169E1', 'Female': '#FF69B4'}
            )
            fig_continent_gender.update_layout(height=500)
            st.plotly_chart(fig_continent_gender, use_container_width=True)
        
        else:  # By Country
            # Top 15 countries by athlete count
            top_countries = gender_data['country'].value_counts().head(15).index
            country_gender = gender_data[gender_data['country'].isin(top_countries)]
            country_gender = country_gender.groupby(['country', 'gender']).size().reset_index(name='count')
            
            fig_country_gender = px.bar(
                country_gender,
                x='country',
                y='count',
                color='gender',
                barmode='group',
                labels={'count': 'Number of Athletes', 'country': 'Country'},
                color_discrete_map={'Male': '#4169E1', 'Female': '#FF69B4'}
            )
            fig_country_gender.update_layout(height=500)
            fig_country_gender.update_xaxes(tickangle=45)
            st.plotly_chart(fig_country_gender, use_container_width=True)
    
    st.divider()
    
    # 4. Top Athletes by Medals
    st.header("🏅 Top Athletes by Medal Count")
    
    if medals is not None:
        # Count medals per athlete
        athlete_medals = medals.groupby(['name', 'country']).size().reset_index(name='medal_count')
        top_athletes = athlete_medals.nlargest(10, 'medal_count')
        
        fig_top_athletes = px.bar(
            top_athletes,
            x='medal_count',
            y='name',
            orientation='h',
            color='medal_count',
            color_continuous_scale='YlOrRd',
            labels={'medal_count': 'Total Medals', 'name': 'Athlete'},
            hover_data=['country']
        )
        fig_top_athletes.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_top_athletes, use_container_width=True)
        
        # Display detailed table
        st.subheader("📋 Detailed Medal Winners")
        st.dataframe(top_athletes, use_container_width=True)

else:
    st.error("Unable to load data. Please ensure CSV files are in the correct directory.")