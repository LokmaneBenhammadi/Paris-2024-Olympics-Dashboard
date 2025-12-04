"""
Data Loader Utility
Loads all CSV data files for Paris 2024 Olympics Dashboard with caching
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from config.config import DATA_FILES, RESULTS_DIR

@st.cache_data
def load_athletes():
    """
    Load athletes data.
    
    Returns:
    --------
    pandas.DataFrame : Athletes data with columns like name, country, gender, age, etc.
    """
    try:
        df = pd.read_csv(DATA_FILES['athletes'])
        return df
    except FileNotFoundError:
        st.warning(f"Athletes file not found: {DATA_FILES['athletes']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading athletes: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_medals_total():
    """
    Load total medals by country.
    
    Returns:
    --------
    pandas.DataFrame : Medal counts by country (Gold, Silver, Bronze, Total)
    """
    try:
        df = pd.read_csv(DATA_FILES['medals_total'])
        return df
    except FileNotFoundError:
        st.warning(f"Medals total file not found: {DATA_FILES['medals_total']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading medals total: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_medals():
    """
    Load detailed medals data.
    
    Returns:
    --------
    pandas.DataFrame : Detailed medal information
    """
    try:
        df = pd.read_csv(DATA_FILES['medals'])
        return df
    except FileNotFoundError:
        st.warning(f"Medals file not found: {DATA_FILES['medals']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading medals: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_medallists():
    """
    Load medallists data (individual medal winners).
    
    Returns:
    --------
    pandas.DataFrame : Individual medallists with athlete names and medal types
    """
    try:
        df = pd.read_csv(DATA_FILES['medallists'])
        return df
    except FileNotFoundError:
        st.warning(f"Medallists file not found: {DATA_FILES['medallists']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading medallists: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_nocs():
    """
    Load National Olympic Committees data.
    
    Returns:
    --------
    pandas.DataFrame : NOC codes with country names and additional info
    """
    try:
        df = pd.read_csv(DATA_FILES['nocs'])
        return df
    except FileNotFoundError:
        st.warning(f"NOCs file not found: {DATA_FILES['nocs']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading NOCs: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_events():
    """
    Load events data.
    
    Returns:
    --------
    pandas.DataFrame : Olympic events with sport, discipline, and event details
    """
    try:
        df = pd.read_csv(DATA_FILES['events'])
        return df
    except FileNotFoundError:
        st.warning(f"Events file not found: {DATA_FILES['events']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading events: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_schedules():
    """
    Load event schedules.
    
    Returns:
    --------
    pandas.DataFrame : Event schedules with dates, times, and venues
    """
    try:
        df = pd.read_csv(DATA_FILES['schedules'])
        return df
    except FileNotFoundError:
        st.warning(f"Schedules file not found: {DATA_FILES['schedules']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading schedules: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_schedules_preliminary():
    """
    Load preliminary schedules.
    
    Returns:
    --------
    pandas.DataFrame : Preliminary event schedules
    """
    try:
        df = pd.read_csv(DATA_FILES['schedules_preliminary'])
        return df
    except FileNotFoundError:
        st.warning(f"Preliminary schedules file not found: {DATA_FILES['schedules_preliminary']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading preliminary schedules: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_venues():
    """
    Load venues data.
    
    Returns:
    --------
    pandas.DataFrame : Venue information with locations, coordinates, etc.
    """
    try:
        df = pd.read_csv(DATA_FILES['venues'])
        return df
    except FileNotFoundError:
        st.warning(f"Venues file not found: {DATA_FILES['venues']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading venues: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_coaches():
    """
    Load coaches data.
    
    Returns:
    --------
    pandas.DataFrame : Coach information
    """
    try:
        df = pd.read_csv(DATA_FILES['coaches'])
        return df
    except FileNotFoundError:
        st.warning(f"Coaches file not found: {DATA_FILES['coaches']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading coaches: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_teams():
    """
    Load teams data.
    
    Returns:
    --------
    pandas.DataFrame : Team information
    """
    try:
        df = pd.read_csv(DATA_FILES['teams'])
        return df
    except FileNotFoundError:
        st.warning(f"Teams file not found: {DATA_FILES['teams']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading teams: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_technical_officials():
    """
    Load technical officials data.
    
    Returns:
    --------
    pandas.DataFrame : Technical officials information
    """
    try:
        df = pd.read_csv(DATA_FILES['technical_officials'])
        return df
    except FileNotFoundError:
        st.warning(f"Technical officials file not found: {DATA_FILES['technical_officials']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading technical officials: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_torch_route():
    """
    Load Olympic torch route data.
    
    Returns:
    --------
    pandas.DataFrame : Torch route information
    """
    try:
        df = pd.read_csv(DATA_FILES['torch_route'])
        return df
    except FileNotFoundError:
        st.warning(f"Torch route file not found: {DATA_FILES['torch_route']}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading torch route: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_sport_results(sport_name):
    """
    Load results for a specific sport.
    
    Parameters:
    -----------
    sport_name : str
        Name of the sport (e.g., 'Swimming', 'Athletics')
    
    Returns:
    --------
    pandas.DataFrame : Results for the specified sport
    """
    try:
        file_path = f"{RESULTS_DIR}{sport_name}.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.warning(f"Results file not found for {sport_name}: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading results for {sport_name}: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_all_sport_results():
    """
    Load all available sport results.
    
    Returns:
    --------
    dict : Dictionary with sport names as keys and DataFrames as values
    """
    results_path = Path(RESULTS_DIR)
    all_results = {}
    
    if not results_path.exists():
        st.warning(f"Results directory not found: {RESULTS_DIR}")
        return all_results
    
    try:
        for file_path in results_path.glob("*.csv"):
            sport_name = file_path.stem  # Get filename without extension
            try:
                df = pd.read_csv(file_path)
                all_results[sport_name] = df
            except Exception as e:
                st.warning(f"Could not load {sport_name}: {str(e)}")
        
        return all_results
    except Exception as e:
        st.error(f"Error loading sport results: {str(e)}")
        return all_results


def load_all_data():
    """
    Load all main data files at once.
    
    Returns:
    --------
    dict : Dictionary containing all loaded DataFrames
    """
    data = {
        'athletes': load_athletes(),
        'medals_total': load_medals_total(),
        'medals': load_medals(),
        'medallists': load_medallists(),
        'nocs': load_nocs(),
        'events': load_events(),
        'schedules': load_schedules(),
        'schedules_preliminary': load_schedules_preliminary(),
        'venues': load_venues(),
        'coaches': load_coaches(),
        'teams': load_teams(),
        'technical_officials': load_technical_officials(),
        'torch_route': load_torch_route()
    }
    
    return data


def check_data_availability():
    """
    Check which data files are available.
    
    Returns:
    --------
    dict : Dictionary with file names as keys and boolean availability as values
    """
    availability = {}
    
    for name, file_path in DATA_FILES.items():
        availability[name] = Path(file_path).exists()
    
    # Check results directory
    results_path = Path(RESULTS_DIR)
    if results_path.exists():
        result_files = list(results_path.glob("*.csv"))
        availability['results_count'] = len(result_files)
        availability['results_available'] = len(result_files) > 0
    else:
        availability['results_count'] = 0
        availability['results_available'] = False
    
    return availability


def get_data_summary():
    """
    Get a summary of loaded data (row counts, columns, etc.).
    
    Returns:
    --------
    dict : Summary statistics for each dataset
    """
    summary = {}
    data = load_all_data()
    
    for name, df in data.items():
        if not df.empty:
            summary[name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns)
            }
        else:
            summary[name] = {
                'rows': 0,
                'columns': 0,
                'column_names': []
            }
    
    return summary