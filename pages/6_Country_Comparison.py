"""
Page 6: Country Comparison - Head-to-Head Analysis
Compare two countries side by side across all Olympic metrics
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from config.config import COLORS, PAGE_CONFIG
from utils.data_loader import load_athletes, load_medallists, load_medals_total, load_medals
from utils.continent_mapper import add_continent_column

# Page configuration
st.set_page_config(
    page_title="Country Comparison - Paris 2024",
    page_icon="⚔️",
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
    ⚔️ Country Comparison - Head-to-Head Analysis
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    Compare Two Countries Across All Olympic Metrics
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_comparison_data():
    """Load and prepare data for country comparison."""
    athletes_df = load_athletes()
    medallists_df = load_medallists()
    medals_df = load_medals()  # Use medals.csv for accurate medal counts (one row per medal event)
    medals_total_df = load_medals_total()
    
    # Calculate age if needed
    if not athletes_df.empty and 'birth_date' in athletes_df.columns:
        athletes_df['birth_date'] = pd.to_datetime(athletes_df['birth_date'], errors='coerce')
        olympics_date = pd.Timestamp('2024-07-26')
        athletes_df['age'] = (olympics_date - athletes_df['birth_date']).dt.days // 365
    
    # Add continent info
    if not athletes_df.empty and 'country_code' in athletes_df.columns:
        athletes_df = add_continent_column(athletes_df, 'country_code')
    
    if not medallists_df.empty and 'country_code' in medallists_df.columns:
        medallists_df = add_continent_column(medallists_df, 'country_code')
    
    if not medals_df.empty and 'country_code' in medals_df.columns:
        medals_df = add_continent_column(medals_df, 'country_code')
    
    # Parse medal dates
    if not medals_df.empty and 'medal_date' in medals_df.columns:
        medals_df['medal_date'] = pd.to_datetime(medals_df['medal_date'], errors='coerce')
    
    return athletes_df, medallists_df, medals_df, medals_total_df

athletes_df, medallists_df, medals_df, medals_total_df = load_comparison_data()

st.markdown(f"""
<div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['paris_green']}; margin-bottom: 30px;'>
    <p style='color: {COLORS['text']}; font-size: 1.1rem; margin: 0;'>
        <strong>⚔️ Head-to-Head Comparison:</strong> Select two countries below to compare their Olympic performance.
    </p>
