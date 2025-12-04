import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Global Analysis", page_icon="🗺️", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        medals_total = pd.read_csv('data/medals_total.csv')
        medals = pd.read_csv('data/medals.csv')
        nocs = pd.read_csv('data/nocs.csv')
        return medals_total, medals, nocs
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

medals_total, medals, nocs = load_data()

# Continent mapping
continent_mapping = {
    'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America', 'CUB': 'North America',
    'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'THA': 'Asia', 'IRN': 'Asia',
    'KAZ': 'Asia', 'UZB': 'Asia', 'TPE': 'Asia', 'HKG': 'Asia', 'INA': 'Asia', 'PHI': 'Asia',
    'GBR': 'Europe', 'FRA': 'Europe', 'GER': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe',
    'NED': 'Europe', 'SUI': 'Europe', 'POL': 'Europe', 'UKR': 'Europe', 'ROU': 'Europe',
    'CZE': 'Europe', 'HUN': 'Europe', 'BEL': 'Europe', 'AUT': 'Europe', 'SWE': 'Europe',
    'NOR': 'Europe', 'DEN': 'Europe', 'CRO': 'Europe', 'SRB': 'Europe', 'GRE': 'Europe',
    'AUS': 'Oceania', 'NZL': 'Oceania', 'FIJ': 'Oceania',
    'BRA': 'South America', 'ARG': 'South America', 'COL': 'South America', 'CHI': 'South America',
    'ECU': 'South America', 'VEN': 'South America',
    'RSA': 'Africa', 'EGY': 'Africa', 'KEN': 'Africa', 'ETH': 'Africa', 'NGR': 'Africa',
    'ALG': 'Africa', 'MAR': 'Africa', 'TUN': 'Africa', 'UGA': 'Africa', 'BOT': 'Africa'
}

# Add continent to medals_total
if medals_total is not None:
    medals_total['continent'] = medals_total['country_code'].map(continent_mapping).fillna('Other')

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

if medals_total is not None:
    all_countries = sorted(medals_total['country'].unique())
    selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=[])
    
    all_continents = sorted(medals_total['continent'].unique())
    selected_continents = st.sidebar.multiselect("🌍 Select Continents", options=all_continents, default=[])
    
    st.sidebar.subheader("Medal Types")
    show_gold = st.sidebar.checkbox("🥇 Gold", value=True)
    show_silver = st.sidebar.checkbox("🥈 Silver", value=True)
    show_bronze = st.sidebar.checkbox("🥉 Bronze", value=True)

# Main content
st.title("🗺️ Global Analysis - World View")
st.markdown("Analyze Olympic performance from geographical and hierarchical perspectives")

