# 🏅 Paris 2024 Olympics Dashboard

**An interactive multi-page Streamlit dashboard for exploring the Paris 2024 Olympic Games data**

Built for the LA28 Volunteer Selection Challenge | ESI-SBA

---

## 🎯 Overview

This dashboard analyzes comprehensive data from the Paris 2024 Olympic Games, providing interactive insights into athlete performance, medal distributions, global trends, and event schedules.

**Key Features:**
- 6 interactive pages with 20+ visualizations
- Global filters (Country, Sport, Medal Type, Continent)
- Creative features: "Who Won the Day?", Head-to-Head comparison
- Professional UI with Olympic-themed design

---

## 📁 Project Structure

```
streamlit_project/
├── app.py                          # Main entry point
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Global_Analysis.py
│   ├── 3_Athlete_Performance.py
│   ├── 4_Sports_and_Events.py
│   ├── 5_Advanced_Analytics.py
│   └── 6_Country_Comparison.py
├── utils/
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── filters.py
│   ├── visualizations.py
│   └── continent_mapper.py
├── config/
│   └── config.py
├── assets/
│   └── styles.css
├── data/                           # CSV files here
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/your-username/paris-2024-olympics-dashboard.git
cd paris-2024-olympics-dashboard

# Run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 📊 Data Sources

Download the dataset from [Kaggle Paris 2024 Olympics](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games) and place all CSV files in the `data/` folder.

**Required files:**
- `athletes.csv`, `medals.csv`, `medals_total.csv`, `nocs.csv`
- `events.csv`, `schedules.csv`, `venues.csv`
- `results/` folder with 45 sport CSV files

---

## ✨ Features by Page

### 🏠 Page 1: Overview
- 5 real-time KPI metrics
- Medal distribution pie chart
- Top 10 countries bar chart

### 🗺️ Page 2: Global Analysis
- World choropleth map
- Continent → Country → Sport hierarchy (Sunburst/Treemap)
- Continental medal comparison

### 👤 Page 3: Athlete Performance
- Searchable athlete profiles with photos
- Age distribution analysis
- Gender distribution by region
- Top athletes leaderboard

### 🏟️ Page 4: Sports & Events
- Event schedule Gantt chart
- Medal count treemap by sport
- Venue map (Paris locations)

### 🎯 Page 5: Advanced Analytics ⭐
- Top countries by continent & gender
- **"Who Won the Day?"** - Daily highlights timeline
- Advanced medal distributions

### ⚔️ Page 6: Country Comparison ⭐
- Head-to-head country analysis
- Performance radar charts
- Medal accumulation timeline
- "What If?" scenarios

---

## 🛠️ Technologies

- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Plotly** - Interactive visualizations
- **Docker** - Containerization

---

## 🎨 Design Choices

**Color Scheme:** Paris 2024 Olympic palette (Pink `#FF6B9D`, Blue `#0085CA`, Gold/Silver/Bronze)

**Layout:** Progressive disclosure - overview first, then drill-down details

**Filters:** Global sidebar filters on every page for consistent UX

---

## 💡 Creative Features

1. **Continent Filter** - Map 206 countries to 6 continents
2. **"Who Won the Day?"** - Interactive daily timeline with medal awards
3. **Head-to-Head Tool** - Compare any two countries side-by-side
4. **Athlete Profiles** - Searchable cards with photos and coach info
5. **Animated Choropleth** - Time-lapse of medal accumulation

---

## 👥 Team

**[Your Team Name]**

- Benhammadi Lokmane
- Benblal Badr-eddin Adam
- Belkaid Yacine

---

## 📝 Competition Info

**Challenge:** LA28 Volunteer Selection - Paris 2024 Dashboard

**Institution:** ESI-SBA

**Instructor:** Dr. Belkacem KHALDI

**Submission:** Early Bird (48 hours) - 100% eligible

**Presentation:** December 7, 2025

---

## 🐳 Docker Commands

```bash
# Build and run
docker-compose up --build

# Stop
docker-compose down

# Rebuild after changes
docker-compose up --build --force-recreate

# View logs
docker-compose logs -f
```

---

## 📄 License

MIT License - Dataset from [Kaggle](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)

---

## 🔗 Links

**Repository:** [GitHub Link]

**Live Demo:** [Streamlit Cloud Link]

**Video Demo:** [YouTube Link]

---