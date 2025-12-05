"""
Page 7: Follow Up Your Country
Interactive country drill-down with map selection, sports, participants,
event timelines, and medals for a chosen NOC.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from config.config import COLORS, FLAG_EMOJI, CHART_HEIGHT
from utils.data_loader import (
    load_medals_total,
    load_medallists,
    load_athletes,
    load_teams,
    load_events,
    load_all_sport_results,
)
from utils.continent_mapper import add_continent_column


# Page configuration
st.set_page_config(
    page_title="Follow Up Your Country - Paris 2024",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS if available
css_file = Path("assets/styles.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_data
def load_follow_data():
    """Load datasets needed for the country follow-up page."""
    medals_total_df = load_medals_total()
    medallists_df = load_medallists()
    athletes_df = load_athletes()
    teams_df = load_teams()
    events_df = load_events()
    all_results = load_all_sport_results()

    # Add continent for map filtering convenience
    medals_total_df = add_continent_column(medals_total_df, "country_code")
    medallists_df = add_continent_column(medallists_df, "country_code")

    return {
        "medals_total": medals_total_df,
        "medallists": medallists_df,
        "athletes": athletes_df,
        "teams": teams_df,
        "events": events_df,
        "all_results": all_results,
    }


def normalize_sport_name(name: str) -> str:
    return str(name).strip().lower() if name is not None else ""


def extract_opponents(sport_df: pd.DataFrame, country_code: str) -> pd.DataFrame:
    """Annotate opponent info using stage_code pairs inside a sport results DF."""
    if sport_df.empty or "stage_code" not in sport_df.columns:
        return sport_df

    df = sport_df.copy()
    grouped = df.groupby("stage_code")
    opponent_country = []
    opponent_name = []

    for idx, row in df.iterrows():
        stage_rows = grouped.get_group(row["stage_code"])
        others = stage_rows[stage_rows["participant_country_code"] != country_code]
        opponent_country.append(", ".join(others["participant_country_code"].unique()) if not others.empty else "N/A")
        opponent_name.append(", ".join(others["participant_name"].astype(str).unique()) if not others.empty else "N/A")

    df["opponent_country"] = opponent_country
    df["opponent_name"] = opponent_name
    return df


def medal_summary_for_sport(medallists_df, country_code, sport_name):
    """Return medal counts for a given country and sport/discipline."""
    if medallists_df.empty:
        return {}
    filt = medallists_df[
        (medallists_df["country_code"] == country_code)
        & (medallists_df["discipline"].str.lower() == sport_name.lower())
    ]
    if filt.empty:
        return {}
    counts = filt["medal_type"].value_counts()
    return {
        "Gold": int(counts.get("Gold Medal", counts.get("Gold", 0))),
        "Silver": int(counts.get("Silver Medal", counts.get("Silver", 0))),
        "Bronze": int(counts.get("Bronze Medal", counts.get("Bronze", 0))),
        "Total": len(filt),
    }


data = load_follow_data()
medals_total_df = data["medals_total"]
medallists_df = data["medallists"]
athletes_df = data["athletes"]
teams_df = data["teams"]
events_df = data["events"]
all_results = data["all_results"]

# Header
st.markdown(
    f"""
<h1 style='text-align: center; color: {COLORS['paris_green']}; font-size: 2.4rem; margin: 0;'>
    📌 Follow Up Your Country
</h1>
<h3 style='text-align: center; color: {COLORS['text_secondary']}; font-weight: 400; margin-top: 8px;'>
    Select a country to see its sports, athletes/teams, opponents, and medals
</h3>
<hr style='border: 1px solid {COLORS['paris_green']}; margin: 18px 0;'>
""",
    unsafe_allow_html=True,
)

code_options = medals_total_df["country_code"].dropna().unique().tolist()
code_options.sort()
selected_code = st.selectbox("🌍 Select a country code", code_options, index=0)

if not selected_code:
    st.info("Select a country on the map or from the list to continue.")
    st.stop()

# Identify country name
country_row = medals_total_df[medals_total_df["country_code"] == selected_code].head(1)
country_name = country_row["country"].iloc[0] if not country_row.empty else selected_code
country_flag = FLAG_EMOJI.get(selected_code, "")

st.markdown(
    f"""
<div style='background:{COLORS['card_bg']}; padding:16px; border-radius:12px; border-left:5px solid {COLORS['paris_green']}; margin-bottom:12px;'>
    <h3 style='margin:0; color:{COLORS['text']};'>Following: {country_flag} {country_name} ({selected_code})</h3>