</div>
""", unsafe_allow_html=True)

# Use full datasets (no sidebar filters)
filtered_athletes = athletes_df
filtered_medallists = medallists_df

# ===== COUNTRY SELECTOR =====
st.header("🎯 Select Countries to Compare")

# Use base data
if not medals_df.empty:
    # Get list of countries from medals_df (more accurate for countries that won medals)
    countries = sorted(medals_df['country'].dropna().unique())
    
    col_select1, col_select2 = st.columns(2)
    
    with col_select1:
        country1 = st.selectbox(
            "🥇 Country 1:",
            options=countries,
            index=0 if len(countries) > 0 else None,
            key='country1_selector'
        )
    
    with col_select2:
        country2 = st.selectbox(
            "🥈 Country 2:",
            options=countries,
            index=1 if len(countries) > 1 else 0,
            key='country2_selector'
        )
    
    if country1 and country2:
        if country1 == country2:
            st.warning("⚠️ Please select two different countries to compare.")
        else:
            # Filter data for both countries
            # Use medals_df for accurate medal counts (one row per medal event, not per athlete)
            country1_medals = medals_df[medals_df['country'] == country1]
            country2_medals = medals_df[medals_df['country'] == country2]
            
            # Keep medallists_df for individual athlete analysis (gender, age)
            country1_medallists = medallists_df[medallists_df['country'] == country1]
            country2_medallists = medallists_df[medallists_df['country'] == country2]
            
            country1_athletes = athletes_df[athletes_df['country'] == country1]
            country2_athletes = athletes_df[athletes_df['country'] == country2]
            
            st.markdown("---")
            
            # ===== 1. OVERVIEW COMPARISON =====
            st.header("📊 Overview Comparison")
            
            col_over1, col_over2 = st.columns(2)
            
            with col_over1:
                st.markdown(f"<h3 style='text-align: center; color: {COLORS['paris_green']};'>{country1}</h3>", unsafe_allow_html=True)
                
                # Use medals_df for accurate counts (one medal per event, not per athlete)
                total_medals_c1 = len(country1_medals)
                gold_c1 = len(country1_medals[country1_medals['medal_type'].str.contains('Gold', case=False, na=False)])
                silver_c1 = len(country1_medals[country1_medals['medal_type'].str.contains('Silver', case=False, na=False)])
                bronze_c1 = len(country1_medals[country1_medals['medal_type'].str.contains('Bronze', case=False, na=False)])
                athletes_c1 = len(country1_athletes)
                
                st.markdown(f"""
                <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; text-align: center;'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>Total Medals</p>
                    <p style='color: {COLORS['paris_green']}; margin: 10px 0; font-size: 3rem; font-weight: bold;'>{total_medals_c1}</p>
                    <div style='display: flex; justify-content: space-around; margin-top: 20px;'>
                        <div>
                            <p style='color: {COLORS['gold']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{gold_c1}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥇 Gold</p>
                        </div>
                        <div>
                            <p style='color: {COLORS['silver']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{silver_c1}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥈 Silver</p>
                        </div>
                        <div>
                            <p style='color: {COLORS['bronze']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{bronze_c1}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥉 Bronze</p>
                        </div>
                    </div>
                    <hr style='border: 1px solid {COLORS['background']}; margin: 20px 0;'>
                    <p style='color: {COLORS['text']}; margin: 0; font-size: 1.2rem;'>👥 Athletes: <strong>{athletes_c1}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_over2:
                st.markdown(f"<h3 style='text-align: center; color: {COLORS['secondary']};'>{country2}</h3>", unsafe_allow_html=True)
                
                # Use medals_df for accurate counts (one medal per event, not per athlete)
                total_medals_c2 = len(country2_medals)
                gold_c2 = len(country2_medals[country2_medals['medal_type'].str.contains('Gold', case=False, na=False)])
                silver_c2 = len(country2_medals[country2_medals['medal_type'].str.contains('Silver', case=False, na=False)])
                bronze_c2 = len(country2_medals[country2_medals['medal_type'].str.contains('Bronze', case=False, na=False)])
                athletes_c2 = len(country2_athletes)
                
                st.markdown(f"""
                <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; text-align: center;'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>Total Medals</p>
                    <p style='color: {COLORS['secondary']}; margin: 10px 0; font-size: 3rem; font-weight: bold;'>{total_medals_c2}</p>
                    <div style='display: flex; justify-content: space-around; margin-top: 20px;'>
                        <div>
                            <p style='color: {COLORS['gold']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{gold_c2}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥇 Gold</p>
                        </div>
                        <div>
                            <p style='color: {COLORS['silver']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{silver_c2}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥈 Silver</p>
                        </div>
                        <div>
                            <p style='color: {COLORS['bronze']}; margin: 0; font-size: 1.5rem; font-weight: bold;'>{bronze_c2}</p>
                            <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥉 Bronze</p>
                        </div>
                    </div>
                    <hr style='border: 1px solid {COLORS['background']}; margin: 20px 0;'>
                    <p style='color: {COLORS['text']}; margin: 0; font-size: 1.2rem;'>👥 Athletes: <strong>{athletes_c2}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ===== 2. MEDAL TYPE BREAKDOWN (STACKED BAR) =====
            st.header("🏅 Medal Type Breakdown")
            
            medal_comparison = pd.DataFrame({
                'Country': [country1, country2],
                'Gold': [gold_c1, gold_c2],
                'Silver': [silver_c1, silver_c2],
                'Bronze': [bronze_c1, bronze_c2]
            })
            
            fig_stacked = go.Figure()
            
            fig_stacked.add_trace(go.Bar(
                name='🥇 Gold',
                x=medal_comparison['Country'],
                y=medal_comparison['Gold'],
                marker=dict(color=COLORS['gold']),
                text=medal_comparison['Gold'],
                textposition='inside',
                textfont=dict(size=14, color='black', family='Arial Black')
            ))
            
            fig_stacked.add_trace(go.Bar(
                name='🥈 Silver',
                x=medal_comparison['Country'],
                y=medal_comparison['Silver'],
                marker=dict(color=COLORS['silver']),
                text=medal_comparison['Silver'],
                textposition='inside',
                textfont=dict(size=14, color='black', family='Arial Black')
            ))
            
            fig_stacked.add_trace(go.Bar(
                name='🥉 Bronze',
                x=medal_comparison['Country'],
                y=medal_comparison['Bronze'],
                marker=dict(color=COLORS['bronze']),
                text=medal_comparison['Bronze'],
                textposition='inside',
                textfont=dict(size=14, color='white', family='Arial Black')
            ))
            
            fig_stacked.update_layout(
                barmode='stack',
                title="Medal Type Distribution",
                plot_bgcolor=COLORS['background'],
                paper_bgcolor=COLORS['background'],
                font=dict(color=COLORS['text'], family='Arial Black'),
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig_stacked, use_container_width=True)
            
            st.markdown("---")
            
            # ===== 3. PERFORMANCE BY SPORT (RADAR CHART) =====
            st.header("🎯 Performance Across Sports")
            
            # Get medals by sport for both countries (use medals_df for accurate counts)
            c1_sports = country1_medals.groupby('discipline').size().reset_index(name='medals')
            c2_sports = country2_medals.groupby('discipline').size().reset_index(name='medals')
            
            # Find common sports
            common_sports = set(c1_sports['discipline']).intersection(set(c2_sports['discipline']))
            
            if len(common_sports) >= 3:
                # Get top sports by combined medals
                all_sports = pd.concat([
                    c1_sports[c1_sports['discipline'].isin(common_sports)],
                    c2_sports[c2_sports['discipline'].isin(common_sports)]
                ]).groupby('discipline')['medals'].sum().sort_values(ascending=False).head(10)
                
                top_sports = all_sports.index.tolist()
                
                # Create radar chart data
                c1_radar = []
                c2_radar = []
                
                for sport in top_sports:
                    c1_val = c1_sports[c1_sports['discipline'] == sport]['medals'].values
                    c2_val = c2_sports[c2_sports['discipline'] == sport]['medals'].values
                    c1_radar.append(c1_val[0] if len(c1_val) > 0 else 0)
                    c2_radar.append(c2_val[0] if len(c2_val) > 0 else 0)
                
                fig_radar = go.Figure()
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=c1_radar,
                    theta=top_sports,
                    fill='toself',
                    name=country1,
                    marker=dict(color=COLORS['paris_green']),
                    line=dict(color=COLORS['paris_green'], width=2)
                ))
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=c2_radar,
                    theta=top_sports,
                    fill='toself',
                    name=country2,
                    marker=dict(color=COLORS['secondary']),
                    line=dict(color=COLORS['secondary'], width=2)
                ))
                
                fig_radar.update_layout(
                    polar=dict(
                        bgcolor=COLORS['card_bg'],
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(max(c1_radar), max(c2_radar)) + 2],
                            gridcolor='rgba(255,255,255,0.2)'
                        )
                    ),
                    title="Medal Count by Sport (Top 10 Common Sports)",
                    plot_bgcolor=COLORS['background'],
                    paper_bgcolor=COLORS['background'],
                    font=dict(color=COLORS['text']),
                    height=500,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Not enough common sports between countries for radar comparison.")
            
            st.markdown("---")
            
            # ===== 4. MEDAL ACCUMULATION OVER TIME =====
            st.header("📈 Medal Accumulation Timeline")
            
            if 'medal_date' in country1_medals.columns and 'medal_date' in country2_medals.columns:
                # Calculate cumulative medals (use medals_df for accurate timeline)
                c1_timeline = country1_medals.groupby('medal_date').size().reset_index(name='daily_medals')
                c1_timeline = c1_timeline.sort_values('medal_date')
                c1_timeline['cumulative'] = c1_timeline['daily_medals'].cumsum()
                
                c2_timeline = country2_medals.groupby('medal_date').size().reset_index(name='daily_medals')
                c2_timeline = c2_timeline.sort_values('medal_date')
                c2_timeline['cumulative'] = c2_timeline['daily_medals'].cumsum()
                
                fig_timeline = go.Figure()
                
                fig_timeline.add_trace(go.Scatter(
                    x=c1_timeline['medal_date'],
                    y=c1_timeline['cumulative'],
                    mode='lines+markers',
                    name=country1,
                    line=dict(color=COLORS['paris_green'], width=3),
                    marker=dict(size=8)
                ))
                
                fig_timeline.add_trace(go.Scatter(
                    x=c2_timeline['medal_date'],
                    y=c2_timeline['cumulative'],
                    mode='lines+markers',
                    name=country2,
                    line=dict(color=COLORS['secondary'], width=3),
                    marker=dict(size=8)
                ))
                
                fig_timeline.update_layout(
                    title="Cumulative Medal Count Over Time",
                    plot_bgcolor=COLORS['background'],
                    paper_bgcolor=COLORS['background'],
                    font=dict(color=COLORS['text'], family='Arial Black'),
                    height=400,
                    xaxis_title='Date',
                    yaxis_title='Cumulative Medals',
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                )
                
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.info("Medal date information not available for timeline comparison.")
            
            st.markdown("---")
            
            # ===== 5. GENDER DISTRIBUTION COMPARISON =====
            st.header("⚥ Gender Distribution Comparison")
            
            col_gender1, col_gender2 = st.columns(2)
            
            with col_gender1:
                if 'gender' in country1_athletes.columns:
                    gender_c1 = country1_athletes['gender'].value_counts()
                    
                    fig_gender_c1 = px.pie(
                        values=gender_c1.values,
                        names=gender_c1.index,
                        title=f"{country1} - Gender Distribution",
                        color_discrete_map={
                            'Male': COLORS['secondary'],
                            'Female': COLORS['paris_green']
                        },
                        hole=0.4
                    )
                    
                    fig_gender_c1.update_layout(
                        plot_bgcolor=COLORS['background'],
                        paper_bgcolor=COLORS['background'],
                        font=dict(color=COLORS['text']),
                        height=350
                    )
                    
                    st.plotly_chart(fig_gender_c1, use_container_width=True)
            
            with col_gender2:
                if 'gender' in country2_athletes.columns:
                    gender_c2 = country2_athletes['gender'].value_counts()
                    
                    fig_gender_c2 = px.pie(
                        values=gender_c2.values,
                        names=gender_c2.index,
                        title=f"{country2} - Gender Distribution",
                        color_discrete_map={
                            'Male': COLORS['secondary'],
                            'Female': COLORS['paris_green']
                        },
                        hole=0.4
                    )
                    
                    fig_gender_c2.update_layout(
                        plot_bgcolor=COLORS['background'],
                        paper_bgcolor=COLORS['background'],
                        font=dict(color=COLORS['text']),
                        height=350
                    )
                    
                    st.plotly_chart(fig_gender_c2, use_container_width=True)
            
            st.markdown("---")
            
            # ===== 6. AGE DISTRIBUTION COMPARISON (BOX PLOTS) =====
            st.header("📊 Age Distribution Comparison")
            
            if 'age' in country1_athletes.columns and 'age' in country2_athletes.columns:
                # Prepare data
                c1_age_data = country1_athletes[country1_athletes['age'].notna()][['age']].copy()
                c1_age_data['country'] = country1
                
                c2_age_data = country2_athletes[country2_athletes['age'].notna()][['age']].copy()
                c2_age_data['country'] = country2
                
                combined_age = pd.concat([c1_age_data, c2_age_data])
                
                if not combined_age.empty:
                    fig_age_box = go.Figure()
                    
                    fig_age_box.add_trace(go.Box(
                        y=c1_age_data['age'],
                        name=country1,
                        marker=dict(color=COLORS['paris_green']),
                        boxmean='sd'
                    ))
                    
                    fig_age_box.add_trace(go.Box(
                        y=c2_age_data['age'],
                        name=country2,
                        marker=dict(color=COLORS['secondary']),
                        boxmean='sd'
                    ))
                    
                    fig_age_box.update_layout(
                        title="Athlete Age Distribution (Box Plot with Mean & SD)",
                        plot_bgcolor=COLORS['background'],
                        paper_bgcolor=COLORS['background'],
                        font=dict(color=COLORS['text'], family='Arial Black'),
                        height=400,
                        yaxis_title='Age',
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    
                    st.plotly_chart(fig_age_box, use_container_width=True)
                    
                    # Age statistics
                    col_age1, col_age2 = st.columns(2)
                    
                    with col_age1:
                        avg_age_c1 = c1_age_data['age'].mean()
                        median_age_c1 = c1_age_data['age'].median()
                        min_age_c1 = c1_age_data['age'].min()
                        max_age_c1 = c1_age_data['age'].max()
                        
                        st.markdown(f"""
                        <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;'>
                            <h4 style='color: {COLORS['paris_green']}; margin: 0 0 15px 0;'>{country1} Age Stats</h4>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Average: <strong>{avg_age_c1:.1f}</strong> years</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Median: <strong>{median_age_c1:.1f}</strong> years</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Range: <strong>{min_age_c1:.0f} - {max_age_c1:.0f}</strong> years</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_age2:
                        avg_age_c2 = c2_age_data['age'].mean()
                        median_age_c2 = c2_age_data['age'].median()
                        min_age_c2 = c2_age_data['age'].min()
                        max_age_c2 = c2_age_data['age'].max()
                        
                        st.markdown(f"""
                        <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;'>
                            <h4 style='color: {COLORS['secondary']}; margin: 0 0 15px 0;'>{country2} Age Stats</h4>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Average: <strong>{avg_age_c2:.1f}</strong> years</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Median: <strong>{median_age_c2:.1f}</strong> years</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0;'>Range: <strong>{min_age_c2:.0f} - {max_age_c2:.0f}</strong> years</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Age data not available for comparison.")
            
            st.markdown("---")
            
            # ===== 7. "WHAT IF?" SCENARIOS =====
            st.header("🤔 What If? Scenarios")
            
            st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Explore hypothetical rankings with modified criteria</p>", unsafe_allow_html=True)
            
            scenario_type = st.radio(
                "Select Scenario:",
                ["Exclude Sports", "Gold Medals Only", "Gender-Specific"],
                horizontal=True
            )
            
            if scenario_type == "Exclude Sports":
                # Get all sports
                all_sports = sorted(medals_df['discipline'].dropna().unique())
                
                excluded_sports = st.multiselect(
                    "🚫 Exclude these sports from rankings:",
                    options=all_sports,
                    default=[],
                    help="Select sports to exclude and recalculate rankings"
                )
                
                if excluded_sports:
                    # Recalculate medals without excluded sports (use medals_df for accurate counts)
                    scenario_data = medals_df[~medals_df['discipline'].isin(excluded_sports)]
                    
                    c1_scenario = scenario_data[scenario_data['country'] == country1]
                    c2_scenario = scenario_data[scenario_data['country'] == country2]
                    
                    c1_new_total = len(c1_scenario)
                    c2_new_total = len(c2_scenario)
                    
                    c1_new_gold = len(c1_scenario[c1_scenario['medal_type'].str.contains('Gold', case=False, na=False)])
                    c2_new_gold = len(c2_scenario[c2_scenario['medal_type'].str.contains('Gold', case=False, na=False)])
                    
                    col_scen1, col_scen2 = st.columns(2)
                    
                    with col_scen1:
                        change_c1 = c1_new_total - total_medals_c1
                        change_pct_c1 = (change_c1 / total_medals_c1 * 100) if total_medals_c1 > 0 else 0
                        
                        st.markdown(f"""
                        <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['paris_green']};'>
                            <h4 style='color: {COLORS['paris_green']}; margin: 0;'>{country1}</h4>
                            <p style='color: {COLORS['text']}; margin: 10px 0 5px 0; font-size: 1.1rem;'>Original: <strong>{total_medals_c1}</strong> medals</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0; font-size: 1.1rem;'>New: <strong>{c1_new_total}</strong> medals</p>
                            <p style='color: {"#00A651" if change_c1 >= 0 else "#EE334E"}; margin: 10px 0 0 0; font-size: 1rem;'>
                                Change: <strong>{change_c1:+d}</strong> ({change_pct_c1:+.1f}%)
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_scen2:
                        change_c2 = c2_new_total - total_medals_c2
                        change_pct_c2 = (change_c2 / total_medals_c2 * 100) if total_medals_c2 > 0 else 0
                        
                        st.markdown(f"""
                        <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['secondary']};'>
                            <h4 style='color: {COLORS['secondary']}; margin: 0;'>{country2}</h4>
                            <p style='color: {COLORS['text']}; margin: 10px 0 5px 0; font-size: 1.1rem;'>Original: <strong>{total_medals_c2}</strong> medals</p>
                            <p style='color: {COLORS['text']}; margin: 5px 0; font-size: 1.1rem;'>New: <strong>{c2_new_total}</strong> medals</p>
                            <p style='color: {"#00A651" if change_c2 >= 0 else "#EE334E"}; margin: 10px 0 0 0; font-size: 1rem;'>
                                Change: <strong>{change_c2:+d}</strong> ({change_pct_c2:+.1f}%)
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show top 10 countries in this scenario
                    st.subheader("📊 Top 10 Countries (Without Selected Sports)")
                    
                    scenario_rankings = scenario_data.groupby('country').size().reset_index(name='medals')
                    scenario_rankings = scenario_rankings.sort_values('medals', ascending=False).head(10)
                    
                    # Highlight selected countries
                    scenario_rankings['color'] = scenario_rankings['country'].apply(
                        lambda x: COLORS['paris_green'] if x == country1 else (
                            COLORS['secondary'] if x == country2 else COLORS['text_secondary']
                        )
                    )
                    
                    fig_scenario = go.Figure()
                    
                    fig_scenario.add_trace(go.Bar(
                        x=scenario_rankings['medals'],
                        y=scenario_rankings['country'],
                        orientation='h',
                        marker=dict(color=scenario_rankings['color']),
                        text=scenario_rankings['medals'],
                        textposition='inside',
                        textfont=dict(size=12, color='white')
                    ))
                    
                    fig_scenario.update_layout(
                        title="Scenario Rankings (Excluded Sports Removed)",
                        plot_bgcolor=COLORS['background'],
                        paper_bgcolor=COLORS['background'],
                        font=dict(color=COLORS['text']),
                        height=400,
                        yaxis={'categoryorder': 'total ascending'},
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_scenario, use_container_width=True)
            
            elif scenario_type == "Gold Medals Only":
                st.markdown(f"<p style='color: {COLORS['text_secondary']};'>Rankings based solely on Gold medal count</p>", unsafe_allow_html=True)
                
                # Gold-only comparison
                col_gold1, col_gold2 = st.columns(2)
                
                with col_gold1:
                    st.markdown(f"""
                    <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; border: 3px solid {COLORS['gold']}; text-align: center;'>
                        <h4 style='color: {COLORS['gold']}; margin: 0 0 15px 0;'>{country1}</h4>
                        <div style='font-size: 4rem; margin: 10px 0;'>🥇</div>
                        <p style='color: {COLORS['gold']}; margin: 0; font-size: 3rem; font-weight: bold;'>{gold_c1}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0;'>Gold Medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_gold2:
                    st.markdown(f"""
                    <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; border: 3px solid {COLORS['gold']}; text-align: center;'>
                        <h4 style='color: {COLORS['gold']}; margin: 0 0 15px 0;'>{country2}</h4>
                        <div style='font-size: 4rem; margin: 10px 0;'>🥇</div>
                        <p style='color: {COLORS['gold']}; margin: 0; font-size: 3rem; font-weight: bold;'>{gold_c2}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0;'>Gold Medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show top 10 by gold
                st.subheader("🥇 Top 10 Countries by Gold Medals")
                
                gold_only = medals_df[medals_df['medal_type'].str.contains('Gold', case=False, na=False)]
                gold_rankings = gold_only.groupby('country').size().reset_index(name='gold_medals')
                gold_rankings = gold_rankings.sort_values('gold_medals', ascending=False).head(10)
                
                gold_rankings['color'] = gold_rankings['country'].apply(
                    lambda x: COLORS['paris_green'] if x == country1 else (
                        COLORS['secondary'] if x == country2 else COLORS['gold']
                    )
                )
                
                fig_gold_rank = go.Figure()
                
                fig_gold_rank.add_trace(go.Bar(
                    x=gold_rankings['gold_medals'],
                    y=gold_rankings['country'],
                    orientation='h',
                    marker=dict(color=gold_rankings['color']),
                    text=gold_rankings['gold_medals'],
                    textposition='inside',
                    textfont=dict(size=12, color='black')
                ))
                
                fig_gold_rank.update_layout(
                    title="Gold Medal Rankings",
                    plot_bgcolor=COLORS['background'],
                    paper_bgcolor=COLORS['background'],
                    font=dict(color=COLORS['text']),
                    height=400,
                    yaxis={'categoryorder': 'total ascending'},
                    showlegend=False
                )
                
                st.plotly_chart(fig_gold_rank, use_container_width=True)
            
            else:  # Gender-Specific
                selected_gender = st.radio("Select Gender:", ["Male", "Female"], horizontal=True)
                
                # Use medals_df for accurate counts (one medal per event)
                # Map gender values: medals.csv uses 'M'/'W', medallists uses 'Male'/'Female'
                gender_map = {'Male': 'M', 'Female': 'W'}
                gender_code = gender_map.get(selected_gender, selected_gender)
                gender_data = medals_df[medals_df['gender'] == gender_code]
                
                c1_gender = gender_data[gender_data['country'] == country1]
                c2_gender = gender_data[gender_data['country'] == country2]
                
                c1_gender_total = len(c1_gender)
                c2_gender_total = len(c2_gender)
                
                col_gend1, col_gend2 = st.columns(2)
                
                with col_gend1:
                    gender_emoji = '♂️' if selected_gender == 'Male' else '♀️'
                    
                    st.markdown(f"""
                    <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; border-left: 5px solid {COLORS['paris_green']}; text-align: center;'>
                        <h4 style='color: {COLORS['paris_green']}; margin: 0 0 15px 0;'>{country1}</h4>
                        <div style='font-size: 3rem; margin: 10px 0;'>{gender_emoji}</div>
                        <p style='color: {COLORS['paris_green']}; margin: 0; font-size: 2.5rem; font-weight: bold;'>{c1_gender_total}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0;'>{selected_gender} Medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_gend2:
                    st.markdown(f"""
                    <div style='background: {COLORS['card_bg']}; padding: 25px; border-radius: 15px; border-left: 5px solid {COLORS['secondary']}; text-align: center;'>
                        <h4 style='color: {COLORS['secondary']}; margin: 0 0 15px 0;'>{country2}</h4>
                        <div style='font-size: 3rem; margin: 10px 0;'>{gender_emoji}</div>
                        <p style='color: {COLORS['secondary']}; margin: 0; font-size: 2.5rem; font-weight: bold;'>{c2_gender_total}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 10px 0 0 0;'>{selected_gender} Medals</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Top 10 countries for this gender
                st.subheader(f"📊 Top 10 Countries - {selected_gender} Medals")
                
                gender_rankings = gender_data.groupby('country').size().reset_index(name='medals')
                gender_rankings = gender_rankings.sort_values('medals', ascending=False).head(10)
                
                gender_rankings['color'] = gender_rankings['country'].apply(
                    lambda x: COLORS['paris_green'] if x == country1 else (
                        COLORS['secondary'] if x == country2 else COLORS['warning']
                    )
                )
                
                fig_gender_rank = go.Figure()
                
                fig_gender_rank.add_trace(go.Bar(
                    x=gender_rankings['medals'],
                    y=gender_rankings['country'],
                    orientation='h',
                    marker=dict(color=gender_rankings['color']),
                    text=gender_rankings['medals'],
                    textposition='inside',
                    textfont=dict(size=12, color='white')
                ))
                
                fig_gender_rank.update_layout(
                    title=f"{selected_gender} Medal Rankings",
                    plot_bgcolor=COLORS['background'],
                    paper_bgcolor=COLORS['background'],
                    font=dict(color=COLORS['text']),
                    height=400,
                    yaxis={'categoryorder': 'total ascending'},
                    showlegend=False
                )
                
                st.plotly_chart(fig_gender_rank, use_container_width=True)

else:
    st.info("No medallist data available for comparison.")

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