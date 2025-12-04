"""
Metrics Utility
KPI calculations and metric functions for Paris 2024 Olympics Dashboard
"""

import pandas as pd
import numpy as np


def calculate_total_athletes(athletes_df, medals_df=None, filters=None):
    """
    Calculate total number of athletes based on filters.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athletes data
    medals_df : pandas.DataFrame
        Medals data (for medal type and sport filtering)
    filters : dict
        Active filters (for medal_types and sports)
    
    Returns:
    --------
    int : Total number of athletes
    """
    if athletes_df is None or athletes_df.empty:
        return 0
    
    # If we need to filter by medal or sport, use medals_df
    if filters and medals_df is not None and not medals_df.empty:
        needs_medal_filter = 'medal_types' in filters and len(filters.get('medal_types', [])) < 3
        needs_sport_filter = 'sports' in filters and "All" not in filters.get('sports', ["All"])
        
        if needs_medal_filter or needs_sport_filter:
            # Get athlete codes from filtered medals
            filtered_medals = medals_df.copy()
            
            # Apply medal type filter
            if needs_medal_filter and 'medal_type' in filtered_medals.columns:
                filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(filters['medal_types'])]
            
            # Apply sport filter
            if needs_sport_filter:
                sport_col = None
                for col in ['sport', 'Sport', 'discipline', 'Discipline']:
                    if col in filtered_medals.columns:
                        sport_col = col
                        break
                if sport_col:
                    filtered_medals = filtered_medals[filtered_medals[sport_col].isin(filters['sports'])]
            
            # Get unique athlete codes from filtered medals
            athlete_col = None
            for col in ['code', 'athlete_code', 'Code', 'Athlete Code']:
                if col in filtered_medals.columns:
                    athlete_col = col
                    break
            
            if athlete_col:
                valid_athlete_codes = filtered_medals[athlete_col].unique()
                # Find matching column in athletes_df
                athlete_match_col = None
                for col in ['code', 'athlete_code', 'Code', 'Athlete Code']:
                    if col in athletes_df.columns:
                        athlete_match_col = col
                        break
                
                if athlete_match_col:
                    return athletes_df[athletes_df[athlete_match_col].isin(valid_athlete_codes)].shape[0]
    
    return len(athletes_df)


def calculate_total_countries(medals_df=None, events_df=None, filters=None):
    """
    Calculate total number of participating countries.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Medals data (preferred for sport/gender filtering)
    events_df : pandas.DataFrame
        Events data (alternative source)
    filters : dict
        Active filters
    
    Returns:
    --------
    int : Number of unique countries
    """
    # Prefer medals_df as it has sport column
    df = medals_df if medals_df is not None and not medals_df.empty else events_df
    
    if df is None or df.empty:
        return 0
    
    # Apply sport filter if needed
    if filters and 'sports' in filters and "All" not in filters.get('sports', ["All"]):
        sport_col = None
        for col in ['sport', 'Sport', 'discipline', 'Discipline']:
            if col in df.columns:
                sport_col = col
                break
        if sport_col:
            df = df[df[sport_col].isin(filters['sports'])]
    
    # Apply gender filter if needed
    if filters and 'gender' in filters and filters.get('gender') != "All":
        gender_col = None
        for col in ['gender', 'Gender', 'sex', 'Sex']:
            if col in df.columns:
                gender_col = col
                break
        if gender_col:
            df = df[df[gender_col].str.strip().str.title() == filters['gender']]
    
    # Get country column
    country_col = None
    for col in ['country_code', 'code', 'country', 'noc', 'NOC', 'Country', 'Country Code']:
        if col in df.columns:
            country_col = col
            break
    
    if country_col is None:
        return 0
    
    return df[country_col].nunique()


