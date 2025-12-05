"""
Filters Utility
Global sidebar filter creation and application for Paris 2024 Olympics Dashboard
"""

import streamlit as st
import pandas as pd
from utils.continent_mapper import get_all_continents, add_continent_column
from config.config import MEDAL_TYPES


def create_sidebar_filters(athletes_df=None, medals_df=None, events_df=None, show_sport=True):
    """
    Create global sidebar filters for the dashboard.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athletes data (optional, for dynamic filter options)
    medals_df : pandas.DataFrame
        Medals data (optional, for dynamic filter options)
    events_df : pandas.DataFrame
        Events data (optional, for dynamic filter options)
    show_sport : bool
        Whether to render the sport selector (default: True)
    
    Returns:
    --------
    dict : Dictionary containing selected filter values
    """
    st.sidebar.header("🎯 Filters")
    st.sidebar.markdown("---")
    
    # Initialize reset counter in session state
    if 'filter_reset_counter' not in st.session_state:
        st.session_state.filter_reset_counter = 0
    
    # Use counter to create unique keys that change on reset
    key_suffix = f"_{st.session_state.filter_reset_counter}"
    
    filters = {}
    
    # Continent filter (first - to enable country dependency)
    st.sidebar.subheader("🗺️ Continent")
    continents = get_all_continents()
    
    continents_raw = st.sidebar.multiselect(
        "Select Continents",
        options=["All"] + continents,
        default=["All"],
        help="Filter by continent (select first, then countries)",
        key=f'continent_filter{key_suffix}'
    )
    
    # Auto-remove "All" when specific selection is made
    if "All" in continents_raw and len(continents_raw) > 1:
        continents_raw = [c for c in continents_raw if c != "All"]
    
    # If nothing selected, default to "All"
    if not continents_raw:
        continents_raw = ["All"]
    
    filters['continents'] = continents_raw
    
    # Country filter (dependent on continent)
    st.sidebar.subheader("🌍 Country")
    if medals_df is not None and not medals_df.empty:
        # Ensure continent column exists
        if 'continent' not in medals_df.columns:
            medals_df = add_continent_column(medals_df, 'country_code')
        
        # Filter countries based on selected continents
        if "All" not in filters['continents'] and 'continent' in medals_df.columns:
            filtered_medals = medals_df[medals_df['continent'].isin(filters['continents'])]
        else:
            filtered_medals = medals_df
        
        country_col = 'country' if 'country' in filtered_medals.columns else 'country_code'
        countries = sorted(filtered_medals[country_col].dropna().unique())
        
        countries_raw = st.sidebar.multiselect(
            "Select Countries",
            options=["All"] + list(countries),
            default=["All"],
            help="Filter by one or more countries",
            key=f'country_filter{key_suffix}'
        )
        
        # Auto-remove "All" when specific selection is made
        if "All" in countries_raw and len(countries_raw) > 1:
            countries_raw = [c for c in countries_raw if c != "All"]
        
        # If nothing selected, default to "All"
        if not countries_raw:
            countries_raw = ["All"]
        
        filters['countries'] = countries_raw
    else:
        filters['countries'] = ["All"]
    
    # Sport filter (optional)
    if show_sport:
        st.sidebar.subheader("🏅 Sport")
        if events_df is not None and not events_df.empty:
            sport_col = 'sport' if 'sport' in events_df.columns else 'Sport'
            sports = sorted(events_df[sport_col].dropna().unique())
            sports_raw = st.sidebar.multiselect(
                "Select Sports",
                options=["All"] + list(sports),
                default=["All"],
                help="Filter by sport",
                key=f'sport_filter{key_suffix}'
            )
            
            # Auto-remove "All" when specific selection is made
            if "All" in sports_raw and len(sports_raw) > 1:
                sports_raw = [s for s in sports_raw if s != "All"]
            
            # If nothing selected, default to "All"
            if not sports_raw:
                sports_raw = ["All"]
            
            filters['sports'] = sports_raw
        elif medals_df is not None and not medals_df.empty:
            sport_cols = ['sport', 'Sport', 'discipline', 'Discipline']
            sport_col = next((col for col in sport_cols if col in medals_df.columns), None)
            if sport_col:
                sports = sorted(medals_df[sport_col].dropna().unique())
                sports_raw = st.sidebar.multiselect(
                    "Select Sports",
                    options=["All"] + list(sports),
                    default=["All"],
                    help="Filter by sport",
                    key=f'sport_filter{key_suffix}'
                )
                
                # Auto-remove "All" when specific selection is made
                if "All" in sports_raw and len(sports_raw) > 1:
                    sports_raw = [s for s in sports_raw if s != "All"]
                
                # If nothing selected, default to "All"
                if not sports_raw:
                    sports_raw = ["All"]
                
                filters['sports'] = sports_raw
            else:
                filters['sports'] = ["All"]
        else:
            filters['sports'] = ["All"]
    else:
        filters['sports'] = ["All"]
    
    # Medal Type filter (checkboxes instead - more intuitive)
    st.sidebar.subheader("🏆 Medal Types")
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        show_gold = st.checkbox("🥇", value=True, key=f'gold_cb{key_suffix}')
    with col2:
        show_silver = st.checkbox("🥈", value=True, key=f'silver_cb{key_suffix}')
    with col3:
        show_bronze = st.checkbox("🥉", value=True, key=f'bronze_cb{key_suffix}')
    
    # Store in filters
    filters['medal_types'] = []
    if show_gold:
        filters['medal_types'].append('Gold')
    if show_silver:
        filters['medal_types'].append('Silver')
    if show_bronze:
        filters['medal_types'].append('Bronze')
    
    # Gender filter
    st.sidebar.subheader("⚥ Gender")
    filters['gender'] = st.sidebar.radio(
        "Select Gender",
        options=["All", "Male", "Female", "Mixed"],
        index=0,
        help="Filter by gender",
        key=f'gender_filter{key_suffix}'
    )
    
    # Age range filter (if athlete data available)
    if athletes_df is not None and not athletes_df.empty and 'age' in athletes_df.columns:
        st.sidebar.subheader("📅 Age Range")
        age_data = athletes_df['age'].dropna()
        if len(age_data) > 0:
            min_age = int(age_data.min())
            max_age = int(age_data.max())
            filters['age_range'] = st.sidebar.slider(
                "Select Age Range",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
                help="Filter by athlete age",
                key=f'age_filter{key_suffix}'
            )
        else:
            filters['age_range'] = None
    else:
        filters['age_range'] = None
    
    st.sidebar.markdown("---")
    
    # Reset filters button
    if st.sidebar.button("🔄 Reset All Filters", key='reset_btn'):
        # Increment the counter to force recreation of all widgets with new keys
        st.session_state.filter_reset_counter += 1
        st.rerun()
    
    return filters


