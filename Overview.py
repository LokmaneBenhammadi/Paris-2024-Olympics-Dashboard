import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Paris 2024 Olympics Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0066cc;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    try:
        athletes = pd.read_csv('data/athletes.csv')
        medals_total = pd.read_csv('data/medals_total.csv')
        events = pd.read_csv('data/events.csv')
        nocs = pd.read_csv('data/nocs.csv')
        medals = pd.read_csv('data/medals.csv')
        return athletes, medals_total, events, nocs, medals
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None

# Load all data
athletes, medals_total, events, nocs, medals = load_data()

# Add continent mapping to NOCs
continent_mapping = {
    'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
    'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'THA': 'Asia',
    'GBR': 'Europe', 'FRA': 'Europe', 'GER': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe',
    'RUS': 'Europe', 'NED': 'Europe', 'SUI': 'Europe', 'POL': 'Europe', 'UKR': 'Europe',
    'AUS': 'Oceania', 'NZL': 'Oceania',
    'BRA': 'South America', 'ARG': 'South America', 'COL': 'South America',
    'RSA': 'Africa', 'EGY': 'Africa', 'KEN': 'Africa', 'ETH': 'Africa', 'NGR': 'Africa'
}

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

# Get unique values for filters
if medals_total is not None and events is not None:
    all_countries = sorted(medals_total['country'].unique())
    all_sports = sorted(events['sport'].unique()) if 'sport' in events.columns else []
    
    # Country filter
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=all_countries,
        default=[]
    )
    
    # Sport filter
    selected_sports = st.sidebar.multiselect(
        "Select Sports",
        options=all_sports,
        default=[]
    )
    
    # Continent filter (Creative addition)
    all_continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    selected_continents = st.sidebar.multiselect(
        "🌍 Select Continents (Creative Filter)",
        options=all_continents,
        default=[]
    )
    
    # Medal type filter
    st.sidebar.subheader("Medal Types")
    show_gold = st.sidebar.checkbox("🥇 Gold", value=True)
    show_silver = st.sidebar.checkbox("🥈 Silver", value=True)
    show_bronze = st.sidebar.checkbox("🥉 Bronze", value=True)

# Main title
st.markdown('<div class="main-title">🏅 Paris 2024 Olympic Games Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore comprehensive insights from the Paris 2024 Summer Olympics</div>', unsafe_allow_html=True)

if medals_total is not None:
    # Apply filters
    filtered_medals = medals_total.copy()
    
    if selected_countries:
        filtered_medals = filtered_medals[filtered_medals['country'].isin(selected_countries)]
    
    if selected_continents:
        filtered_medals['continent'] = filtered_medals['country_code'].map(continent_mapping)
        filtered_medals = filtered_medals[filtered_medals['continent'].isin(selected_continents)]
    
    # Apply medal type filters
    medal_cols = []
    if show_gold:
        medal_cols.append('Gold Medal')
    if show_silver:
        medal_cols.append('Silver Medal')
    if show_bronze:
        medal_cols.append('Bronze Medal')
    
    # KPI Metrics Section
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_athletes = len(athletes) if athletes is not None else 0
        st.metric(
            label="👥 Total Athletes",
            value=f"{total_athletes:,}"
        )
    
    with col2:
        total_countries = len(filtered_medals) if filtered_medals is not None else 0
        st.metric(
            label="🌍 Total Countries",
            value=f"{total_countries}"
        )
    
    with col3:
        total_sports = len(events['sport'].unique()) if events is not None and 'sport' in events.columns else 0
        st.metric(
            label="🏃 Total Sports",
            value=f"{total_sports}"
        )
    
    with col4:
        total_medals = filtered_medals[medal_cols].sum().sum() if medal_cols else 0
        st.metric(
            label="🏅 Total Medals",
            value=f"{int(total_medals):,}"
        )
    
    with col5:
        total_events = len(events) if events is not None else 0
        st.metric(
            label="🎯 Total Events",
            value=f"{total_events}"
        )
    
    st.divider()
    
    # Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🥧 Global Medal Distribution")
        
        if medal_cols:
            medal_distribution = {
                'Gold': filtered_medals['Gold Medal'].sum() if 'Gold Medal' in medal_cols else 0,
                'Silver': filtered_medals['Silver Medal'].sum() if 'Silver Medal' in medal_cols else 0,
                'Bronze': filtered_medals['Bronze Medal'].sum() if 'Bronze Medal' in medal_cols else 0
            }
            
            medal_df = pd.DataFrame(list(medal_distribution.items()), columns=['Medal Type', 'Count'])
            medal_df = medal_df[medal_df['Count'] > 0]
            
            fig_pie = px.pie(
                medal_df,
                values='Count',
                names='Medal Type',
                hole=0.4,
                color='Medal Type',
                color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Please select at least one medal type")
    
    with col_right:
        st.subheader("🏆 Top 10 Medal Standings")
        
        if medal_cols:
            filtered_medals['Total'] = filtered_medals[medal_cols].sum(axis=1)
            top_10 = filtered_medals.nlargest(10, 'Total')
            
            fig_bar = px.bar(
                top_10,
                y='country',
                x='Total',
                orientation='h',
                color='Total',
                color_continuous_scale='Blues',
                labels={'Total': 'Total Medals', 'country': 'Country'}
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Please select at least one medal type")
    
    st.divider()
    
    # Additional insights
    st.header("💡 Quick Insights")
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        if not filtered_medals.empty:
            top_country = filtered_medals.loc[filtered_medals['Total'].idxmax(), 'country']
            st.info(f"🥇 **Leading Nation:** {top_country}")
    
    with insight_col2:
        if medal_cols:
            most_common_medal = max(medal_distribution.items(), key=lambda x: x[1])[0]
            st.info(f"🏅 **Most Common Medal:** {most_common_medal}")
    
    with insight_col3:
        avg_medals = filtered_medals['Total'].mean()
        st.info(f"📊 **Avg Medals per Country:** {avg_medals:.1f}")

else:
    st.error("Unable to load data. Please ensure CSV files are in the correct directory.")
    st.info("Expected files: athletes.csv, medals_total.csv, events.csv, nocs.csv, medals.csv")