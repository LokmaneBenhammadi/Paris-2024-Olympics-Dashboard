import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced Analytics", page_icon="⭐", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        athletes = pd.read_csv('data/athletes.csv')
        medals = pd.read_csv('data/medals.csv')
        medals_total = pd.read_csv('data/medals_total.csv')
        events = pd.read_csv('data/events.csv')
        return athletes, medals, medals_total, events
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

athletes, medals, medals_total, events = load_data()

# Continent mapping
continent_mapping = {
    'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America', 'CUB': 'North America',
    'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia', 'THA': 'Asia', 'IRN': 'Asia',
    'GBR': 'Europe', 'FRA': 'Europe', 'GER': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe',
    'NED': 'Europe', 'SUI': 'Europe', 'POL': 'Europe', 'UKR': 'Europe', 'ROU': 'Europe',
    'AUS': 'Oceania', 'NZL': 'Oceania',
    'BRA': 'South America', 'ARG': 'South America', 'COL': 'South America',
    'RSA': 'Africa', 'EGY': 'Africa', 'KEN': 'Africa', 'ETH': 'Africa', 'NGR': 'Africa'
}

# Main title
st.title("⭐ Advanced Analytics - Creative Insights")
st.markdown("Explore advanced features and creative analysis beyond the basics")

# SIDEBAR
st.sidebar.header("🎯 Advanced Filters")

if medals_total is not None:
    medals_total['continent'] = medals_total['country_code'].map(continent_mapping).fillna('Other')
    
    all_continents = sorted(medals_total['continent'].unique())
    selected_continent = st.sidebar.selectbox("Select Continent", options=['All'] + all_continents)
    
    st.sidebar.subheader("Analysis Options")
    show_gender_breakdown = st.sidebar.checkbox("Show Gender Breakdown", value=True)
    show_efficiency = st.sidebar.checkbox("Show Efficiency Metrics", value=True)

st.divider()

# 1. Head-to-Head Country Comparison
st.header("🤝 Head-to-Head Country Comparison")

