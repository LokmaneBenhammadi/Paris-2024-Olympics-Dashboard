"""
Page 5: Advanced Analytics - Creative Insights
Creativity showcase with advanced visualizations and analysis
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.config import COLORS, PAGE_CONFIG
from utils.data_loader import load_athletes, load_medallists, load_events
from utils.filters import create_sidebar_filters, apply_filters, show_filter_summary
from utils.continent_mapper import add_continent_column
from utils.visualizations import create_enhanced_sunburst

# Page configuration
st.set_page_config(
    page_title="Advanced Analytics - Paris 2024",
    page_icon="⭐",
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
    ⭐ Advanced Analytics - Creativity Showcase
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    Beyond the Basics: Advanced Features and Creative Visualizations
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_analytics_data():
    """Load and prepare data for advanced analytics."""
    athletes_df = load_athletes()
    medallists_df = load_medallists()
    events_df = load_events()
    
    try:
        medals_total_df = pd.read_csv('data/medals_total.csv')
    except:
        medals_total_df = pd.DataFrame()
    
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
    
    if not medals_total_df.empty and 'country_code' in medals_total_df.columns:
        medals_total_df = add_continent_column(medals_total_df, 'country_code')
    
    return athletes_df, medallists_df, medals_total_df, events_df

athletes_df, medallists_df, medals_total_df, events_df = load_analytics_data()

# ===== FILTERS =====
filters = create_sidebar_filters(athletes_df, medallists_df, events_df)

# Apply filters
filtered_athletes = apply_filters(athletes_df, filters) if not athletes_df.empty else athletes_df
filtered_medallists = apply_filters(medallists_df, filters) if not medallists_df.empty else medallists_df

# Show filter summary
show_filter_summary(filters, filtered_medallists, medallists_df)

st.markdown(f"""
<div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['paris_green']}; margin-bottom: 30px;'>
    <p style='color: {COLORS['text']}; font-size: 1.1rem; margin: 0;'>
        <strong>💡 Advanced Features:</strong> This page showcases creative analytics beyond standard dashboards.
        Use the <strong>sidebar filters</strong> to refine all visualizations globally.
    </p>
