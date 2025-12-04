"""
Continent Mapper Utility
Maps country codes to continents for Paris 2024 Olympics Dashboard
"""

import pandas as pd
from config.config import CONTINENT_MAP, CONTINENT_COLORS

def get_continent(country_code):
    """
    Get continent for a given country code.
    
    Parameters:
    -----------
    country_code : str or any
        Three-letter country code (e.g., 'USA', 'FRA', 'CHN')
    
    Returns:
    --------
    str : Continent name or 'Unknown' if not found
    """
    # Handle NaN, None, or non-string values
    if pd.isna(country_code) or country_code is None:
        return 'Unknown'
    
    # Convert to string if needed
    if not isinstance(country_code, str):
        country_code = str(country_code)
    
    # Strip whitespace and convert to uppercase for consistency
    country_code = country_code.strip().upper()
    
    return CONTINENT_MAP.get(country_code, 'Unknown')


def get_countries_by_continent(continent_name):
    """
    Get all country codes for a given continent.
    
    Parameters:
    -----------
    continent_name : str
        Name of the continent (e.g., 'Europe', 'Asia', 'Africa')
    
    Returns:
    --------
    list : List of country codes belonging to the continent
    """
    return [code for code, cont in CONTINENT_MAP.items() if cont == continent_name]


def add_continent_column(df, country_column='country_code'):
    """
    Add a continent column to a DataFrame based on country codes.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing country codes
    country_column : str
        Name of the column containing country codes (default: 'country_code')
    
    Returns:
    --------
    pandas.DataFrame : DataFrame with added 'continent' column
    """
    if df is None or df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # If continent column already exists, return as-is
    if 'continent' in df.columns:
        return df
    
    # Find the country column - be very specific
    actual_country_col = None
    
    # First, check if the requested column exists and is a single column
    if country_column in df.columns:
        # Make absolutely sure it's a single column
        if isinstance(df[country_column], pd.Series):
            actual_country_col = country_column
    
    # If not found, try alternative column names
    if actual_country_col is None:
        possible_names = ['country_code', 'code', 'noc', 'NOC', 'Country Code']
        for col_name in possible_names:
            if col_name in df.columns:
                # Verify it's actually a Series, not a DataFrame
                try:
                    col_data = df[col_name]
                    if isinstance(col_data, pd.Series):
                        actual_country_col = col_name
                        break
                except:
                    continue
    
    if actual_country_col is None:
        # If no suitable column found, return original df
        return df
    
    # Define the mapping function
    def safe_get_continent(code):
        if pd.isna(code) or code is None:
            return 'Unknown'
        if not isinstance(code, str):
            code = str(code)
        code = code.strip().upper()
        return CONTINENT_MAP.get(code, 'Unknown')
    
    # Extract the column as a Series explicitly using iloc
    try:
        # Get column index
        col_idx = df.columns.get_loc(actual_country_col)
        
        # Use iloc to get the column as a Series
        country_series = df.iloc[:, col_idx]
        
        # Apply mapping
        df['continent'] = country_series.map(safe_get_continent).fillna('Unknown')
        
    except Exception as e:
        # Fallback: try direct assignment with explicit Series conversion
        try:
            country_series = pd.Series(df[actual_country_col].values, index=df.index)
            df['continent'] = country_series.map(safe_get_continent).fillna('Unknown')
        except:
            # Last resort: return df without continent
            return df
    
    return df


def filter_by_continent(df, continent_name, country_column='country_code'):
    """
    Filter DataFrame by continent.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to filter
    continent_name : str or list
        Continent name(s) to filter by
    country_column : str
        Name of the column containing country codes
    
    Returns:
    --------
    pandas.DataFrame : Filtered DataFrame
    """
    if df.empty:
        return df
    
    # Add continent column if not present
    if 'continent' not in df.columns:
        df = add_continent_column(df, country_column)
    
    # Handle single continent or list of continents
    if isinstance(continent_name, str):
        continent_name = [continent_name]
    
    return df[df['continent'].isin(continent_name)]


def get_all_continents():
    """
    Get list of all unique continents in the mapping.
    
    Returns:
    --------
    list : Sorted list of continent names
    """
    return sorted(set(CONTINENT_MAP.values()))


def get_continent_color(continent_name):
    """
    Get color for a given continent.
    
    Parameters:
    -----------
    continent_name : str
        Name of the continent
    
    Returns:
    --------
    str : Hex color code
    """
    return CONTINENT_COLORS.get(continent_name, '#808080')


def get_continent_stats(df, country_column='country_code'):
    """
    Get medal statistics by continent.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with country and medal data
    country_column : str
        Name of the column containing country codes
    
    Returns:
    --------
    pandas.DataFrame : Statistics grouped by continent
    """
    if df.empty:
        return pd.DataFrame()
    
    # Add continent column if not present
    if 'continent' not in df.columns:
        df = add_continent_column(df, country_column)
    
    # Determine which medal columns exist
    medal_cols = []
    for col in ['Gold', 'Silver', 'Bronze', 'Total']:
        if col in df.columns:
            medal_cols.append(col)
    
    if not medal_cols:
        return pd.DataFrame()
    
    # Group by continent and sum medals
    stats = df.groupby('continent')[medal_cols].sum().reset_index()
    stats = stats.sort_values(medal_cols[0] if medal_cols else 'Total', ascending=False)
    
    return stats


def validate_country_code(country_code):
    """
    Check if a country code is valid (exists in mapping).
    
    Parameters:
    -----------
    country_code : str
        Country code to validate
    
    Returns:
    --------
    bool : True if valid, False otherwise
    """
    if pd.isna(country_code) or country_code is None:
        return False
    
    if not isinstance(country_code, str):
        country_code = str(country_code)
    
    country_code = country_code.strip().upper()
    return country_code in CONTINENT_MAP