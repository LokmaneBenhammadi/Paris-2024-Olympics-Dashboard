"""
Data Processor Utility
Data cleaning, transformation, and aggregation functions for Paris 2024 Olympics Dashboard
"""

import pandas as pd
import numpy as np
from utils.continent_mapper import add_continent_column


def clean_athlete_data(df):
    """
    Clean and standardize athlete data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Raw athlete data
    
    Returns:
    --------
    pandas.DataFrame : Cleaned athlete data
    """
    df = df.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    if 'birth_date' in df.columns:
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    
    # Standardize gender values
    if 'gender' in df.columns:
        df['gender'] = df['gender'].str.strip().str.title()
    
    # Calculate age if birth_date exists
    if 'birth_date' in df.columns:
        olympics_date = pd.Timestamp('2024-07-26')
        df['age'] = (olympics_date - df['birth_date']).dt.days // 365
    
    return df


def merge_with_nocs(df, nocs_df, country_col='country_code'):
    """
    Merge data with NOC information to get full country names.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to merge
    nocs_df : pandas.DataFrame
        NOCs reference data
    country_col : str
        Name of the country code column in df
    
    Returns:
    --------
    pandas.DataFrame : Merged data with country information
    """
    if nocs_df.empty:
        return df
    
    # Determine NOC column name in nocs_df
    noc_col = 'code' if 'code' in nocs_df.columns else 'country_code'
    
    if noc_col not in nocs_df.columns:
        return df
    
    # Merge
    df = df.copy()
    merged = df.merge(
        nocs_df[[noc_col, 'country']] if 'country' in nocs_df.columns else nocs_df,
        left_on=country_col,
        right_on=noc_col,
        how='left'
    )
    
    return merged


def normalize_medal_columns(df):
    """
    Normalize medal column names to standard format.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with medal columns
    
    Returns:
    --------
    pandas.DataFrame : DataFrame with normalized column names
    """
    df = df.copy()
    
    # Create a mapping of possible column names to standard names
    column_mapping = {}
    
    for col in df.columns:
        col_lower = col.lower().strip()
        
        # Check for exact matches first
        if col_lower == 'total':
            column_mapping[col] = 'Total'
        # Then check for medal types
        elif 'gold' in col_lower and 'Gold' not in column_mapping.values():
            column_mapping[col] = 'Gold'
        elif 'silver' in col_lower and 'Silver' not in column_mapping.values():
            column_mapping[col] = 'Silver'
        elif 'bronze' in col_lower and 'Bronze' not in column_mapping.values():
            column_mapping[col] = 'Bronze'
        # Country columns - be more specific
        elif col in ['country_code', 'code', 'noc', 'NOC'] or (col_lower == 'code'):
            column_mapping[col] = 'country_code'
        elif col == 'country' or col_lower == 'country':
            column_mapping[col] = 'country'
    
    df = df.rename(columns=column_mapping)
    
    # If Total doesn't exist but Gold, Silver, Bronze do, calculate it
    if 'Total' not in df.columns and all(col in df.columns for col in ['Gold', 'Silver', 'Bronze']):
        df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
    
    # Sort by Total descending if Total column exists
    if 'Total' in df.columns:
        df = df.sort_values('Total', ascending=False).reset_index(drop=True)
    
    return df


def add_continent_to_dataframe(df, country_col=None):
    """
    Add continent information to dataframe.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to process
    country_col : str or None
        Name of the country code column
    
    Returns:
    --------
    pandas.DataFrame : Data with continent column added
    """
    if df is None or df.empty:
        return df
    
    # First normalize column names
    df = normalize_medal_columns(df)
    
    # Auto-detect country code column if not specified
    if country_col is None:
        if 'country_code' in df.columns:
            country_col = 'country_code'
        else:
            for col in ['code', 'noc', 'NOC', 'Country Code']:
                if col in df.columns:
                    country_col = col
                    break
    
    if country_col:
        return add_continent_column(df, country_col)
    
    return df