</div>
""", unsafe_allow_html=True)

# ===== 1. TOP PERFORMING COUNTRIES BY CONTINENT & GENDER =====
st.header("🌍 Top Performing Countries")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Explore top medal-winning countries with gender breakdown</p>", unsafe_allow_html=True)

if not filtered_medallists.empty:
    # Only slider for Top N
    top_n = st.slider("Show Top N Countries:", 5, 20, 10, help="Adjust the number of countries to display")
    
    # Total medals ranking
    country_ranks = filtered_medallists.groupby('country').size().reset_index(name='medal_count')
    country_ranks = country_ranks.sort_values('medal_count', ascending=False).head(top_n)
    
    # Gender breakdown if available
    if 'gender' in filtered_medallists.columns:
        gender_performance = filtered_medallists.groupby(['country', 'gender']).size().reset_index(name='medal_count')
        gender_pivot = gender_performance.pivot(index='country', columns='gender', values='medal_count').fillna(0)
        gender_pivot['total'] = gender_pivot.sum(axis=1)
        gender_pivot = gender_pivot.sort_values('total', ascending=False).head(top_n)
        
        # Calculate percentages
        male_pct = (gender_pivot.get('Male', 0) / gender_pivot['total'] * 100).round(1)
        female_pct = (gender_pivot.get('Female', 0) / gender_pivot['total'] * 100).round(1)
        
        fig_gender = go.Figure()
        
        if 'Male' in gender_pivot.columns:
            fig_gender.add_trace(go.Bar(
                name='♂️ Male',
                y=gender_pivot.index,
                x=gender_pivot['Male'],
                orientation='h',
                marker=dict(color=COLORS['secondary'], line=dict(color=COLORS['background'], width=2)),
                text=[f"{int(v)} ({p}%)" for v, p in zip(gender_pivot['Male'], male_pct)],
                textposition='inside',
                textfont=dict(size=11, family='Arial Black'),
                hovertemplate='<b>%{y}</b><br>Male: %{x}<extra></extra>'
            ))
        
        if 'Female' in gender_pivot.columns:
            fig_gender.add_trace(go.Bar(
                name='♀️ Female',
                y=gender_pivot.index,
                x=gender_pivot['Female'],
                orientation='h',
                marker=dict(color=COLORS['paris_green'], line=dict(color=COLORS['background'], width=2)),
                text=[f"{int(v)} ({p}%)" for v, p in zip(gender_pivot['Female'], female_pct)],
                textposition='inside',
                textfont=dict(size=11, family='Arial Black'),
                hovertemplate='<b>%{y}</b><br>Female: %{x}<extra></extra>'
            ))
        
        fig_gender.update_layout(
            barmode='stack',
            title=f"Top {top_n} Countries - Medal Count by Gender (with percentages)",
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], family='Arial Black'),
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Medal Count',
            yaxis_title='',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        # Simple bar chart without gender breakdown
        fig_rank = go.Figure()
        
        fig_rank.add_trace(go.Bar(
            x=country_ranks['medal_count'],
            y=country_ranks['country'],
            orientation='h',
            marker=dict(
                color=country_ranks['medal_count'],
                colorscale=[
                    [0, COLORS['secondary']],
                    [0.5, COLORS['paris_green']],
                    [1, COLORS['gold']]
                ],
                line=dict(color=COLORS['background'], width=2)
            ),
            text=country_ranks['medal_count'],
            textposition='inside',
            textfont=dict(size=14, color='white', family='Arial Black'),
            hovertemplate='<b>%{y}</b><br>Medals: %{x}<extra></extra>'
        ))
        
        fig_rank.update_layout(
            title=f"Top {top_n} Countries - Total Medals",
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], family='Arial Black'),
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Total Medals',
            yaxis_title='',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig_rank, use_container_width=True)
else:
    st.info("Medallist data not available")

st.markdown("---")

# ===== 2. ATHLETES BY SPORT DISCIPLINE, COUNTRY & GENDER =====
st.header("🏃 Athletes by Sport Discipline, Country & Gender")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Deep dive into athlete distribution with multiple visualization options</p>", unsafe_allow_html=True)

if not filtered_athletes.empty and 'disciplines' in filtered_athletes.columns:
    # Output options (no additional filters - use sidebar)
    output_type = st.radio("📊 View As:", ["Sunburst Chart", "Data Table", "Statistics"], horizontal=True)
    
    if output_type == "Sunburst Chart":
        # Create hierarchy: Sport -> Country -> Gender
        hierarchy_data = filtered_athletes.groupby(['disciplines', 'country', 'gender']).size().reset_index(name='athletes')
        
        if not hierarchy_data.empty:
            fig_sunburst = create_enhanced_sunburst(
                hierarchy_data,
                path_cols=['disciplines', 'country', 'gender'],
                value_col='athletes',
                title="Athletes Hierarchy: Sport → Country → Gender"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
    
    elif output_type == "Data Table":
        st.subheader("📋 Searchable Athlete Data")
        
        # Search box
        search_query = st.text_input("🔍 Search athletes by name:", "", help="Filter the current data by athlete name")
        
        display_cols = ['name', 'country', 'gender', 'age', 'height', 'weight', 'disciplines']
        available_cols = [col for col in display_cols if col in filtered_athletes.columns]
        
        if search_query:
            search_data = filtered_athletes[
                filtered_athletes['name'].str.contains(search_query, case=False, na=False)
            ]
        else:
            search_data = filtered_athletes
        
        if available_cols and not search_data.empty:
            st.dataframe(
                search_data[available_cols].sort_values('name'),
                use_container_width=True,
                hide_index=True
            )
            
            st.info(f"Showing {len(search_data)} of {len(filtered_athletes)} athletes")
        else:
            st.info("No athletes found matching your criteria")
    
    else:  # Statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            # Gender breakdown pie
            if 'gender' in filtered_athletes.columns:
                gender_counts = filtered_athletes['gender'].value_counts()
                
                fig_gender_pie = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title="Gender Distribution",
                    color_discrete_map={
                        'Male': COLORS['secondary'],
                        'Female': COLORS['paris_green']
                    },
                    hole=0.4
                )
                
                fig_gender_pie.update_layout(
                    plot_bgcolor=COLORS['background'],
                    paper_bgcolor=COLORS['background'],
                    font=dict(color=COLORS['text']),
                    height=350
                )
                
                st.plotly_chart(fig_gender_pie, use_container_width=True)
        
        with col_stat2:
            # Key metrics
            st.markdown(f"""
            <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; margin-bottom: 15px;
                        border-left: 5px solid {COLORS['paris_green']};'>
                <p style='color: {COLORS['text_secondary']}; margin: 0;'>Total Athletes</p>
                <p style='color: {COLORS['paris_green']}; margin: 5px 0 0 0; font-size: 2.5rem; font-weight: bold;'>{len(filtered_athletes)}</p>
            </div>
            
            <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; margin-bottom: 15px;
                        border-left: 5px solid {COLORS['secondary']};'>
                <p style='color: {COLORS['text_secondary']}; margin: 0;'>Countries</p>
                <p style='color: {COLORS['secondary']}; margin: 5px 0 0 0; font-size: 2.5rem; font-weight: bold;'>{filtered_athletes['country'].nunique()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if 'age' in filtered_athletes.columns:
                avg_age = filtered_athletes['age'].mean()
                st.markdown(f"""
                <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px;
                            border-left: 5px solid {COLORS['warning']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0;'>Average Age</p>
                    <p style='color: {COLORS['warning']}; margin: 5px 0 0 0; font-size: 2.5rem; font-weight: bold;'>{avg_age:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_stat3:
            # Top countries
            top_countries = filtered_athletes['country'].value_counts().head(10)
            
            fig_top = go.Figure()
            
            fig_top.add_trace(go.Bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                marker=dict(color=COLORS['paris_green']),
                text=top_countries.values,
                textposition='inside'
            ))
            
            fig_top.update_layout(
                title="Top 10 Countries",
                plot_bgcolor=COLORS['background'],
                paper_bgcolor=COLORS['background'],
                font=dict(color=COLORS['text']),
                height=350,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            st.plotly_chart(fig_top, use_container_width=True)
else:
    st.info("Athlete data not available")

st.markdown("---")

# ===== 3. WHO WON THE DAY? =====
st.header("🏆 Who Won the Day? - Daily Medal Winners")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Explore medals awarded on any day of the Olympics</p>", unsafe_allow_html=True)

if not filtered_medallists.empty and 'medal_date' in filtered_medallists.columns:
    # Parse dates
    filtered_medallists['medal_date'] = pd.to_datetime(filtered_medallists['medal_date'], errors='coerce')
    
    # Get date range
    valid_dates = filtered_medallists['medal_date'].dropna()
    
    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        
        # Calendar date picker
        col_date1, col_date2 = st.columns([2, 2])
        
        with col_date1:
            selected_date = st.date_input(
                "📅 Select a Day:",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                help="Choose a day to see all medals awarded"
            )
        
        # Filter by date
        day_medals = filtered_medallists[filtered_medallists['medal_date'].dt.date == selected_date]
        
        if not day_medals.empty:
            # Daily Summary
            st.markdown(f"<h3 style='text-align: center; color: {COLORS['paris_green']}; margin: 20px 0;'>📊 {selected_date.strftime('%A, %B %d, %Y')}</h3>", unsafe_allow_html=True)
            
            col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
            
            total_medals = len(day_medals)
            gold_count = len(day_medals[day_medals['medal_type'].str.contains('Gold', case=False, na=False)])
            silver_count = len(day_medals[day_medals['medal_type'].str.contains('Silver', case=False, na=False)])
            bronze_count = len(day_medals[day_medals['medal_type'].str.contains('Bronze', case=False, na=False)])
            sports_count = day_medals['discipline'].nunique()
            
            with col_s1:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; border-radius: 15px; border: 3px solid {COLORS['paris_green']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Total</p>
                    <p style='color: {COLORS['paris_green']}; margin: 5px 0 0 0; font-size: 2rem; font-weight: bold;'>{total_medals}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s2:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; border-radius: 15px; border: 3px solid {COLORS['gold']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥇 Gold</p>
                    <p style='color: {COLORS['gold']}; margin: 5px 0 0 0; font-size: 2rem; font-weight: bold;'>{gold_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s3:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; border-radius: 15px; border: 3px solid {COLORS['silver']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥈 Silver</p>
                    <p style='color: {COLORS['silver']}; margin: 5px 0 0 0; font-size: 2rem; font-weight: bold;'>{silver_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s4:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; border-radius: 15px; border: 3px solid {COLORS['bronze']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>🥉 Bronze</p>
                    <p style='color: {COLORS['bronze']}; margin: 5px 0 0 0; font-size: 2rem; font-weight: bold;'>{bronze_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s5:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: {COLORS['card_bg']}; border-radius: 15px; border: 3px solid {COLORS['secondary']};'>
                    <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Sports</p>
                    <p style='color: {COLORS['secondary']}; margin: 5px 0 0 0; font-size: 2rem; font-weight: bold;'>{sports_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Daily MVP
            if 'name' in day_medals.columns:
                athlete_day_medals = day_medals['name'].value_counts()
                max_medals_day = athlete_day_medals.max()
                
                if max_medals_day > 0:
                    mvps = athlete_day_medals[athlete_day_medals == max_medals_day]
                    
                    st.markdown(f"<h3 style='color: {COLORS['gold']}; text-align: center; margin: 20px 0;'>🌟 Daily MVP{' (Tie)' if len(mvps) > 1 else ''}</h3>", unsafe_allow_html=True)
                    
                    mvp_cols = st.columns(min(len(mvps), 3))
                    
                    for idx, (mvp_name, medal_count) in enumerate(mvps.head(3).items()):
                        with mvp_cols[idx]:
                            mvp_data = day_medals[day_medals['name'] == mvp_name].iloc[0]
                            country = mvp_data.get('country', 'Unknown')
                            sport = mvp_data.get('discipline', 'Unknown')
                            
                            st.markdown(f"""
                            <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['gold']}30);
                                        border-radius: 20px; border: 4px solid {COLORS['gold']}; box-shadow: 0 10px 40px rgba(212,175,55,0.4);'>
                                <div style='font-size: 4rem; margin-bottom: 10px;'>🏆</div>
                                <h4 style='color: {COLORS['gold']}; margin: 10px 0;'>{mvp_name}</h4>
                                <p style='color: {COLORS['text']}; margin: 5px 0;'>{country}</p>
                                <p style='color: {COLORS['text_secondary']}; margin: 5px 0; font-size: 0.9rem;'>{sport}</p>
                                <p style='color: {COLORS['gold']}; margin: 15px 0 0 0; font-size: 2rem; font-weight: bold;'>{int(medal_count)}</p>
                                <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 0.8rem;'>Medals Today</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Medal Winners by Sport
            st.subheader("🏅 All Medal Winners")
            
            # Group by sport
            sports_on_day = sorted(day_medals['discipline'].unique())
            
            for sport in sports_on_day:
                sport_medals = day_medals[day_medals['discipline'] == sport]
                
                with st.expander(f"🏅 {sport} ({len(sport_medals)} medals)", expanded=len(sports_on_day) <= 5):
                    for _, medal in sport_medals.iterrows():
                        medal_type = medal.get('medal_type', 'Medal')
                        athlete_name = medal.get('name', 'Unknown')
                        country = medal.get('country', 'Unknown')
                        event = medal.get('event', 'Unknown Event')
                        gender = medal.get('gender', '')
                        
                        # Medal emoji
                        if 'Gold' in medal_type:
                            medal_emoji = '🥇'
                            medal_color = COLORS['gold']
                        elif 'Silver' in medal_type:
                            medal_emoji = '🥈'
                            medal_color = COLORS['silver']
                        else:
                            medal_emoji = '🥉'
                            medal_color = COLORS['bronze']
                        
                        gender_emoji = '♂️' if gender == 'Male' else '♀️' if gender == 'Female' else '⚥'
                        
                        st.markdown(f"""
                        <div style='background: {COLORS['card_bg']}; padding: 15px; border-radius: 10px; margin: 8px 0;
                                    border-left: 5px solid {medal_color}; display: flex; align-items: center;'>
                            <div style='font-size: 2rem; margin-right: 15px;'>{medal_emoji}</div>
                            <div style='flex-grow: 1;'>
                                <strong style='color: {COLORS['text']}; font-size: 1.1rem;'>{athlete_name}</strong>
                                <span style='color: {COLORS['text_secondary']}; margin-left: 10px;'>{gender_emoji} {country}</span>
                                <br>
                                <span style='color: {COLORS['text_secondary']}; font-size: 0.9rem;'>{event}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Country Performance Summary
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🌍 Country Performance Summary")
            
            country_day = day_medals.groupby('country').agg({
                'medal_type': lambda x: {
                    'gold': sum('Gold' in str(m) for m in x),
                    'silver': sum('Silver' in str(m) for m in x),
                    'bronze': sum('Bronze' in str(m) for m in x),
                    'total': len(x)
                }
            }).reset_index()
            
            country_day['gold'] = country_day['medal_type'].apply(lambda x: x['gold'])
            country_day['silver'] = country_day['medal_type'].apply(lambda x: x['silver'])
            country_day['bronze'] = country_day['medal_type'].apply(lambda x: x['bronze'])
            country_day['total'] = country_day['medal_type'].apply(lambda x: x['total'])
            country_day = country_day.drop('medal_type', axis=1).sort_values('total', ascending=False).head(15)
            
            fig_country_day = go.Figure()
            
            fig_country_day.add_trace(go.Bar(
                name='🥇 Gold',
                x=country_day['country'],
                y=country_day['gold'],
                marker=dict(color=COLORS['gold']),
                text=country_day['gold'],
                textposition='inside'
            ))
            
            fig_country_day.add_trace(go.Bar(
                name='🥈 Silver',
                x=country_day['country'],
                y=country_day['silver'],
                marker=dict(color=COLORS['silver']),
                text=country_day['silver'],
                textposition='inside'
            ))
            
            fig_country_day.add_trace(go.Bar(
                name='🥉 Bronze',
                x=country_day['country'],
                y=country_day['bronze'],
                marker=dict(color=COLORS['bronze']),
                text=country_day['bronze'],
                textposition='inside'
            ))
            
            fig_country_day.update_layout(
                barmode='stack',
                title=f"Top Countries on {selected_date.strftime('%B %d, %Y')}",
                plot_bgcolor=COLORS['background'],
                paper_bgcolor=COLORS['background'],
                font=dict(color=COLORS['text'], family='Arial Black'),
                height=400,
                xaxis=dict(tickangle=45),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig_country_day, use_container_width=True)
        else:
            st.info(f"No medals awarded on {selected_date.strftime('%B %d, %Y')}. Try another date within the Olympics period (July 26 - August 11, 2024).")
    else:
        st.warning("No valid medal dates found in the data")
else:
    st.info("Medal timeline data not available. Ensure 'medal_date' column exists in medallists data.")

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