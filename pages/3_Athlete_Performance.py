"""
Page 3: Athlete Performance - The Human Story
Individual athlete analysis and demographics
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import re  # Add this line
from config.config import COLORS, PAGE_CONFIG
from utils.data_loader import load_athletes, load_coaches, load_medallists, load_teams, load_events
from utils.filters import create_sidebar_filters, apply_filters, show_filter_summary
from utils.continent_mapper import add_continent_column
from utils.visualizations import (
    create_athlete_age_violin,
    create_athlete_age_box_by_sport,
    create_gender_distribution_pie,
    create_gender_distribution_bar,
    create_top_athletes_stacked_bar
)

# Page configuration
st.set_page_config(
    page_title="Athlete Performance - Paris 2024",
    page_icon="👤",
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
    👤 Athlete Performance - The Human Story
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 10px;'>
    Individual Athletes, Their Achievements, and Demographics
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 20px 0;'>
""", unsafe_allow_html=True)

# ===== HELPER FUNCTION: FLAG EMOJI =====
def get_flag_emoji(country_code):
    """Convert IOC country code to flag emoji using regional indicator symbols."""
    if not country_code or len(country_code) != 3:
        return '🏳️'
    
    # IOC to ISO 3166-1 alpha-2 mapping
    ioc_to_iso2 = {
        'AFG': 'AF', 'ALB': 'AL', 'ALG': 'DZ', 'AND': 'AD', 'ANG': 'AO',
        'ANT': 'AG', 'ARG': 'AR', 'ARM': 'AM', 'ARU': 'AW', 'ASA': 'AS',
        'AUS': 'AU', 'AUT': 'AT', 'AZE': 'AZ', 'BAH': 'BS', 'BAN': 'BD',
        'BAR': 'BB', 'BDI': 'BI', 'BEL': 'BE', 'BEN': 'BJ', 'BER': 'BM',
        'BHU': 'BT', 'BIH': 'BA', 'BIZ': 'BZ', 'BOL': 'BO', 'BOT': 'BW',
        'BRA': 'BR', 'BRN': 'BH', 'BRU': 'BN', 'BUL': 'BG', 'BUR': 'BF',
        'CAF': 'CF', 'CAM': 'KH', 'CAN': 'CA', 'CAY': 'KY', 'CGO': 'CG',
        'CHA': 'TD', 'CHI': 'CL', 'CHN': 'CN', 'CIV': 'CI', 'CMR': 'CM',
        'COD': 'CD', 'COK': 'CK', 'COL': 'CO', 'COM': 'KM', 'CPV': 'CV',
        'CRC': 'CR', 'CRO': 'HR', 'CUB': 'CU', 'CYP': 'CY', 'CZE': 'CZ',
        'DEN': 'DK', 'DJI': 'DJ', 'DMA': 'DM', 'DOM': 'DO', 'ECU': 'EC',
        'EGY': 'EG', 'ERI': 'ER', 'ESA': 'SV', 'ESP': 'ES', 'EST': 'EE',
        'ETH': 'ET', 'FIJ': 'FJ', 'FIN': 'FI', 'FRA': 'FR', 'FSM': 'FM',
        'GAB': 'GA', 'GAM': 'GM', 'GBR': 'GB', 'GBS': 'GW', 'GEO': 'GE',
        'GEQ': 'GQ', 'GER': 'DE', 'GHA': 'GH', 'GRE': 'GR', 'GRN': 'GD',
        'GUA': 'GT', 'GUI': 'GN', 'GUM': 'GU', 'GUY': 'GY', 'HAI': 'HT',
        'HKG': 'HK', 'HON': 'HN', 'HUN': 'HU', 'INA': 'ID', 'IND': 'IN',
        'IRI': 'IR', 'IRL': 'IE', 'IRQ': 'IQ', 'ISL': 'IS', 'ISR': 'IL',
        'ISV': 'VI', 'ITA': 'IT', 'JAM': 'JM', 'JOR': 'JO', 'JPN': 'JP',
        'KAZ': 'KZ', 'KEN': 'KE', 'KGZ': 'KG', 'KIR': 'KI', 'KOR': 'KR',
        'KOS': 'XK', 'KSA': 'SA', 'KUW': 'KW', 'LAO': 'LA', 'LAT': 'LV',
        'LBA': 'LY', 'LBN': 'LB', 'LBR': 'LR', 'LCA': 'LC', 'LES': 'LS',
        'LIE': 'LI', 'LTU': 'LT', 'LUX': 'LU', 'MAD': 'MG', 'MAR': 'MA',
        'MAS': 'MY', 'MAW': 'MW', 'MDA': 'MD', 'MDV': 'MV', 'MEX': 'MX',
        'MGL': 'MN', 'MHL': 'MH', 'MKD': 'MK', 'MLI': 'ML', 'MLT': 'MT',
        'MNE': 'ME', 'MON': 'MC', 'MOZ': 'MZ', 'MRI': 'MU', 'MTN': 'MR',
        'MYA': 'MM', 'NAM': 'NA', 'NCA': 'NI', 'NED': 'NL', 'NEP': 'NP',
        'NGR': 'NG', 'NIG': 'NE', 'NOR': 'NO', 'NRU': 'NR', 'NZL': 'NZ',
        'OMA': 'OM', 'PAK': 'PK', 'PAN': 'PA', 'PAR': 'PY', 'PER': 'PE',
        'PHI': 'PH', 'PLE': 'PS', 'PLW': 'PW', 'PNG': 'PG', 'POL': 'PL',
        'POR': 'PT', 'PRK': 'KP', 'PUR': 'PR', 'QAT': 'QA', 'ROU': 'RO',
        'RSA': 'ZA', 'RUS': 'RU', 'RWA': 'RW', 'SAM': 'WS', 'SEN': 'SN',
        'SEY': 'SC', 'SGP': 'SG', 'SKN': 'KN', 'SLE': 'SL', 'SLO': 'SI',
        'SMR': 'SM', 'SOL': 'SB', 'SOM': 'SO', 'SRB': 'RS', 'SRI': 'LK',
        'SSD': 'SS', 'STP': 'ST', 'SUD': 'SD', 'SUI': 'CH', 'SUR': 'SR',
        'SVK': 'SK', 'SWE': 'SE', 'SYR': 'SY', 'TAN': 'TZ', 'TGA': 'TO',
        'THA': 'TH', 'TJK': 'TJ', 'TKM': 'TM', 'TLS': 'TL', 'TOG': 'TG',
        'TPE': 'TW', 'TTO': 'TT', 'TUN': 'TN', 'TUR': 'TR', 'TUV': 'TV',
        'UAE': 'AE', 'UGA': 'UG', 'UKR': 'UA', 'URU': 'UY', 'USA': 'US',
        'UZB': 'UZ', 'VAN': 'VU', 'VEN': 'VE', 'VIE': 'VN', 'VIN': 'VC',
        'YEM': 'YE', 'ZAM': 'ZM', 'ZIM': 'ZW'
    }
    
    iso2 = ioc_to_iso2.get(country_code.upper())
    if iso2:
        return ''.join(chr(127397 + ord(char)) for char in iso2.upper())
    
    return '🏳️'