def calculate_medal_counts(df, group_by='country_code'):
    """
    Calculate medal counts grouped by specified column.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medal data
    group_by : str or list
        Column(s) to group by
    
    Returns:
    --------
    pandas.DataFrame : Aggregated medal counts
    """
    if df.empty:
        return pd.DataFrame()
    
    # Check if medal type column exists
    medal_col = None
    for col in ['medal_type', 'medal', 'Medal']:
        if col in df.columns:
            medal_col = col
            break
    
    if medal_col is None:
        return pd.DataFrame()
    
    # Count medals by type
    medal_counts = df.groupby([group_by, medal_col]).size().unstack(fill_value=0)
    
    # Ensure all medal types exist
    for medal_type in ['Gold', 'Silver', 'Bronze']:
        if medal_type not in medal_counts.columns:
            medal_counts[medal_type] = 0
    
    # Calculate total
    medal_counts['Total'] = medal_counts[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    
    # Sort by total medals
    medal_counts = medal_counts.sort_values('Total', ascending=False).reset_index()
    
    return medal_counts


def get_top_countries(df, n=10, medal_col='Total'):
    """
    Get top N countries by medal count.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medal data with country information
    n : int
        Number of top countries to return
    medal_col : str
        Column to sort by (default: 'Total')
    
    Returns:
    --------
    pandas.DataFrame : Top N countries
    """
    if df.empty or medal_col not in df.columns:
        return pd.DataFrame()
    
    return df.nlargest(n, medal_col)


def filter_by_country(df, countries, country_col='country_code'):
    """
    Filter data by country or list of countries.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to filter
    countries : str or list
        Country code(s) to filter by
    country_col : str
        Name of the country column
    
    Returns:
    --------
    pandas.DataFrame : Filtered data
    """
    if df.empty:
        return df
    
    if isinstance(countries, str):
        countries = [countries]
    
    return df[df[country_col].isin(countries)]


def filter_by_sport(df, sports, sport_col='sport'):
    """
    Filter data by sport or list of sports.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to filter
    sports : str or list
        Sport name(s) to filter by
    sport_col : str
        Name of the sport column
    
    Returns:
    --------
    pandas.DataFrame : Filtered data
    """
    if df.empty:
        return df
    
    if isinstance(sports, str):
        sports = [sports]
    
    return df[df[sport_col].isin(sports)]


def filter_by_gender(df, gender, gender_col='gender'):
    """
    Filter data by gender.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to filter
    gender : str
        Gender to filter by ('Male', 'Female', or 'Mixed')
    gender_col : str
        Name of the gender column
    
    Returns:
    --------
    pandas.DataFrame : Filtered data
    """
    if df.empty or gender_col not in df.columns:
        return df
    
    return df[df[gender_col].str.strip().str.title() == gender]


def get_age_statistics(df, group_by=None):
    """
    Calculate age statistics from athlete data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Athlete data with age column
    group_by : str or None
        Column to group statistics by (e.g., 'sport', 'country_code')
    
    Returns:
    --------
    pandas.DataFrame : Age statistics
    """
    if df.empty or 'age' not in df.columns:
        return pd.DataFrame()
    
    # Remove invalid ages
    df_clean = df[df['age'].notna() & (df['age'] > 0) & (df['age'] < 100)]
    
    if group_by:
        stats = df_clean.groupby(group_by)['age'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('min', 'min'),
            ('max', 'max'),
            ('std', 'std')
        ]).reset_index()
    else:
        stats = pd.DataFrame({
            'count': [df_clean['age'].count()],
            'mean': [df_clean['age'].mean()],
            'median': [df_clean['age'].median()],
            'min': [df_clean['age'].min()],
            'max': [df_clean['age'].max()],
            'std': [df_clean['age'].std()]
        })
    
    return stats


def get_gender_distribution(df, group_by=None, gender_col='gender'):
    """
    Calculate gender distribution.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with gender information
    group_by : str or None
        Column to group by
    gender_col : str
        Name of the gender column
    
    Returns:
    --------
    pandas.DataFrame : Gender distribution counts
    """
    if df.empty or gender_col not in df.columns:
        return pd.DataFrame()
    
    if group_by:
        gender_dist = df.groupby([group_by, gender_col]).size().unstack(fill_value=0)
    else:
        gender_dist = df[gender_col].value_counts().to_frame('count')
    
    return gender_dist


def calculate_medal_efficiency(df, athletes_df):
    """
    Calculate medals per athlete ratio by country.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medal data
    athletes_df : pandas.DataFrame
        Athlete data
    
    Returns:
    --------
    pandas.DataFrame : Medal efficiency metrics
    """
    if df.empty or athletes_df.empty:
        return pd.DataFrame()
    
    # Count athletes per country
    country_col = 'country_code' if 'country_code' in athletes_df.columns else 'code'
    athletes_per_country = athletes_df.groupby(country_col).size().reset_index(name='athlete_count')
    
    # Count medals per country
    medal_col = 'country_code' if 'country_code' in df.columns else 'code'
    medals_per_country = df.groupby(medal_col).size().reset_index(name='medal_count')
    
    # Merge and calculate efficiency
    efficiency = athletes_per_country.merge(medals_per_country, on=country_col, how='left')
    efficiency['medal_count'] = efficiency['medal_count'].fillna(0)
    efficiency['efficiency'] = efficiency['medal_count'] / efficiency['athlete_count']
    efficiency = efficiency.sort_values('efficiency', ascending=False)
    
    return efficiency