</div>
""",
    unsafe_allow_html=True,
)

# Filter data for the selected country
country_medals = medallists_df[medallists_df["country_code"] == selected_code]
country_athletes = athletes_df[athletes_df["country_code"] == selected_code] if not athletes_df.empty and "country_code" in athletes_df.columns else pd.DataFrame()
country_teams = teams_df[teams_df["country_code"] == selected_code] if not teams_df.empty and "country_code" in teams_df.columns else pd.DataFrame()

# Determine sports with participation (from medallists + results)
sports_from_medals = set(country_medals["discipline"].dropna().unique())
sports_from_results = set()
for sport_key, df in all_results.items():
    if not df.empty and "participant_country_code" in df.columns:
        if selected_code in df["participant_country_code"].unique():
            sports_from_results.add(sport_key)

all_sports_for_country = sorted({normalize_sport_name(s) for s in sports_from_medals} | {normalize_sport_name(s) for s in sports_from_results})

summary_cols = st.columns(4)
with summary_cols[0]:
    st.metric("Sports participated", len(all_sports_for_country))
with summary_cols[1]:
    st.metric("Medals", len(country_medals))
with summary_cols[2]:
    st.metric("Athletes", len(country_athletes))
with summary_cols[3]:
    total_teams = int(country_teams["team"].nunique()) if not country_teams.empty and "team" in country_teams.columns else 0
    st.metric("Teams", total_teams)

st.markdown("---")

if not all_sports_for_country:
    st.info("No participation data found for this country in results/medals.")
    st.stop()

# Sport-by-sport detail
for sport_norm in all_sports_for_country:
    # Find matching results DF by normalized name
    matching_key = next((k for k in all_results.keys() if normalize_sport_name(k) == sport_norm), None)
    sport_df = all_results.get(matching_key, pd.DataFrame()) if matching_key else pd.DataFrame()

    sport_label = matching_key or sport_norm.title()

    st.markdown(
        f"<h3 style='color:{COLORS['paris_green']}; margin-bottom:6px;' id='{sport_label}'>🏅 {sport_label}</h3>",
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([1, 2])

    with col_a:
        # Participants from results
        participants = pd.DataFrame()
        if not sport_df.empty and "participant_country_code" in sport_df.columns:
            participants = sport_df[sport_df["participant_country_code"] == selected_code]
            participants = participants[["participant_name", "participant_type"]].drop_duplicates()
            participants.rename(columns={"participant_name": "Name", "participant_type": "Type"}, inplace=True)

        # Athletes/teams from master tables
        if participants.empty:
            if not country_athletes.empty and "disciplines" in country_athletes.columns:
                mask = country_athletes["disciplines"].astype(str).str.contains(sport_label, case=False, na=False)
                participants = country_athletes[mask][["name", "gender"]].rename(columns={"name": "Name", "gender": "Type"})
            elif not country_teams.empty and "discipline" in country_teams.columns:
                mask = country_teams["discipline"].astype(str).str.contains(sport_label, case=False, na=False)
                participants = country_teams[mask][["team", "team_gender"]].rename(columns={"team": "Name", "team_gender": "Type"})

        st.write("Athletes / Teams")
        if participants.empty:
            st.info("No participant data for this sport.")
        else:
            st.dataframe(participants.reset_index(drop=True), use_container_width=True, hide_index=True)

        # Medals in this sport
        medal_counts = medal_summary_for_sport(medallists_df, selected_code, sport_label)
        if medal_counts:
            st.write("Medals in this sport")
            medal_cols = st.columns(4)
            medal_cols[0].metric("Total", medal_counts.get("Total", 0))
            medal_cols[1].metric("🥇 Gold", medal_counts.get("Gold", 0))
            medal_cols[2].metric("🥈 Silver", medal_counts.get("Silver", 0))
            medal_cols[3].metric("🥉 Bronze", medal_counts.get("Bronze", 0))
        else:
            st.caption("No medals recorded for this sport.")

    with col_b:
        if sport_df.empty:
            st.info("No detailed results available for this sport.")
        else:
            # Filter and annotate opponents
            country_results = sport_df[sport_df["participant_country_code"] == selected_code]
            country_results = extract_opponents(sport_df, selected_code)
            country_results = country_results[country_results["participant_country_code"] == selected_code]

            if country_results.empty:
                st.info("No results rows for this country in the sport file.")
            else:
                # Final outcome column
                if "result_WLT" in country_results.columns:
                    outcome_map = {"W": "Win", "L": "Lose", "T": "Draw"}
                    country_results["final_outcome"] = country_results["result_WLT"].map(outcome_map).fillna("")
                elif "rank" in country_results.columns:
                    country_results["final_outcome"] = country_results["rank"].apply(
                        lambda r: "Win" if pd.notna(r) and r == 1 else "Lose"
                    )
                else:
                    country_results["final_outcome"] = ""

                # Compact table
                show_cols = [
                    "date",
                    "event_stage",
                    "participant_name",
                    "opponent_name",
                    "result",
                    "rank",
                    "final_outcome",
                ]
                existing_cols = [c for c in show_cols if c in country_results.columns]
                st.write("Event details")
                st.dataframe(
                    country_results[existing_cols].sort_values(by="date").reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

    st.markdown("---")