def apply_filters(df, filters, country_col=None, sport_col=None, medal_col=None, gender_col=None):
    """
    Apply selected filters to a DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to filter
    filters : dict
        Dictionary of filter selections from create_sidebar_filters()
    country_col : str
        Name of the country column (auto-detected if None)
    sport_col : str
        Name of the sport column (auto-detected if None)
    medal_col : str
        Name of the medal type column (auto-detected if None)
    gender_col : str
        Name of the gender column (auto-detected if None)
    
    Returns:
    --------
    pandas.DataFrame : Filtered data
    """
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Ensure continent column exists for continent filtering
    if 'continents' in filters and "All" not in filters['continents']:
        if 'continent' not in filtered_df.columns:
            from utils.continent_mapper import add_continent_column
            filtered_df = add_continent_column(filtered_df, 'country_code')
    
    # Auto-detect column names if not provided
    if country_col is None:
        country_col = get_country_column(filtered_df)
    
    if sport_col is None:
        sport_col = get_sport_column(filtered_df)
    
    if medal_col is None:
        medal_col = get_medal_column(filtered_df)
    
    if gender_col is None:
        gender_col = get_gender_column(filtered_df)
    
    # Apply continent filter
    if 'continents' in filters and "All" not in filters['continents'] and 'continent' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['continent'].isin(filters['continents'])]
    
    # Apply country filter
    if 'countries' in filters and "All" not in filters['countries'] and country_col and country_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[country_col].isin(filters['countries'])]
    
    # Apply sport filter
    if 'sports' in filters and "All" not in filters['sports'] and sport_col and sport_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[sport_col].isin(filters['sports'])]
    
    # Apply medal type filter (for aggregated data with Gold, Silver, Bronze columns)
    if 'medal_types' in filters and len(filters['medal_types']) > 0:
        # Check if we have Gold, Silver, Bronze columns (medals_total style)
        if all(col in filtered_df.columns for col in ['Gold', 'Silver', 'Bronze']):
            # For aggregated medal data, filter out rows where all selected medal types are 0
            medal_cols = filters['medal_types']
            if medal_cols:
                # Keep rows where at least one selected medal type > 0
                mask = filtered_df[medal_cols].sum(axis=1) > 0
                filtered_df = filtered_df[mask]
                # For individual medal records with medal_type column
  # For individual medal records with medal_type column
        elif medal_col and medal_col in filtered_df.columns:
            # Convert filter values to match data format (handles both "Gold" and "Gold Medal")
            medal_types_with_suffix = [f"{m} Medal" for m in filters['medal_types']]
            # Check if data uses "Medal" suffix
            if not filtered_df.empty and filtered_df[medal_col].astype(str).str.contains(' Medal', na=False).any():
                filtered_df = filtered_df[filtered_df[medal_col].isin(medal_types_with_suffix)]
            else:
                filtered_df = filtered_df[filtered_df[medal_col].isin(filters['medal_types'])]
    
    # Apply gender filter
    if 'gender' in filters and filters['gender'] != "All" and gender_col and gender_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[gender_col].str.strip().str.title() == filters['gender']]
    
    # Apply age range filter
    if 'age_range' in filters and filters['age_range'] is not None and 'age' in filtered_df.columns:
        min_age, max_age = filters['age_range']
        filtered_df = filtered_df[
            (filtered_df['age'] >= min_age) & (filtered_df['age'] <= max_age)
        ]
    
    return filtered_df