# ===== DATA LOADING =====
@st.cache_data
def load_athlete_data():
    """Load and prepare data for athlete performance analysis."""
    athletes_df = load_athletes()
    coaches_df = load_coaches()
    medallists_df = load_medallists()
    teams_df = load_teams()
    events_df = load_events()
    
    # Calculate age from birth_date
    if not athletes_df.empty and 'birth_date' in athletes_df.columns:
        athletes_df['birth_date'] = pd.to_datetime(athletes_df['birth_date'], errors='coerce')
        olympics_date = pd.Timestamp('2024-07-26')
        athletes_df['age'] = (olympics_date - athletes_df['birth_date']).dt.days // 365
        athletes_df.loc[athletes_df['age'] <= 0, 'age'] = pd.NA
        athletes_df.loc[athletes_df['age'] > 100, 'age'] = pd.NA
    
    # Add continent info
    if not athletes_df.empty and 'country_code' in athletes_df.columns:
        athletes_df = add_continent_column(athletes_df, 'country_code')
    
    if not medallists_df.empty and 'country_code' in medallists_df.columns:
        medallists_df = add_continent_column(medallists_df, 'country_code')
    
    return athletes_df, coaches_df, medallists_df, teams_df, events_df

athletes_df, coaches_df, medallists_df, teams_df, events_df = load_athlete_data()

# ===== FILTERS =====
filters = create_sidebar_filters(athletes_df, medallists_df, events_df)

# Apply filters
filtered_athletes = apply_filters(athletes_df, filters) if not athletes_df.empty else athletes_df
filtered_medallists = apply_filters(medallists_df, filters) if not medallists_df.empty else medallists_df