if medals_total is not None:
    # Apply filters
    filtered_data = medals_total.copy()
    
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]
    
    # Prepare medal columns
    medal_cols = []
    if show_gold:
        medal_cols.append('Gold Medal')
    if show_silver:
        medal_cols.append('Silver Medal')
    if show_bronze:
        medal_cols.append('Bronze Medal')
    
    # Calculate total for filtering
    if medal_cols:
        filtered_data['Total'] = filtered_data[medal_cols].sum(axis=1)
        filtered_data = filtered_data[filtered_data['Total'] > 0]
    
    # 1. World Medal Map (Choropleth)
    st.header("🌍 World Medal Map")
    
    if not filtered_data.empty:
        fig_map = px.choropleth(
            filtered_data,
            locations='country_code',
            color='Total',
            hover_name='country',
            hover_data={'country_code': False, 'Total': True, 'Gold Medal': True, 'Silver Medal': True, 'Bronze Medal': True},
            color_continuous_scale='YlOrRd',
            labels={'Total': 'Total Medals'}
        )
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
            height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No data available for the selected filters")
    
    st.divider()
    
    # 2. Medal Hierarchy by Continent (Sunburst & Treemap)
    st.header("🎯 Medal Hierarchy by Continent")
    
    tab1, tab2 = st.tabs(["Sunburst Chart", "Treemap"])
    
    with tab1:
        if medals is not None and not filtered_data.empty:
            # Prepare hierarchical data
            medals_with_continent = medals.copy()
            medals_with_continent['continent'] = medals_with_continent['country_code'].map(continent_mapping).fillna('Other')
            
            # Apply filters
            if selected_countries:
                medals_with_continent = medals_with_continent[medals_with_continent['country'].isin(selected_countries)]
            if selected_continents:
                medals_with_continent = medals_with_continent[medals_with_continent['continent'].isin(selected_continents)]
            
            # Filter by medal type
            medal_type_filter = []
            if show_gold:
                medal_type_filter.append('Gold Medal')
            if show_silver:
                medal_type_filter.append('Silver Medal')
            if show_bronze:
                medal_type_filter.append('Bronze Medal')
            
            if medal_type_filter:
                medals_with_continent = medals_with_continent[medals_with_continent['medal_type'].isin(medal_type_filter)]
            
            # Group data for hierarchy
            hierarchy_data = medals_with_continent.groupby(['continent', 'country', 'discipline']).size().reset_index(name='medal_count')
            
            if not hierarchy_data.empty:
                fig_sunburst = px.sunburst(
                    hierarchy_data,
                    path=['continent', 'country', 'discipline'],
                    values='medal_count',
                    color='medal_count',
                    color_continuous_scale='RdYlGn'
                )
                fig_sunburst.update_layout(height=600)
                st.plotly_chart(fig_sunburst, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
    
    with tab2:
        if medals is not None and not filtered_data.empty:
            if not hierarchy_data.empty:
                fig_treemap = px.treemap(
                    hierarchy_data,
                    path=['continent', 'country', 'discipline'],
                    values='medal_count',
                    color='medal_count',
                    color_continuous_scale='Viridis'
                )
                fig_treemap.update_layout(height=600)
                st.plotly_chart(fig_treemap, use_container_width=True)
    
    st.divider()
    
    # 3. Continent vs Medals Bar Chart
    st.header("📊 Continent vs Medals Comparison")
    
    if not filtered_data.empty:
        continent_medals = filtered_data.groupby('continent')[['Gold Medal', 'Silver Medal', 'Bronze Medal']].sum().reset_index()
        
        fig_continent = go.Figure()
        
        if show_gold:
            fig_continent.add_trace(go.Bar(name='Gold', x=continent_medals['continent'], 
                                          y=continent_medals['Gold Medal'], marker_color='#FFD700'))
        if show_silver:
            fig_continent.add_trace(go.Bar(name='Silver', x=continent_medals['continent'], 
                                          y=continent_medals['Silver Medal'], marker_color='#C0C0C0'))
        if show_bronze:
            fig_continent.add_trace(go.Bar(name='Bronze', x=continent_medals['continent'], 
                                          y=continent_medals['Bronze Medal'], marker_color='#CD7F32'))
        
        fig_continent.update_layout(barmode='group', xaxis_title='Continent', yaxis_title='Medal Count', height=500)
        st.plotly_chart(fig_continent, use_container_width=True)
    
    st.divider()
    
    # 4. Top 20 Countries vs Medals
    st.header("🏆 Top 20 Countries - Medal Comparison")
    
    if not filtered_data.empty and medal_cols:
        top_20 = filtered_data.nlargest(20, 'Total')
        
        fig_countries = go.Figure()
        
        if show_gold:
            fig_countries.add_trace(go.Bar(name='Gold', y=top_20['country'], 
                                          x=top_20['Gold Medal'], orientation='h', marker_color='#FFD700'))
        if show_silver:
            fig_countries.add_trace(go.Bar(name='Silver', y=top_20['country'], 
                                          x=top_20['Silver Medal'], orientation='h', marker_color='#C0C0C0'))
        if show_bronze:
            fig_countries.add_trace(go.Bar(name='Bronze', y=top_20['country'], 
                                          x=top_20['Bronze Medal'], orientation='h', marker_color='#CD7F32'))
        
        fig_countries.update_layout(
            barmode='group',
            xaxis_title='Medal Count',
            yaxis_title='Country',
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_countries, use_container_width=True)

else:
    st.error("Unable to load data. Please ensure CSV files are in the correct directory.")