def get_country_column(df):
    """
    Auto-detect the country column name.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to check
    
    Returns:
    --------
    str or None : Name of the country column
    """
    possible_names = ['country', 'country_code', 'code', 'noc', 'NOC', 'Country']
    for col in possible_names:
        if col in df.columns:
            return col
    return None


def get_sport_column(df):
    """
    Auto-detect the sport column name.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to check
    
    Returns:
    --------
    str or None : Name of the sport column
    """
    possible_names = ['sport', 'Sport', 'discipline', 'Discipline']
    for col in possible_names:
        if col in df.columns:
            return col
    return None


def get_medal_column(df):
    """
    Auto-detect the medal type column name.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to check
    
    Returns:
    --------
    str or None : Name of the medal column
    """
    possible_names = ['medal_type', 'medal', 'Medal', 'medal_code']
    for col in possible_names:
        if col in df.columns:
            return col
    return None


def get_gender_column(df):
    """
    Auto-detect the gender column name.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to check
    
    Returns:
    --------
    str or None : Name of the gender column
    """
    possible_names = ['gender', 'Gender', 'sex', 'Sex']
    for col in possible_names:
        if col in df.columns:
            return col
    return None


def show_filter_summary(filters, filtered_df=None, original_df=None):
    """
    Display a summary of applied filters.
    
    Parameters:
    -----------
    filters : dict
        Dictionary of filter selections
    filtered_df : pandas.DataFrame
        Filtered DataFrame (optional)
    original_df : pandas.DataFrame
        Original DataFrame before filtering (optional)
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Active Filters")
    
    active_filters = []
    
    if 'continents' in filters and "All" not in filters['continents']:
        active_filters.append(f"🗺️ {len(filters['continents'])} Continents")
    
    if 'countries' in filters and "All" not in filters['countries']:
        active_filters.append(f"🌍 {len(filters['countries'])} Countries")
    
    if 'sports' in filters and "All" not in filters['sports']:
        active_filters.append(f"🏅 {len(filters['sports'])} Sports")
    
    if 'medal_types' in filters and len(filters['medal_types']) < 3:
        active_filters.append(f"🏆 {', '.join(filters['medal_types'])}")
    
    if 'gender' in filters and filters['gender'] != "All":
        active_filters.append(f"⚥ {filters['gender']}")
    
    if 'age_range' in filters and filters['age_range'] is not None:
        min_age, max_age = filters['age_range']
        active_filters.append(f"📅 Age {min_age}-{max_age}")
    
    if active_filters:
        for filter_text in active_filters:
            st.sidebar.markdown(f"✓ {filter_text}")
    else:
        st.sidebar.info("No filters applied")
    
    # Show data reduction summary
    if filtered_df is not None and original_df is not None:
        reduction = len(filtered_df)
        total = len(original_df)
        percentage = (reduction / total * 100) if total > 0 else 0
        st.sidebar.metric(
            "Data Shown",
            f"{reduction:,} / {total:,}",
            f"{percentage:.1f}%"
        )


def get_filter_statistics(filters, df):
    """
    Get statistics about filter selections.
    """
    stats = {}
    
    country_col = get_country_column(df)
    if country_col:
        stats['unique_countries'] = df[country_col].nunique()
    
    sport_col = get_sport_column(df)
    if sport_col:
        stats['unique_sports'] = df[sport_col].nunique()
    
    return stats


def has_active_filters(filters):
    """Check if any filters are active."""
    active = False
    
    if 'continents' in filters and "All" not in filters['continents']:
        active = True
    if 'countries' in filters and "All" not in filters['countries']:
        active = True
    if 'sports' in filters and "All" not in filters['sports']:
        active = True
    if 'medal_types' in filters and len(filters['medal_types']) < 3:
        active = True
    if 'gender' in filters and filters['gender'] != "All":
        active = True
    
    return active