# Show filter summary
show_filter_summary(filters, filtered_athletes, athletes_df)

# ===== 1. ATHLETE DETAILED PROFILE CARD =====
st.header("🔍 Athlete Detailed Profile")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Search and view detailed information about individual athletes</p>", unsafe_allow_html=True)

if not filtered_athletes.empty and 'name' in filtered_athletes.columns:
    # Search input
    search_query = st.text_input(
        "🔎 Search for an athlete by name",
        placeholder="Start typing athlete name...",
        help="Enter at least 3 characters to search"
    )
    
    if search_query and len(search_query) >= 3:
        # Filter athletes based on search query
        matching_athletes = filtered_athletes[
            filtered_athletes['name'].str.contains(search_query, case=False, na=False)
        ]
        
        if not matching_athletes.empty:
            # Show matching results in a selectbox
            athlete_options = []
            for idx, row in matching_athletes.iterrows():
                athlete_name = row.get('name', 'Unknown')
                country = row.get('country', 'Unknown')
                athlete_options.append(f"{athlete_name} ({country})")
            
            if len(athlete_options) > 1:
                selected_athlete_display = st.selectbox(
                    f"Found {len(athlete_options)} athletes:",
                    options=athlete_options
                )
            else:
                selected_athlete_display = athlete_options[0]
                st.success(f"✅ Found: {selected_athlete_display}")
            
            # Extract athlete name from selection
            athlete_name = selected_athlete_display.split(" (")[0]
            athlete_data = filtered_athletes[filtered_athletes['name'] == athlete_name].iloc[0]
            
            # Display athlete profile card
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                # Profile image with gender-based placeholder
                image_displayed = False
                
                if 'url' in athlete_data and pd.notna(athlete_data['url']) and str(athlete_data['url']).strip():
                    try:
                        st.image(athlete_data['url'], width=200)
                        image_displayed = True
                    except:
                        pass
                
                if not image_displayed:
                    gender = str(athlete_data.get('gender', '')).strip().lower()
                    female_placeholder = Path("assets/female_placeholder.png")
                    male_placeholder = Path("assets/male_placeholder.png")
                    
                    if gender in ['female', 'f', 'w', 'women']:
                        if female_placeholder.exists():
                            st.image(str(female_placeholder), width=200)
                        else:
                            st.markdown(f"""
                            <div style='width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; 
                                        background: linear-gradient(135deg, {COLORS['paris_green']}, {COLORS['gold']});
                                        display: flex; align-items: center; justify-content: center;
                                        font-size: 5rem; border: 4px solid {COLORS['paris_green']};
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
                                👩
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        if male_placeholder.exists():
                            st.image(str(male_placeholder), width=200)
                        else:
                            st.markdown(f"""
                            <div style='width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; 
                                        background: linear-gradient(135deg, {COLORS['secondary']}, {COLORS['paris_green']});
                                        display: flex; align-items: center; justify-content: center;
                                        font-size: 5rem; border: 4px solid {COLORS['secondary']};
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
                                👨
                            </div>
                            """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<h2 style='color: {COLORS['paris_green']}; margin: 0;'>🏅 {athlete_data.get('name', 'Unknown')}</h2>", unsafe_allow_html=True)
                
                # Country with flag emoji (REPLACED globe)
                country_code = athlete_data.get('country_code', '')
                country_name = athlete_data.get('country', 'Unknown')
                flag = get_flag_emoji(country_code)
                st.markdown(f"<h3 style='color: {COLORS['text']}; margin: 10px 0;'>{flag} {country_name}</h3>", unsafe_allow_html=True)
                
                # Physical stats
                height = athlete_data.get('height', None)
                weight = athlete_data.get('weight', None)
                gender = athlete_data.get('gender', 'N/A')
                birth_date = athlete_data.get('birth_date', 'N/A')
                
                height_str = f"{height} cm" if pd.notna(height) and height > 0 else "N/A"
                weight_str = f"{weight} kg" if pd.notna(weight) and weight > 0 else "N/A"
                
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Height:</strong> {height_str}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Weight:</strong> {weight_str}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Gender:</strong> {gender}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Birth Date:</strong> {birth_date}</p>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<h3 style='color: {COLORS['secondary']}; margin: 0 0 15px 0;'>📋 Competition Details</h3>", unsafe_allow_html=True)
                
                # Coach information
                coach_info = "Not available"
                if 'coach' in athlete_data.index and pd.notna(athlete_data.get('coach')):
                    coaches_raw = str(athlete_data.get('coach', ''))
                    if coaches_raw and coaches_raw != 'nan' and coaches_raw.strip():
                        coaches_clean = re.sub(r'<br>|<br/>|<br />', ', ', coaches_raw)
                        coaches_clean = re.sub(r'<[^>]+>', '', coaches_clean)
                        coach_info = coaches_clean.strip()
                
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Coach(es):</strong> {coach_info}</p>", unsafe_allow_html=True)
                
                # Disciplines
                disciplines_raw = athlete_data.get('disciplines', 'N/A')
                if pd.notna(disciplines_raw) and disciplines_raw != 'N/A':
                    disciplines_str = str(disciplines_raw)
                    if disciplines_str.startswith('[') and disciplines_str.endswith(']'):
                        disciplines_clean = disciplines_str.strip('[]').replace("'", "").replace('"', '')
                    else:
                        disciplines_clean = disciplines_str
                else:
                    disciplines_clean = 'N/A'
                
                st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 5px 0;'><strong>Discipline(s):</strong> {disciplines_clean}</p>", unsafe_allow_html=True)
                
                # Check for medals - SIMPLIFIED (medallists.csv has athlete names for all sports!)
                athlete_name = athlete_data.get('name', '')
                
                if not medallists_df.empty and athlete_name and 'name' in medallists_df.columns:
                    # Direct name match works for BOTH individual and team sports in medallists.csv
                    athlete_medals = medallists_df[medallists_df['name'] == athlete_name]
                    
                    if not athlete_medals.empty and 'medal_type' in athlete_medals.columns:
                        medal_counts = athlete_medals['medal_type'].value_counts()
                        gold = medal_counts.get('Gold Medal', 0) + medal_counts.get('Gold', 0)
                        silver = medal_counts.get('Silver Medal', 0) + medal_counts.get('Silver', 0)
                        bronze = medal_counts.get('Bronze Medal', 0) + medal_counts.get('Bronze', 0)
                        
                        if gold + silver + bronze > 0:
                            st.markdown(f"<p style='color: {COLORS['gold']}; margin: 15px 0 5px 0; font-size: 1.2rem;'><strong>🏅 Medals Won:</strong></p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: {COLORS['text']}; margin: 0;'>🥇 Gold: {gold} | 🥈 Silver: {silver} | 🥉 Bronze: {bronze}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 15px 0 5px 0;'><em>No medals won at Paris 2024</em></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 15px 0 5px 0;'><em>No medals won at Paris 2024</em></p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 15px 0 5px 0;'><em>No medals won at Paris 2024</em></p>", unsafe_allow_html=True)
        else:
            st.warning(f"No athletes found matching '{search_query}'. Try a different search term.")
    elif search_query:
        st.info("Please enter at least 3 characters to search.")
    else:
        st.info("👆 Enter an athlete's name in the search box above to view their profile.")
else:
    st.info("No athlete data available.")

st.markdown("---")
# ===== 2. AGE DISTRIBUTION =====
st.header("📊 Athlete Age Distribution")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Age distribution analysis by sport and gender</p>", unsafe_allow_html=True)

if not filtered_athletes.empty and 'age' in filtered_athletes.columns:
    athletes_with_age = filtered_athletes[filtered_athletes['age'].notna()]
    
    if not athletes_with_age.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age Distribution by Gender")
            fig_gender = create_athlete_age_violin(athletes_with_age, "Age Distribution by Gender")
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            st.subheader("Age Distribution by Sport")
            fig_sport = create_athlete_age_box_by_sport(athletes_with_age, n=10, title="Age Distribution by Top 10 Sports")
            st.plotly_chart(fig_sport, use_container_width=True)
    else:
        st.info("Age data not available for the selected filters.")
else:
    st.info("Age data not available.")
 
st.markdown("---")

# ===== 3. GENDER DISTRIBUTION =====
st.header("⚥ Gender Distribution Analysis")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Gender balance across continents and countries</p>", unsafe_allow_html=True)

if not filtered_athletes.empty and 'gender' in filtered_athletes.columns:
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for gender distribution
        fig_pie = create_gender_distribution_pie(filtered_athletes, "Gender Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📊 Gender Statistics")
        
        gender_counts = filtered_athletes['gender'].value_counts()
        total = gender_counts.sum()
        
        for gender, count in gender_counts.items():
            percentage = (count / total * 100)
            color = COLORS['paris_green'] if gender == 'Female' else COLORS['secondary']
            icon = '♀️' if gender == 'Female' else '♂️' if gender == 'Male' else '⚥'
            
            st.markdown(f"""
            <div style='background: {COLORS['card_bg']}; padding: 20px; border-radius: 10px; margin: 10px 0;
                        border-left: 5px solid {color}; box-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <div>
                        <h4 style='color: {COLORS['text']}; margin: 0; font-size: 1.2rem;'>{icon} {gender}</h4>
                        <p style='color: {COLORS['text']}; font-size: 2.5rem; font-weight: bold; margin: 10px 0 5px 0;'>{count:,}</p>
                        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 1rem;'>{percentage:.1f}% of total</p>
                    </div>
                    <div style='font-size: 4rem; opacity: 0.3;'>{icon}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional insights
        st.markdown("<br>", unsafe_allow_html=True)
    
else:
    st.info("Gender data not available.")

st.markdown("---")

# ===== 4. TOP ATHLETES BY MEDALS =====
st.header("🏆 Top Athletes by Medal Count")
st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 20px;'>Athletes with the most medals at Paris 2024</p>", unsafe_allow_html=True)

if not filtered_medallists.empty:
    fig_top, top_athletes = create_top_athletes_stacked_bar(filtered_medallists, n=10, title="Top 10 Athletes by Total Medal Count")
    
    if fig_top and not top_athletes.empty:
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Podium display for top 3
        if len(top_athletes) >= 3:
            st.markdown(f"<h3 style='text-align: center; color: {COLORS['paris_green']}; margin: 30px 0 20px 0;'>🥇 Top 3 Medal Winners</h3>", unsafe_allow_html=True)
            
            p1, p2, p3 = st.columns(3)
            
            with p1:
                athlete = top_athletes.iloc[1]
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['silver']}20);
                            border-radius: 15px; border: 3px solid {COLORS['silver']}; 
                            box-shadow: 0 5px 25px {COLORS['silver']}40;'>
                    <div style='font-size: 3rem; margin-bottom: 10px;'>🥈</div>
                    <h3 style='color: {COLORS['silver']}; margin: 10px 0; font-size: 1.2rem;'>{athlete['name']}</h3>
                    <p style='color: {COLORS['text_secondary']}; margin: 5px 0;'>{athlete['country']}</p>
                    <p style='color: {COLORS['text']}; margin: 10px 0; font-size: 2rem; font-weight: bold;'>{int(athlete['total_medals'])}</p>
                    <p style='color: {COLORS['text_secondary']}; margin: 0;'>Total Medals</p>
                </div>
                """, unsafe_allow_html=True)
            
            with p2:
                athlete = top_athletes.iloc[0]
                st.markdown(f"""
                <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['gold']}30);
                            border-radius: 15px; border: 4px solid {COLORS['gold']}; 
                            box-shadow: 0 8px 35px {COLORS['gold']}60; transform: scale(1.05);'>
                    <div style='font-size: 4rem; margin-bottom: 10px;'>🥇</div>
                    <h3 style='color: {COLORS['gold']}; margin: 10px 0; font-size: 1.4rem;'>{athlete['name']}</h3>
                    <p style='color: {COLORS['text_secondary']}; margin: 5px 0;'>{athlete['country']}</p>
                    <p style='color: {COLORS['text']}; margin: 10px 0; font-size: 2.5rem; font-weight: bold;'>{int(athlete['total_medals'])}</p>
                    <p style='color: {COLORS['text_secondary']}; margin: 0;'>Total Medals</p>
                </div>
                """, unsafe_allow_html=True)
            
            with p3:
                athlete = top_athletes.iloc[2]
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['card_bg']}, {COLORS['bronze']}20);
                            border-radius: 15px; border: 3px solid {COLORS['bronze']}; 
                            box-shadow: 0 5px 25px {COLORS['bronze']}40;'>
                    <div style='font-size: 3rem; margin-bottom: 10px;'>🥉</div>
                    <h3 style='color: {COLORS['bronze']}; margin: 10px 0; font-size: 1.2rem;'>{athlete['name']}</h3>
                    <p style='color: {COLORS['text_secondary']}; margin: 5px 0;'>{athlete['country']}</p>
                    <p style='color: {COLORS['text']}; margin: 10px 0; font-size: 2rem; font-weight: bold;'>{int(athlete['total_medals'])}</p>
                    <p style='color: {COLORS['text_secondary']}; margin: 0;'>Total Medals</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No medal data available for athletes.")
else:
    st.info("No medal data available.")

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