if medals_total is not None:
    col1, col2 = st.columns(2)
    
    country_list = sorted(medals_total['country'].unique())
    
    with col1:
        country_1 = st.selectbox("Select First Country", options=country_list, index=0)
    
    with col2:
        country_2 = st.selectbox("Select Second Country", options=country_list, 
                                 index=min(1, len(country_list)-1))
    
    if country_1 and country_2:
        # Get data for both countries
        c1_data = medals_total[medals_total['country'] == country_1].iloc[0]
        c2_data = medals_total[medals_total['country'] == country_2].iloc[0]
        
        # Create comparison
        comparison_df = pd.DataFrame({
            'Metric': ['Gold Medals', 'Silver Medals', 'Bronze Medals', 'Total Medals'],
            country_1: [c1_data['Gold Medal'], c1_data['Silver Medal'], 
                       c1_data['Bronze Medal'], c1_data['Total']],
            country_2: [c2_data['Gold Medal'], c2_data['Silver Medal'], 
                       c2_data['Bronze Medal'], c2_data['Total']]
        })
        
        fig_comparison = go.Figure()
        
        fig_comparison.add_trace(go.Bar(
            name=country_1,
            x=comparison_df['Metric'],
            y=comparison_df[country_1],
            marker_color='#4169E1'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name=country_2,
            x=comparison_df['Metric'],
            y=comparison_df[country_2],
            marker_color='#FF6347'
        ))
        
        fig_comparison.update_layout(
            barmode='group',
            title=f"{country_1} vs {country_2} - Medal Comparison",
            height=400
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Show detailed stats
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric(f"{country_1} Total", int(c1_data['Total']))
        
        with col_stat2:
            st.metric(f"{country_2} Total", int(c2_data['Total']))
        
        with col_stat3:
            diff = int(c1_data['Total'] - c2_data['Total'])
            st.metric("Difference", diff, delta=f"{abs(diff)} medals")

st.divider()

# 2. Top Performing Countries by Continent and Gender
st.header("🌍 Continental Performance Analysis")

if medals is not None and athletes is not None:
    medals['continent'] = medals['country_code'].map(continent_mapping).fillna('Other')
    
    # Filter by continent
    if selected_continent != 'All':
        continent_medals = medals[medals['continent'] == selected_continent]
    else:
        continent_medals = medals.copy()
    
    # Ranking type selector
    ranking_type = st.radio(
        "Ranking Criteria",
        ["Total Medals", "Gold Medals Only", "By Gender Performance"],
        horizontal=True
    )
    
    if ranking_type == "Total Medals":
        country_ranks = continent_medals.groupby('country').size().reset_index(name='medal_count')
        country_ranks = country_ranks.sort_values('medal_count', ascending=False).head(15)
        
        fig_rank = px.bar(
            country_ranks,
            x='medal_count',
            y='country',
            orientation='h',
            color='medal_count',
            color_continuous_scale='Viridis',
            labels={'medal_count': 'Total Medals', 'country': 'Country'}
        )
        fig_rank.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        st.plotly_chart(fig_rank, use_container_width=True)
    
    elif ranking_type == "Gold Medals Only":
        gold_medals = continent_medals[continent_medals['medal_type'] == 'Gold Medal']
        gold_ranks = gold_medals.groupby('country').size().reset_index(name='gold_count')
        gold_ranks = gold_ranks.sort_values('gold_count', ascending=False).head(15)
        
        fig_gold = px.bar(
            gold_ranks,
            x='gold_count',
            y='country',
            orientation='h',
            color='gold_count',
            color_continuous_scale='YlOrRd',
            labels={'gold_count': 'Gold Medals', 'country': 'Country'}
        )
        fig_gold.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        st.plotly_chart(fig_gold, use_container_width=True)
    
    else:  # By Gender Performance
        # Merge with athletes to get gender
        medals_gender = continent_medals.merge(
            athletes[['code', 'gender']], 
            left_on='code_athlete', 
            right_on='code', 
            how='left'
        )
        
        gender_performance = medals_gender.groupby(['country', 'gender']).size().reset_index(name='medal_count')
        gender_performance = gender_performance.pivot(index='country', columns='gender', values='medal_count').fillna(0)
        gender_performance['total'] = gender_performance.sum(axis=1)
        gender_performance = gender_performance.sort_values('total', ascending=False).head(15)
        
        fig_gender_perf = go.Figure()
        
        if 'Male' in gender_performance.columns:
            fig_gender_perf.add_trace(go.Bar(
                name='Male',
                y=gender_performance.index,
                x=gender_performance['Male'],
                orientation='h',
                marker_color='#4169E1'
            ))
        
        if 'Female' in gender_performance.columns:
            fig_gender_perf.add_trace(go.Bar(
                name='Female',
                y=gender_performance.index,
                x=gender_performance['Female'],
                orientation='h',
                marker_color='#FF69B4'
            ))
        
        fig_gender_perf.update_layout(
            barmode='stack',
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Medal Count',
            yaxis_title='Country'
        )
        st.plotly_chart(fig_gender_perf, use_container_width=True)

st.divider()

# 3. Athletes by Sport Discipline, Country, and Gender
st.header("🏃 Athlete Analysis by Discipline")

if athletes is not None and 'disciplines' in athletes.columns:
    # Get unique disciplines
    all_disciplines = sorted(athletes['disciplines'].dropna().unique())
    
    selected_discipline = st.selectbox("Select Sport Discipline", options=all_disciplines)
    
    if selected_discipline:
        discipline_athletes = athletes[athletes['disciplines'] == selected_discipline]
        
        # Country selector
        discipline_countries = sorted(discipline_athletes['country'].unique())
        selected_country = st.selectbox("Select Country", options=['All'] + discipline_countries)
        
        if selected_country != 'All':
            discipline_athletes = discipline_athletes[discipline_athletes['country'] == selected_country]
        
        # Gender breakdown
        if not discipline_athletes.empty:
            col_gender1, col_gender2 = st.columns(2)
            
            with col_gender1:
                gender_counts = discipline_athletes['gender'].value_counts()
                
                fig_gender = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title=f"Gender Distribution - {selected_discipline}",
                    color_discrete_map={'Male': '#4169E1', 'Female': '#FF69B4'}
                )
                st.plotly_chart(fig_gender, use_container_width=True)
            
            with col_gender2:
                st.metric("Total Athletes", len(discipline_athletes))
                st.metric("Countries Represented", discipline_athletes['country'].nunique())
                
                if 'age' in discipline_athletes.columns:
                    avg_age = discipline_athletes['age'].mean()
                    st.metric("Average Age", f"{avg_age:.1f} years")
            
            # Display athlete table
            st.subheader("📋 Athlete Details")
            display_cols = ['name', 'country', 'gender', 'age', 'height', 'weight']
            available_cols = [col for col in display_cols if col in discipline_athletes.columns]
            st.dataframe(discipline_athletes[available_cols], use_container_width=True)

st.divider()

# 4. Medal Efficiency Analysis (Creative Feature)
st.header("📈 Medal Efficiency Analysis")

if show_efficiency and athletes is not None and medals_total is not None:
    st.markdown("**Efficiency = Medals per 100 Athletes**")
    
    # Calculate athletes per country
    athletes_per_country = athletes.groupby('country').size().reset_index(name='athlete_count')
    
    # Merge with medals
    efficiency_data = medals_total.merge(athletes_per_country, on='country', how='inner')
    efficiency_data['efficiency'] = (efficiency_data['Total'] / efficiency_data['athlete_count']) * 100
    efficiency_data = efficiency_data.sort_values('efficiency', ascending=False).head(20)
    
    fig_efficiency = px.scatter(
        efficiency_data,
        x='athlete_count',
        y='Total',
        size='efficiency',
        color='efficiency',
        hover_name='country',
        labels={'athlete_count': 'Number of Athletes', 'Total': 'Total Medals'},
        color_continuous_scale='Turbo',
        size_max=60
    )
    
    fig_efficiency.update_layout(height=500)
    st.plotly_chart(fig_efficiency, use_container_width=True)
    
    st.info("💡 Larger bubbles indicate higher medal efficiency (more medals per athlete)")