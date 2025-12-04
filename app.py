import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="🏅 Paris 2024 Olympics Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏅 Paris 2024 Olympics Dashboard")
st.markdown("### LA28 Volunteer Selection Challenge")

# Sidebar
st.sidebar.header("🎯 Filters")
st.sidebar.info("Use filters to explore the data")

# Simple data example
@st.cache_data
def load_sample_data():
    data = {
        'Country': ['USA', 'China', 'Japan', 'Great Britain', 'France'],
        'Gold': [40, 40, 20, 14, 16],
        'Silver': [44, 27, 12, 22, 26],
        'Bronze': [42, 24, 13, 29, 22],
        'Total': [126, 91, 45, 65, 64]
    }
    return pd.DataFrame(data)

df = load_sample_data()

# Display metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Countries", 5)
with col2:
    st.metric("Total Medals", df['Total'].sum())
with col3:
    st.metric("Gold Medals", df['Gold'].sum())
with col4:
    st.metric("Total Athletes", "11,000+")

# Display data
st.header("🏆 Top 5 Countries")
st.dataframe(df, use_container_width=True)

# Chart
st.header("📈 Medal Distribution")
fig = px.bar(df, x='Country', y=['Gold', 'Silver', 'Bronze'],
             title="Medals by Country",
             labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
             color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Built with Streamlit** 🎈 | **Data from Paris 2024 Olympics**")