def calculate_total_sports(events_df=None, medals_df=None, filters=None):
    """
    Calculate total number of sports.
    
    Parameters:
    -----------
    events_df : pandas.DataFrame
        Events data with sport column
    medals_df : pandas.DataFrame
        Medals data (for country/gender filtering)
    filters : dict
        Active filters
    
    Returns:
    --------
    int : Number of unique sports
    """
    # Use medals_df if we need country/gender filtering
    needs_filtering = False
    if filters:
        needs_filtering = (
            ('continents' in filters and "All" not in filters.get('continents', ["All"])) or
            ('countries' in filters and "All" not in filters.get('countries', ["All"])) or
            ('gender' in filters and filters.get('gender') != "All")
        )
    
    # If we need filtering by country/gender, use medals_df (has country_code)
    df = medals_df if needs_filtering and medals_df is not None else events_df
    
    if df is None or df.empty:
        return 0
    
    # Apply continent filter if using medals_df
    if needs_filtering and medals_df is not None and df is medals_df:
        if 'continents' in filters and "All" not in filters.get('continents', ["All"]):
            if 'continent' in df.columns:
                df = df[df['continent'].isin(filters['continents'])]
        
        # Apply country filter
        if 'countries' in filters and "All" not in filters.get('countries', ["All"]):
            country_col = None
            for col in ['country_code', 'code', 'country', 'noc']:
                if col in df.columns:
                    country_col = col
                    break
            if country_col:
                df = df[df[country_col].isin(filters['countries'])]
        
        # Apply gender filter
        if 'gender' in filters and filters.get('gender') != "All":
            gender_col = None
            for col in ['gender', 'Gender', 'sex', 'Sex']:
                if col in df.columns:
                    gender_col = col
                    break
            if gender_col:
                df = df[df[gender_col].str.strip().str.title() == filters['gender']]
    
    # Get sport count
    sport_col = None
    for col in ['sport', 'Sport', 'discipline', 'Discipline']:
        if col in df.columns:
            sport_col = col
            break
    
    if sport_col is None:
        return 0
    
    return df[sport_col].nunique()


def calculate_total_medals(medals_df, medals_total_df=None, medal_types=None, filters=None):
    """
    Calculate total number of medals awarded.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Individual medals data (for sport/gender filtering)
    medals_total_df : pandas.DataFrame
        Aggregated medals data (alternative)
    medal_types : list
        List of medal types to include (e.g., ['Gold', 'Silver', 'Bronze'])
    filters : dict
        Active filters
    
    Returns:
    --------
    int : Total number of medals
    """
    # Use medals_total_df if it's already filtered, otherwise use medals_df
    df = medals_total_df if medals_total_df is not None and not medals_total_df.empty else medals_df
    
    if df is None or df.empty:
        return 0
    
    # Check if we need to filter by sport or gender (requires individual medals data)
    needs_detailed_filter = False
    if filters:
        needs_detailed_filter = (
            ('sports' in filters and "All" not in filters.get('sports', ["All"])) or
            ('gender' in filters and filters.get('gender') != "All")
        )
    
    # Use individual medals_df if detailed filtering needed
    if needs_detailed_filter and medals_df is not None and not medals_df.empty:
        df = medals_df.copy()
        
        # Apply sport filter
        if 'sports' in filters and "All" not in filters.get('sports', ["All"]):
            sport_col = None
            for col in ['sport', 'Sport', 'discipline', 'Discipline']:
                if col in df.columns:
                    sport_col = col
                    break
            if sport_col:
                df = df[df[sport_col].isin(filters['sports'])]
        
        # Apply gender filter
        if 'gender' in filters and filters.get('gender') != "All":
            gender_col = None
            for col in ['gender', 'Gender', 'sex', 'Sex']:
                if col in df.columns:
                    gender_col = col
                    break
            if gender_col:
                df = df[df[gender_col].str.strip().str.title() == filters['gender']]
        
        # Count by medal type
        if 'medal_type' in df.columns:
            if medal_types and len(medal_types) > 0:
                df = df[df['medal_type'].isin(medal_types)]
            return len(df)
    
    # For aggregated data with Gold, Silver, Bronze columns
    if all(col in df.columns for col in ['Gold', 'Silver', 'Bronze']):
        if medal_types and len(medal_types) > 0:
            total = 0
            for medal_type in medal_types:
                if medal_type in df.columns:
                    total += df[medal_type].sum()
            return int(total)
        else:
            return int(df['Gold'].sum() + df['Silver'].sum() + df['Bronze'].sum())
    
    # Try 'Total' column
    for col in ['Total', 'total']:
        if col in df.columns:
            return int(df[col].sum())
    
    # Otherwise count rows
    return len(df)