def aggregate_by_sport(df, value_cols=None):
    """
    Aggregate data by sport.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to aggregate
    value_cols : list or None
        Columns to aggregate (if None, counts rows)
    
    Returns:
    --------
    pandas.DataFrame : Aggregated data by sport
    """
    if df.empty:
        return pd.DataFrame()
    
    sport_col = 'sport' if 'sport' in df.columns else 'Sport'
    
    if sport_col not in df.columns:
        return pd.DataFrame()
    
    if value_cols:
        return df.groupby(sport_col)[value_cols].sum().reset_index()
    else:
        return df.groupby(sport_col).size().reset_index(name='count')


def get_medal_timeline(df, date_col='date'):
    """
    Create medal timeline (cumulative medals over time).
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medal data with date information
    date_col : str
        Name of the date column
    
    Returns:
    --------
    pandas.DataFrame : Cumulative medal counts by date
    """
    if df.empty or date_col not in df.columns:
        return pd.DataFrame()
    
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # Count medals by date
    daily_medals = df.groupby(date_col).size().reset_index(name='daily_count')
    daily_medals = daily_medals.sort_values(date_col)
    daily_medals['cumulative_count'] = daily_medals['daily_count'].cumsum()
    
    return daily_medals


def pivot_medals_by_country_sport(df):
    """
    Create pivot table of medals by country and sport.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medal data with country and sport columns
    
    Returns:
    --------
    pandas.DataFrame : Pivot table
    """
    if df.empty:
        return pd.DataFrame()
    
    country_col = 'country_code' if 'country_code' in df.columns else 'country'
    sport_col = 'sport' if 'sport' in df.columns else 'Sport'
    
    if country_col not in df.columns or sport_col not in df.columns:
        return pd.DataFrame()
    
    pivot = pd.pivot_table(
        df,
        values='medal_type' if 'medal_type' in df.columns else None,
        index=country_col,
        columns=sport_col,
        aggfunc='count',
        fill_value=0
    )
    
    return pivot


def get_top_athletes(df, n=10, country_col='country_code'):
    """
    Get top athletes by medal count.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Medallist data
    n : int
        Number of top athletes to return
    country_col : str
        Country column name
    
    Returns:
    --------
    pandas.DataFrame : Top athletes with medal counts
    """
    if df.empty:
        return pd.DataFrame()
    
    # Find athlete name column
    name_col = None
    for col in ['name', 'athlete_name', 'athlete']:
        if col in df.columns:
            name_col = col
            break
    
    if name_col is None:
        return pd.DataFrame()
    
    # Count medals per athlete
    athlete_medals = df.groupby([name_col, country_col]).size().reset_index(name='medal_count')
    athlete_medals = athlete_medals.sort_values('medal_count', ascending=False).head(n)
    
    # Add medal breakdown if available
    if 'medal_type' in df.columns:
        medal_breakdown = df.groupby([name_col, country_col, 'medal_type']).size().unstack(fill_value=0)
        athlete_medals = athlete_medals.merge(medal_breakdown, on=[name_col, country_col], how='left')
    
    return athlete_medals


def normalize_column_names(df):
    """
    Normalize column names (lowercase, replace spaces with underscores).
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to normalize
    
    Returns:
    --------
    pandas.DataFrame : DataFrame with normalized column names
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def handle_missing_values(df, strategy='drop', fill_value=None):
    """
    Handle missing values in DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to process
    strategy : str
        Strategy to handle missing values ('drop', 'fill', 'forward', 'backward')
    fill_value : any
        Value to fill missing data with (if strategy='fill')
    
    Returns:
    --------
    pandas.DataFrame : Processed data
    """
    df = df.copy()
    
    if strategy == 'drop':
        return df.dropna()
    elif strategy == 'fill' and fill_value is not None:
        return df.fillna(fill_value)
    elif strategy == 'forward':
        return df.fillna(method='ffill')
    elif strategy == 'backward':
        return df.fillna(method='bfill')
    else:
        return df