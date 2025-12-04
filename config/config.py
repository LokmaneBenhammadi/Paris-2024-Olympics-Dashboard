# Paris 2024 Olympics Dashboard Configuration

# ============================================================================
# COLOR SCHEMES
# ============================================================================

# Paris 2024 Official Colors
COLORS = {
    'primary': '#FF6B9D',      # Paris 2024 Pink
    'secondary': '#0085CA',    # Olympic Blue
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'bronze': '#CD7F32',
    'background': '#F8F9FA',
    'text': '#212529',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545'
}

# Medal colors for charts
MEDAL_COLORS = {
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
    'Bronze': '#CD7F32'
}

# Continent colors
CONTINENT_COLORS = {
    'Europe': '#0085CA',
    'Asia': '#FF6B9D',
    'Africa': '#28A745',
    'North America': '#FFC107',
    'South America': '#DC3545',
    'Oceania': '#6F42C1'
}

# ============================================================================
# APP SETTINGS
# ============================================================================

APP_TITLE = "🏅 Paris 2024 Olympics Dashboard"
APP_SUBTITLE = "LA28 Volunteer Selection Challenge"
PAGE_ICON = "🏅"

# Streamlit page config
PAGE_CONFIG = {
    'page_title': APP_TITLE,
    'page_icon': PAGE_ICON,
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# ============================================================================
# DATA PATHS
# ============================================================================

DATA_DIR = "data/"

# Main CSV files
DATA_FILES = {
    'athletes': f'{DATA_DIR}athletes.csv',
    'coaches': f'{DATA_DIR}coaches.csv',
    'events': f'{DATA_DIR}events.csv',
    'medals': f'{DATA_DIR}medals.csv',
    'medals_total': f'{DATA_DIR}medals_total.csv',
    'medallists': f'{DATA_DIR}medallists.csv',
    'nocs': f'{DATA_DIR}nocs.csv',
    'schedules': f'{DATA_DIR}schedules.csv',
    'schedules_preliminary': f'{DATA_DIR}schedules_preliminary.csv',
    'teams': f'{DATA_DIR}teams.csv',
    'technical_officials': f'{DATA_DIR}technical_officials.csv',
    'torch_route': f'{DATA_DIR}torch_route.csv',
    'venues': f'{DATA_DIR}venues.csv'
}

RESULTS_DIR = f"{DATA_DIR}results/"

# ============================================================================
# OLYMPICS INFO
# ============================================================================

OLYMPICS_START_DATE = "2024-07-26"
OLYMPICS_END_DATE = "2024-08-11"
OLYMPICS_LOCATION = "Paris, France"
OLYMPICS_YEAR = 2024

# ============================================================================
# FILTER OPTIONS
# ============================================================================

MEDAL_TYPES = ['Gold', 'Silver', 'Bronze']

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Chart height defaults
CHART_HEIGHT = {
    'small': 300,
    'medium': 500,
    'large': 700
}

# Plotly layout template
PLOTLY_TEMPLATE = 'plotly_white'

# Map settings
MAP_SETTINGS = {
    'mapbox_style': 'carto-positron',
    'zoom': 1,
    'center': {'lat': 48.8566, 'lon': 2.3522}  # Paris coordinates
}

# ============================================================================
# UI TEXT
# ============================================================================

WELCOME_TEXT = """
Welcome to the **Paris 2024 Olympics Dashboard**! 🏅

This interactive dashboard provides comprehensive insights into the Paris 2024 Olympic Games.
Explore athlete performances, medal distributions, global trends, and event schedules.

Use the **sidebar filters** to customize your view and discover insights!
"""

PAGE_DESCRIPTIONS = {
    'overview': "High-level summary of the Olympic Games with key performance indicators",
    'global': "Geographical and hierarchical analysis of medal distributions by continent and country",
    'athlete': "Detailed athlete profiles, demographics, and performance metrics",
    'sports': "Event schedules, sport-specific analysis, and venue locations",
    'advanced': "Advanced analytics including daily highlights and gender-based insights",
    'comparison': "Head-to-head country comparison tool with multiple metrics"
}

# ============================================================================
# CONTINENT MAPPING
# ============================================================================

CONTINENT_MAP = {
    # Europe
    'ALB': 'Europe', 'AND': 'Europe', 'ARM': 'Europe', 'AUT': 'Europe',
    'AZE': 'Europe', 'BLR': 'Europe', 'BEL': 'Europe', 'BIH': 'Europe',
    'BUL': 'Europe', 'CRO': 'Europe', 'CYP': 'Europe', 'CZE': 'Europe',
    'DEN': 'Europe', 'ESP': 'Europe', 'EST': 'Europe', 'FIN': 'Europe',
    'FRA': 'Europe', 'GBR': 'Europe', 'GEO': 'Europe', 'GER': 'Europe',
    'GRE': 'Europe', 'HUN': 'Europe', 'IRL': 'Europe', 'ISL': 'Europe',
    'ISR': 'Europe', 'ITA': 'Europe', 'KOS': 'Europe', 'LAT': 'Europe',
    'LIE': 'Europe', 'LTU': 'Europe', 'LUX': 'Europe', 'MDA': 'Europe',
    'MKD': 'Europe', 'MLT': 'Europe', 'MON': 'Europe', 'MNE': 'Europe',
    'NED': 'Europe', 'NOR': 'Europe', 'POL': 'Europe', 'POR': 'Europe',
    'ROU': 'Europe', 'RSA': 'Europe', 'RUS': 'Europe', 'SRB': 'Europe',
    'SVK': 'Europe', 'SLO': 'Europe', 'SMR': 'Europe', 'SUI': 'Europe',
    'SWE': 'Europe', 'TUR': 'Europe', 'UKR': 'Europe',
    
    # Asia
    'AFG': 'Asia', 'BAN': 'Asia', 'BRN': 'Asia', 'BHU': 'Asia',
    'BRU': 'Asia', 'CAM': 'Asia', 'CHN': 'Asia', 'TPE': 'Asia',
    'HKG': 'Asia', 'IND': 'Asia', 'INA': 'Asia', 'IRI': 'Asia',
    'IRQ': 'Asia', 'JOR': 'Asia', 'JPN': 'Asia', 'KAZ': 'Asia',
    'KGZ': 'Asia', 'KOR': 'Asia', 'KSA': 'Asia', 'KUW': 'Asia',
    'LAO': 'Asia', 'LBN': 'Asia', 'MAS': 'Asia', 'MDV': 'Asia',
    'MGL': 'Asia', 'MYA': 'Asia', 'NEP': 'Asia', 'OMA': 'Asia',
    'PAK': 'Asia', 'PLE': 'Asia', 'PHI': 'Asia', 'PRK': 'Asia',
    'QAT': 'Asia', 'SGP': 'Asia', 'SRI': 'Asia', 'SYR': 'Asia',
    'TJK': 'Asia', 'THA': 'Asia', 'TLS': 'Asia', 'TKM': 'Asia',
    'UAE': 'Asia', 'UZB': 'Asia', 'VIE': 'Asia', 'YEM': 'Asia',
    
    # Africa
    'ALG': 'Africa', 'ANG': 'Africa', 'BEN': 'Africa', 'BOT': 'Africa',
    'BUR': 'Africa', 'BDI': 'Africa', 'CMR': 'Africa', 'CPV': 'Africa',
    'CAF': 'Africa', 'CHA': 'Africa', 'CGO': 'Africa', 'COM': 'Africa',
    'CIV': 'Africa', 'COD': 'Africa', 'DJI': 'Africa', 'EGY': 'Africa',
    'GEQ': 'Africa', 'ERI': 'Africa', 'ETH': 'Africa', 'GAB': 'Africa',
    'GAM': 'Africa', 'GHA': 'Africa', 'GUI': 'Africa', 'GBS': 'Africa',
    'KEN': 'Africa', 'LES': 'Africa', 'LBR': 'Africa', 'LBA': 'Africa',
    'MAD': 'Africa', 'MAW': 'Africa', 'MLI': 'Africa', 'MRI': 'Africa',
    'MTN': 'Africa', 'MAR': 'Africa', 'MOZ': 'Africa', 'NAM': 'Africa',
    'NIG': 'Africa', 'NGR': 'Africa', 'RWA': 'Africa', 'STP': 'Africa',
    'SEN': 'Africa', 'SEY': 'Africa', 'SLE': 'Africa', 'SOM': 'Africa',
    'RSA': 'Africa', 'SSD': 'Africa', 'SUD': 'Africa', 'TAN': 'Africa',
    'TOG': 'Africa', 'TUN': 'Africa', 'UGA': 'Africa', 'ZAM': 'Africa',
    'ZIM': 'Africa',
    
    # North America
    'ANT': 'North America', 'ARU': 'North America', 'BAH': 'North America',
    'BAR': 'North America', 'BIZ': 'North America', 'BER': 'North America',
    'CAN': 'North America', 'CAY': 'North America', 'CRC': 'North America',
    'CUB': 'North America', 'DMA': 'North America', 'DOM': 'North America',
    'ESA': 'North America', 'GRN': 'North America', 'GUA': 'North America',
    'HAI': 'North America', 'HON': 'North America', 'JAM': 'North America',
    'MEX': 'North America', 'NCA': 'North America', 'PAN': 'North America',
    'PUR': 'North America', 'SKN': 'North America', 'LCA': 'North America',
    'VIN': 'North America', 'TTO': 'North America', 'USA': 'North America',
    'ISV': 'North America',
    
    # South America
    'ARG': 'South America', 'BOL': 'South America', 'BRA': 'South America',
    'CHI': 'South America', 'COL': 'South America', 'ECU': 'South America',
    'GUY': 'South America', 'PAR': 'South America', 'PER': 'South America',
    'SUR': 'South America', 'URU': 'South America', 'VEN': 'South America',
    
    # Oceania
    'ASA': 'Oceania', 'AUS': 'Oceania', 'COK': 'Oceania', 'FIJ': 'Oceania',
    'GUM': 'Oceania', 'KIR': 'Oceania', 'MHL': 'Oceania', 'FSM': 'Oceania',
    'NRU': 'Oceania', 'NZL': 'Oceania', 'PLW': 'Oceania', 'PNG': 'Oceania',
    'SAM': 'Oceania', 'SOL': 'Oceania', 'TGA': 'Oceania', 'TUV': 'Oceania',
    'VAN': 'Oceania'
}

# ============================================================================
# COUNTRY FLAG EMOJIS (Sample - add more as needed)
# ============================================================================

FLAG_EMOJI = {
    'USA': '🇺🇸', 'CHN': '🇨🇳', 'JPN': '🇯🇵', 'GBR': '🇬🇧',
    'FRA': '🇫🇷', 'AUS': '🇦🇺', 'ITA': '🇮🇹', 'GER': '🇩🇪',
    'CAN': '🇨🇦', 'BRA': '🇧🇷', 'ESP': '🇪🇸', 'KOR': '🇰🇷',
    'NED': '🇳🇱', 'NZL': '🇳🇿', 'CUB': '🇨🇺', 'HUN': '🇭🇺',
    'ROU': '🇷🇴', 'POL': '🇵🇱', 'SWE': '🇸🇪', 'NOR': '🇳🇴',
    'UKR': '🇺🇦', 'BEL': '🇧🇪', 'GRE': '🇬🇷', 'KAZ': '🇰🇿',
    'DEN': '🇩🇰', 'CRO': '🇭🇷', 'SUI': '🇨🇭', 'IRI': '🇮🇷',
    'SRB': '🇷🇸', 'CZE': '🇨🇿', 'RSA': '🇿🇦', 'KEN': '🇰🇪',
    'JAM': '🇯🇲', 'ETH': '🇪🇹', 'IND': '🇮🇳', 'MEX': '🇲🇽',
    'ARG': '🇦🇷', 'TUR': '🇹🇷', 'EGY': '🇪🇬', 'NGR': '🇳🇬',
}

# ============================================================================
# CONSTANTS
# ============================================================================

TOP_N_COUNTRIES = 10
TOP_N_ATHLETES = 10
TOP_N_SPORTS = 20

# Cache TTL (seconds)
CACHE_TTL = 3600  # 1 hour