def calculate_total_events(events_df, medals_df=None, filters=None):
    """
    Calculate total number of events.
    
    Parameters:
    -----------
    events_df : pandas.DataFrame
        Events data
    medals_df : pandas.DataFrame
        Medals data (for country/gender filtering)
    filters : dict
        Active filters
    
    Returns:
    --------
    int : Total number of events
    """
    if events_df is None or events_df.empty:
        return 0
    
    # Check if we need country/gender filtering (requires medals data)
    needs_detailed_filter = False
    if filters:
        needs_detailed_filter = (
            ('continents' in filters and "All" not in filters.get('continents', ["All"])) or
            ('countries' in filters and "All" not in filters.get('countries', ["All"])) or
            ('gender' in filters and filters.get('gender') != "All")
        )
    
    # If we need country/gender filtering, filter by sports that have medals matching criteria
    if needs_detailed_filter and medals_df is not None and not medals_df.empty:
        filtered_medals = medals_df.copy()
        
        # Apply continent filter
        if 'continents' in filters and "All" not in filters.get('continents', ["All"]):
            if 'continent' in filtered_medals.columns:
                filtered_medals = filtered_medals[filtered_medals['continent'].isin(filters['continents'])]
        
        # Apply country filter
        if 'countries' in filters and "All" not in filters.get('countries', ["All"]):
            country_col = None
            for col in ['country_code', 'code', 'country', 'noc']:
                if col in filtered_medals.columns:
                    country_col = col
                    break
            if country_col:
                filtered_medals = filtered_medals[filtered_medals[country_col].isin(filters['countries'])]
        
        # Apply gender filter
        if 'gender' in filters and filters.get('gender') != "All":
            gender_col = None
            for col in ['gender', 'Gender', 'sex', 'Sex']:
                if col in filtered_medals.columns:
                    gender_col = col
                    break
            if gender_col:
                filtered_medals = filtered_medals[filtered_medals[gender_col].str.strip().str.title() == filters['gender']]
        
        # Get unique sports/events from filtered medals
        sport_col = None
        for col in ['sport', 'Sport', 'discipline', 'Discipline']:
            if col in filtered_medals.columns:
                sport_col = col
                break
        
        if sport_col:
            valid_sports = filtered_medals[sport_col].unique()
            # Filter events by these sports
            event_sport_col = None
            for col in ['sport', 'Sport', 'discipline', 'Discipline']:
                if col in events_df.columns:
                    event_sport_col = col
                    break
            
            if event_sport_col:
                events_df = events_df[events_df[event_sport_col].isin(valid_sports)]
    
    return len(events_df)


def calculate_medal_distribution(medals_df):
    """
    Calculate distribution of medals by type.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Medals data
    
    Returns:
    --------
    dict : Medal counts by type (Gold, Silver, Bronze)
    """
    if medals_df is None or medals_df.empty:
        return {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    
    # Try aggregated format (Gold, Silver, Bronze columns)
    if all(col in medals_df.columns for col in ['Gold', 'Silver', 'Bronze']):
        return {
            'Gold': int(medals_df['Gold'].sum()),
            'Silver': int(medals_df['Silver'].sum()),
            'Bronze': int(medals_df['Bronze'].sum())
        }
    
    # Try individual medal format (medal_type column)
    if 'medal_type' in medals_df.columns:
        dist = medals_df['medal_type'].value_counts().to_dict()
        return {
            'Gold': dist.get('Gold', 0),
            'Silver': dist.get('Silver', 0),
            'Bronze': dist.get('Bronze', 0)
        }
    
    return {'Gold': 0, 'Silver': 0, 'Bronze': 0}
