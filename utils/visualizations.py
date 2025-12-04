"""
Visualizations Utility
Reusable Plotly chart functions for Paris 2024 Olympics Dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.config import COLORS, MEDAL_COLORS, PLOTLY_TEMPLATE, CONTINENT_COLORS, CHART_HEIGHT
from utils.continent_mapper import get_continent_color


def create_medal_distribution_pie(medals_df, title="Medal Distribution"):
    """
    Create an enhanced donut chart showing medal distribution.
    """
    if medals_df.empty:
        return go.Figure()
    
    # Find medal columns flexibly
    gold_cols = [c for c in medals_df.columns if 'gold' in c.lower()]
    silver_cols = [c for c in medals_df.columns if 'silver' in c.lower()]
    bronze_cols = [c for c in medals_df.columns if 'bronze' in c.lower()]
    
    if not (gold_cols and silver_cols and bronze_cols):
        return go.Figure()
    
    totals = {
        'Gold': int(medals_df[gold_cols[0]].sum()),
        'Silver': int(medals_df[silver_cols[0]].sum()),
        'Bronze': int(medals_df[bronze_cols[0]].sum())
    }
    
    # Remove zeros
    totals = {k: v for k, v in totals.items() if v > 0}
    
    if not totals:
        return go.Figure()
    
    fig = go.Figure(data=[go.Pie(
        labels=list(totals.keys()),
        values=list(totals.values()),
        marker=dict(
            colors=[MEDAL_COLORS[k] for k in totals.keys()],
            line=dict(color=COLORS['background'], width=3)
        ),
        hole=0.5,
        textinfo='label+percent',
        textfont=dict(size=16, color=COLORS['text'], family='Arial Black'),
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>',
        pull=[0.05, 0.03, 0.03]  # Slightly pull out Gold
    )])
    
    # Add center annotation
    total_medals = sum(totals.values())
    fig.add_annotation(
        text=f'<b>{total_medals:,}</b><br>Total<br>Medals',
        x=0.5, y=0.5,
        font=dict(size=20, color=COLORS['paris_green'], family='Arial Black'),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLORS['text'], family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        template=PLOTLY_TEMPLATE,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium'],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        )
    )
    
    return fig


def create_top_countries_bar(medals_df, n=10, title="Top Countries by Medal Count"):
    """
    Create an enhanced horizontal stacked bar chart of top countries.
    """
    if medals_df.empty:
        return go.Figure()
    
    # Ensure we have the needed columns
    gold_cols = [c for c in medals_df.columns if 'gold' in c.lower()]
    silver_cols = [c for c in medals_df.columns if 'silver' in c.lower()]
    bronze_cols = [c for c in medals_df.columns if 'bronze' in c.lower()]
    total_cols = [c for c in medals_df.columns if c.lower() == 'total']
    
    if not (gold_cols and silver_cols and bronze_cols):
        return go.Figure()
    
    df_work = medals_df.copy()
    
    # Normalize column names
    df_work['Gold'] = df_work[gold_cols[0]]
    df_work['Silver'] = df_work[silver_cols[0]]
    df_work['Bronze'] = df_work[bronze_cols[0]]
    
    if total_cols:
        df_work['Total'] = df_work[total_cols[0]]
    else:
        df_work['Total'] = df_work['Gold'] + df_work['Silver'] + df_work['Bronze']
    
    # Get top N countries
    top_countries = df_work.nlargest(n, 'Total')
    country_col = 'country' if 'country' in top_countries.columns else 'country_code'
    
    # Create figure with stacked bars
    fig = go.Figure()
    
    # Add traces in reverse order for proper stacking
    fig.add_trace(go.Bar(
        name='🥇 Gold',
        y=top_countries[country_col],
        x=top_countries['Gold'],
        orientation='h',
        marker=dict(
            color=MEDAL_COLORS['Gold'],
            line=dict(color=COLORS['background'], width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Gold: %{x}<extra></extra>',
        text=top_countries['Gold'],
        textposition='inside',
        textfont=dict(size=12, color='#000')
    ))
    
    fig.add_trace(go.Bar(
        name='🥈 Silver',
        y=top_countries[country_col],
        x=top_countries['Silver'],
        orientation='h',
        marker=dict(
            color=MEDAL_COLORS['Silver'],
            line=dict(color=COLORS['background'], width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Silver: %{x}<extra></extra>',
        text=top_countries['Silver'],
        textposition='inside',
        textfont=dict(size=12, color='#000')
    ))
    
    fig.add_trace(go.Bar(
        name='🥉 Bronze',
        y=top_countries[country_col],
        x=top_countries['Bronze'],
        orientation='h',
        marker=dict(
            color=MEDAL_COLORS['Bronze'],
            line=dict(color=COLORS['background'], width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Bronze: %{x}<extra></extra>',
        text=top_countries['Bronze'],
        textposition='inside',
        textfont=dict(size=12, color='#000')
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLORS['text'], family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        barmode='stack',
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium'],
        xaxis=dict(
            title='Medal Count',
            gridcolor=COLORS['card_bg'],
            showgrid=True
        ),
        yaxis=dict(
            title='',
            categoryorder='total ascending'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        hovermode='closest',
        template=PLOTLY_TEMPLATE
    )
    
    return fig


def create_continent_comparison_bar(medals_df, title="Medal Count by Continent"):
    """
    Create a bar chart comparing continents.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Medal data with continent column
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Bar chart
    """
    if medals_df.empty or 'continent' not in medals_df.columns:
        return go.Figure()
    
    continent_data = medals_df.groupby('continent')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    continent_data['Total'] = continent_data['Gold'] + continent_data['Silver'] + continent_data['Bronze']
    continent_data = continent_data.sort_values('Total', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Gold',
        x=continent_data['continent'],
        y=continent_data['Gold'],
        marker_color=MEDAL_COLORS['Gold']
    ))
    
    fig.add_trace(go.Bar(
        name='Silver',
        x=continent_data['continent'],
        y=continent_data['Silver'],
        marker_color=MEDAL_COLORS['Silver']
    ))
    
    fig.add_trace(go.Bar(
        name='Bronze',
        x=continent_data['continent'],
        y=continent_data['Bronze'],
        marker_color=MEDAL_COLORS['Bronze']
    ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        template=PLOTLY_TEMPLATE,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium'],
        xaxis_title='Continent',
        yaxis_title='Medal Count'
    )
    
    return fig


def create_choropleth_map(medals_df, title="Global Medal Distribution"):
    """
    Create a choropleth world map showing medal distribution.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Medal data with country codes
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Choropleth map
    """
    if medals_df.empty:
        return go.Figure()
    
    country_col = 'country_code' if 'country_code' in medals_df.columns else 'code'
    
    if 'Total' not in medals_df.columns:
        medals_df = medals_df.copy()
        medals_df['Total'] = medals_df.get('Gold', 0) + medals_df.get('Silver', 0) + medals_df.get('Bronze', 0)
    
    fig = px.choropleth(
        medals_df,
        locations=country_col,
        locationmode='ISO-3',
        color='Total',
        hover_name='country' if 'country' in medals_df.columns else country_col,
        color_continuous_scale=[
            [0, COLORS['background']],
            [0.5, COLORS['paris_green']],
            [1, COLORS['paris_green_dark']]
        ],
        title=title,
        template=PLOTLY_TEMPLATE
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['large'],
        geo=dict(
            bgcolor=COLORS['background'],
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    return fig


def create_sunburst_chart(df, path, values, title="Hierarchical View"):
    """
    Create a sunburst chart for hierarchical data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with hierarchical columns
    path : list
        List of column names defining hierarchy (e.g., ['continent', 'country', 'sport'])
    values : str
        Column name for values
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Sunburst chart
    """
    if df.empty:
        return go.Figure()
    
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['large']
    )
    
    return fig


def create_treemap_chart(df, path, values, title="Treemap View"):
    """
    Create a treemap chart for hierarchical data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with hierarchical columns
    path : list
        List of column names defining hierarchy
    values : str
        Column name for values
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Treemap chart
    """
    if df.empty:
        return go.Figure()
    
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        template=PLOTLY_TEMPLATE,
        color=values,
        color_continuous_scale=[
            [0, COLORS['background']],
            [0.5, COLORS['paris_green']],
            [1, COLORS['paris_green_dark']]
        ]
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['large']
    )
    
    return fig


def create_age_distribution_box(athletes_df, group_by=None, title="Age Distribution"):
    """
    Create a box plot showing age distribution.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athlete data with age column
    group_by : str or None
        Column to group by (e.g., 'sport', 'gender')
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Box plot
    """
    if athletes_df.empty or 'age' not in athletes_df.columns:
        return go.Figure()
    
    # Filter valid ages
    df_clean = athletes_df[(athletes_df['age'].notna()) & (athletes_df['age'] > 0) & (athletes_df['age'] < 100)]
    
    if group_by and group_by in df_clean.columns:
        fig = px.box(
            df_clean,
            y='age',
            x=group_by,
            title=title,
            template=PLOTLY_TEMPLATE,
            color=group_by
        )
    else:
        fig = px.box(
            df_clean,
            y='age',
            title=title,
            template=PLOTLY_TEMPLATE
        )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium']
    )
    
    return fig


def create_gender_distribution_pie(athletes_df, title="Gender Distribution"):
    """
    Create a pie chart showing gender distribution.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athlete data with gender column
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Pie chart
    """
    if athletes_df.empty or 'gender' not in athletes_df.columns:
        return go.Figure()
    
    gender_counts = athletes_df['gender'].value_counts()
    
    fig = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        title=title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=[COLORS['secondary'], COLORS['danger'], COLORS['paris_green']]
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium']
    )
    
    return fig


def create_timeline_chart(df, x_col, y_col, title="Timeline", color_col=None):
    """
    Create a timeline/line chart.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with time series
    x_col : str
        Column for x-axis (typically date/time)
    y_col : str
        Column for y-axis (values)
    title : str
        Chart title
    color_col : str or None
        Column to color lines by
    
    Returns:
    --------
    plotly.graph_objects.Figure : Line chart
    """
    if df.empty:
        return go.Figure()
    
    if color_col and color_col in df.columns:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            template=PLOTLY_TEMPLATE
        )
    else:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS['paris_green']]
        )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium']
    )
    
    return fig


def create_radar_chart(categories, values, title="Performance Radar", names=None):
    """
    Create a radar/spider chart for multi-dimensional comparison.
    
    Parameters:
    -----------
    categories : list
        Category names for each axis
    values : list or list of lists
        Values for each category (or list of value lists for multiple traces)
    title : str
        Chart title
    names : list or None
        Names for multiple traces
    
    Returns:
    --------
    plotly.graph_objects.Figure : Radar chart
    """
    fig = go.Figure()
    
    if isinstance(values[0], (list, tuple)):
        # Multiple traces
        colors = [COLORS['paris_green'], COLORS['secondary'], COLORS['danger']]
        for i, val_list in enumerate(values):
            fig.add_trace(go.Scatterpolar(
                r=val_list,
                theta=categories,
                fill='toself',
                name=names[i] if names else f'Series {i+1}',
                line_color=colors[i % len(colors)]
            ))
    else:
        # Single trace
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance',
            line_color=COLORS['paris_green']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(v) if isinstance(v, list) else v for v in values) * 1.1]
            ),
            bgcolor=COLORS['card_bg']
        ),
        showlegend=True,
        title=title,
        template=PLOTLY_TEMPLATE,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['medium']
    )
    
    return fig


def create_gantt_chart(df, x_start, x_end, y, title="Schedule", color_col=None):
    """
    Create a Gantt chart for schedules.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Schedule data
    x_start : str
        Column for start time
    x_end : str
        Column for end time
    y : str
        Column for y-axis labels
    title : str
        Chart title
    color_col : str or None
        Column to color by
    
    Returns:
    --------
    plotly.graph_objects.Figure : Gantt/timeline chart
    """
    if df.empty:
        return go.Figure()
    
    if color_col and color_col in df.columns:
        fig = px.timeline(
            df,
            x_start=x_start,
            x_end=x_end,
            y=y,
            color=color_col,
            title=title,
            template=PLOTLY_TEMPLATE
        )
    else:
        fig = px.timeline(
            df,
            x_start=x_start,
            x_end=x_end,
            y=y,
            title=title,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS['paris_green']]
        )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['large']
    )
    
    return fig


def create_scatter_map(df, lat_col, lon_col, title="Map View", hover_name=None, size_col=None):
    """
    Create a scatter map showing locations.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with coordinates
    lat_col : str
        Latitude column
    lon_col : str
        Longitude column
    title : str
        Chart title
    hover_name : str or None
        Column for hover labels
    size_col : str or None
        Column for marker size
    
    Returns:
    --------
    plotly.graph_objects.Figure : Scatter map
    """
    if df.empty:
        return go.Figure()
    
    fig = px.scatter_mapbox(
        df,
        lat=lat_col,
        lon=lon_col,
        hover_name=hover_name,
        size=size_col,
        title=title,
        zoom=10,
        height=CHART_HEIGHT['large'],
        color_discrete_sequence=[COLORS['paris_green']]
    )
    
    fig.update_layout(
        mapbox_style='carto-darkmatter',
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig


def create_heatmap(df, x_col, y_col, values_col, title="Heatmap"):
    """
    Create a heatmap visualization.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data for heatmap
    x_col : str
        Column for x-axis
    y_col : str
        Column for y-axis
    values_col : str
        Column for cell values
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Heatmap
    """
    if df.empty:
        return go.Figure()
    
    pivot_df = df.pivot_table(values=values_col, index=y_col, columns=x_col, aggfunc='sum', fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale=[
            [0, COLORS['background']],
            [0.5, COLORS['paris_green']],
            [1, COLORS['paris_green_dark']]
        ],
        text=pivot_df.values,
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title=title,
        template=PLOTLY_TEMPLATE,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        height=CHART_HEIGHT['large']
    )
    
    return fig


def create_grouped_bar_chart(medals_df, show_gold=True, show_silver=True, show_bronze=True, 
                             title="Medal Comparison", orientation='v', n=None):
    """
    Create a grouped bar chart for medal comparison.
    
    Parameters:
    -----------
    medals_df : pandas.DataFrame
        Medal data with Gold, Silver, Bronze columns
    show_gold : bool
        Show gold medals
    show_silver : bool
        Show silver medals
    show_bronze : bool
        Show bronze medals
    title : str
        Chart title
    orientation : str
        'v' for vertical, 'h' for horizontal
    n : int or None
        Limit to top N entries
    
    Returns:
    --------
    plotly.graph_objects.Figure : Grouped bar chart
    """
    if medals_df.empty:
        return go.Figure()
    
    # Limit to top N if specified
    if n is not None and 'Total' in medals_df.columns:
        medals_df = medals_df.nlargest(n, 'Total')
    
    # Determine label column
    label_col = 'country' if 'country' in medals_df.columns else 'continent'
    
    fig = go.Figure()
    
    if orientation == 'v':
        x_data = medals_df[label_col]
        if show_gold:
            fig.add_trace(go.Bar(
                name='🥇 Gold',
                x=x_data,
                y=medals_df['Gold'],
                marker=dict(
                    color=MEDAL_COLORS['Gold'],
                    line=dict(color=COLORS['background'], width=2.5),
                    pattern=dict(shape="/", solidity=0.3)
                ),
                text=medals_df['Gold'],
                textposition='outside',
                textfont=dict(size=12, color=COLORS['text'], family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>🥇 Gold: %{y:,}<extra></extra>'
            ))
        
        if show_silver:
            fig.add_trace(go.Bar(
                name='🥈 Silver',
                x=x_data,
                y=medals_df['Silver'],
                marker=dict(
                    color=MEDAL_COLORS['Silver'],
                    line=dict(color=COLORS['background'], width=2.5)
                ),
                text=medals_df['Silver'],
                textposition='outside',
                textfont=dict(size=12, color=COLORS['text'], family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>🥈 Silver: %{y:,}<extra></extra>'
            ))
        
        if show_bronze:
            fig.add_trace(go.Bar(
                name='🥉 Bronze',
                x=x_data,
                y=medals_df['Bronze'],
                marker=dict(
                    color=MEDAL_COLORS['Bronze'],
                    line=dict(color=COLORS['background'], width=2.5)
                ),
                text=medals_df['Bronze'],
                textposition='outside',
                textfont=dict(size=12, color=COLORS['text'], family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>🥉 Bronze: %{y:,}<extra></extra>'
            ))
        
        xaxis_config = dict(
            title=dict(text=f'<b>{label_col.title()}</b>', font=dict(size=16)),
            tickfont=dict(size=13, family='Arial Black')
        )
        yaxis_config = dict(
            title=dict(text='<b>Medal Count</b>', font=dict(size=16)),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        )
    else:  # horizontal
        y_data = medals_df[label_col]
        if show_gold:
            fig.add_trace(go.Bar(
                name='🥇 Gold',
                y=y_data,
                x=medals_df['Gold'],
                orientation='h',
                marker=dict(
                    color=MEDAL_COLORS['Gold'],
                    line=dict(color=COLORS['background'], width=2)
                ),
                text=medals_df['Gold'],
                textposition='inside',
                textfont=dict(size=13, color='black', family='Arial Black'),
                hovertemplate='<b>%{y}</b><br>Gold: %{x:,}<extra></extra>'
            ))
        
        if show_silver:
            fig.add_trace(go.Bar(
                name='🥈 Silver',
                y=y_data,
                x=medals_df['Silver'],
                orientation='h',
                marker=dict(
                    color=MEDAL_COLORS['Silver'],
                    line=dict(color=COLORS['background'], width=2)
                ),
                text=medals_df['Silver'],
                textposition='inside',
                textfont=dict(size=13, color='black', family='Arial Black'),
                hovertemplate='<b>%{y}</b><br>Silver: %{x:,}<extra></extra>'
            ))
        
        if show_bronze:
            fig.add_trace(go.Bar(
                name='🥉 Bronze',
                y=y_data,
                x=medals_df['Bronze'],
                orientation='h',
                marker=dict(
                    color=MEDAL_COLORS['Bronze'],
                    line=dict(color=COLORS['background'], width=2)
                ),
                text=medals_df['Bronze'],
                textposition='inside',
                textfont=dict(size=13, color='black', family='Arial Black'),
                hovertemplate='<b>%{y}</b><br>Bronze: %{x:,}<extra></extra>'
            ))
        
        xaxis_config = dict(
            title=dict(text='<b>Medal Count</b>', font=dict(size=16)),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        )
        yaxis_config = dict(
            title='',
            categoryorder='total ascending' if orientation == 'h' else None,
            tickfont=dict(size=13, family='Arial Black')
        )
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color=COLORS['paris_green'], family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        barmode='group',
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family='Arial'),
        height=550 if orientation == 'v' else 800,
        xaxis=xaxis_config,
        yaxis=yaxis_config,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=15, family='Arial Black'),
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor=COLORS['paris_green'],
            borderwidth=2
        ),
        hovermode='x unified' if orientation == 'v' else 'y unified',
        template='plotly_dark'
    )
    
    return fig


def create_enhanced_sunburst(grouped_df, path_cols, value_col, title="Medal Hierarchy"):
    """
    Create an enhanced sunburst chart with custom styling.
    
    Parameters:
    -----------
    grouped_df : pandas.DataFrame
        Grouped data for hierarchy
    path_cols : list
        List of column names for hierarchy path
    value_col : str
        Column name for values
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Enhanced sunburst chart
    """
    if grouped_df.empty:
        return go.Figure()
    
    fig = px.sunburst(
        grouped_df,
        path=path_cols,
        values=value_col,
        color=value_col,
        color_continuous_scale=[
            [0, '#1a1a2e'],
            [0.2, COLORS['secondary']],
            [0.5, COLORS['paris_green']],
            [0.7, COLORS['warning']],
            [1, COLORS['gold']]
        ],
        template='plotly_dark',
        labels={value_col: 'Medals'},
        hover_data={value_col: ':,'}
    )
    
    fig.update_traces(
        textfont=dict(size=14, family='Arial Black'),
        marker=dict(
            line=dict(color=COLORS['background'], width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Medals: %{value:,}<br>%{percentParent}<extra></extra>'
    )
    
    fig.update_layout(
        height=700,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], size=13, family='Arial'),
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text=f"<b>{title}</b><br><sub>Click segments to drill down</sub>",
            font=dict(size=20, color=COLORS['paris_green']),
            x=0.5,
            xanchor='center'
        )
    )
    
    return fig


def create_enhanced_treemap(grouped_df, path_cols, value_col, title="Medal Distribution"):
    """
    Create an enhanced treemap chart with custom styling.
    
    Parameters:
    -----------
    grouped_df : pandas.DataFrame
        Grouped data for hierarchy
    path_cols : list
        List of column names for hierarchy path
    value_col : str
        Column name for values
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Enhanced treemap chart
    """
    if grouped_df.empty:
        return go.Figure()
    
    fig = px.treemap(
        grouped_df,
        path=path_cols,
        values=value_col,
        color=value_col,
        color_continuous_scale=[
            [0, '#2d2d44'],
            [0.3, COLORS['secondary']],
            [0.6, COLORS['paris_green']],
            [0.8, COLORS['warning']],
            [1, COLORS['danger']]
        ],
        template='plotly_dark',
        labels={value_col: 'Medals'},
        hover_data={value_col: ':,'}
    )
    
    fig.update_traces(
        textfont=dict(size=16, family='Arial Black', color='white'),
        marker=dict(
            line=dict(color=COLORS['background'], width=3),
            cornerradius=5
        ),
        hovertemplate='<b>%{label}</b><br>Medals: %{value:,}<br>%{percentParent} of parent<extra></extra>'
    )
    
    fig.update_layout(
        height=700,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], size=13),
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text=f"<b>{title}</b><br><sub>Size represents medal count</sub>",
            font=dict(size=20, color=COLORS['paris_green']),
            x=0.5,
            xanchor='center'
        )
    )
    
    return fig


def create_athlete_age_violin(athletes_df, title="Age Distribution by Gender"):
    """
    Create an enhanced violin plot for age distribution by gender.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athlete data with age and gender columns
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Violin plot
    """
    if athletes_df.empty or 'age' not in athletes_df.columns or 'gender' not in athletes_df.columns:
        return go.Figure()
    
    df_clean = athletes_df.dropna(subset=['age', 'gender'])
    
    if df_clean.empty:
        return go.Figure()
    
    fig = px.violin(
        df_clean,
        y='age',
        x='gender',
        color='gender',
        box=True,
        points='outliers',
        color_discrete_map={
            'Male': COLORS['secondary'], 
            'Female': COLORS['paris_green'],
            'Mixed': COLORS['warning']
        },
        template='plotly_dark',
        title=title
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family='Arial Black'),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, color=COLORS['paris_green']),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        height=CHART_HEIGHT['medium'],
        xaxis_title='Gender',
        yaxis_title='Age (years)',
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        hovermode='closest'
    )
    
    return fig


def create_athlete_age_box_by_sport(athletes_df, n=10, title="Age Distribution by Top Sports"):
    """
    Create an enhanced box plot for age distribution by sport.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athlete data with age and sport columns
    n : int
        Number of top sports to show
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Box plot
    """
    if athletes_df.empty or 'age' not in athletes_df.columns:
        return go.Figure()
    
    sport_col = 'disciplines' if 'disciplines' in athletes_df.columns else 'sport'
    
    if sport_col not in athletes_df.columns:
        return go.Figure()
    
    df_clean = athletes_df.dropna(subset=['age', sport_col])
    
    if df_clean.empty:
        return go.Figure()
    
    # Get top N sports
    top_sports = df_clean[sport_col].value_counts().head(n).index
    sport_data = df_clean[df_clean[sport_col].isin(top_sports)]
    
    fig = px.box(
        sport_data,
        x=sport_col,
        y='age',
        color=sport_col,
        template='plotly_dark',
        title=title
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family='Arial Black'),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, color=COLORS['paris_green']),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        xaxis_title='Sport',
        yaxis_title='Age (years)',
        height=CHART_HEIGHT['medium'],
        xaxis=dict(tickangle=45),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        hovermode='x'
    )
    
    return fig


def create_gender_distribution_bar(athletes_df, group_by='continent', title="Gender Distribution"):
    """
    Create an enhanced grouped bar chart for gender distribution.
    
    Parameters:
    -----------
    athletes_df : pandas.DataFrame
        Athlete data with gender column
    group_by : str
        Column to group by ('continent' or 'country')
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Grouped bar chart
    """
    if athletes_df.empty or 'gender' not in athletes_df.columns or group_by not in athletes_df.columns:
        return go.Figure()
    
    grouped_data = athletes_df.groupby([group_by, 'gender']).size().reset_index(name='count')
    
    if grouped_data.empty:
        return go.Figure()
    
    # For country view, limit to top 20
    if group_by == 'country':
        top_entities = athletes_df[group_by].value_counts().head(20).index
        grouped_data = grouped_data[grouped_data[group_by].isin(top_entities)]
    
    fig = px.bar(
        grouped_data,
        x=group_by,
        y='count',
        color='gender',
        title=title,
        barmode='group',
        color_discrete_map={
            'Male': COLORS['secondary'], 
            'Female': COLORS['paris_green'],
            'Mixed': COLORS['warning']
        },
        template='plotly_dark'
    )
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family='Arial Black'),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, color=COLORS['paris_green']),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=group_by.title(),
        yaxis_title='Number of Athletes',
        height=CHART_HEIGHT['medium'],
        xaxis=dict(tickangle=45 if group_by == 'country' else 0),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        )
    )
    
    return fig


def create_top_athletes_stacked_bar(medallists_df, n=10, title="Top Athletes by Medal Count"):
    """
    Create an enhanced stacked bar chart for top athletes by medal count.
    
    Parameters:
    -----------
    medallists_df : pandas.DataFrame
        Medallist data with name, country, and medal_type columns
    n : int
        Number of top athletes to show
    title : str
        Chart title
    
    Returns:
    --------
    plotly.graph_objects.Figure : Stacked bar chart
    """
    if medallists_df.empty or 'name' not in medallists_df.columns or 'medal_type' not in medallists_df.columns:
        return go.Figure()
    
    # Count medals per athlete
    athlete_medals = medallists_df.groupby(['name', 'country']).agg({
        'medal_type': 'count'
    }).reset_index()
    athlete_medals.columns = ['name', 'country', 'total_medals']
    
    # Get medal type breakdown
    medal_breakdown = medallists_df.groupby(['name', 'medal_type']).size().unstack(fill_value=0).reset_index()
    
    # Merge
    top_athletes = athlete_medals.merge(medal_breakdown, on='name', how='left').fillna(0)
    top_athletes = top_athletes.sort_values('total_medals', ascending=False).head(n)
    
    if top_athletes.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Check for medal column names (handle both "Gold Medal" and "Gold" formats)
    gold_col = 'Gold Medal' if 'Gold Medal' in top_athletes.columns else 'Gold'
    silver_col = 'Silver Medal' if 'Silver Medal' in top_athletes.columns else 'Silver'
    bronze_col = 'Bronze Medal' if 'Bronze Medal' in top_athletes.columns else 'Bronze'
    
    if gold_col in top_athletes.columns:
        fig.add_trace(go.Bar(
            name='🥇 Gold',
            x=top_athletes['name'],
            y=top_athletes[gold_col],
            marker=dict(
                color=COLORS['gold'],
                line=dict(color=COLORS['background'], width=2)
            ),
            text=top_athletes[gold_col].astype(int),
            textposition='inside',
            textfont=dict(size=14, color='black', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>🥇 Gold: %{y}<extra></extra>'
        ))
    
    if silver_col in top_athletes.columns:
        fig.add_trace(go.Bar(
            name='🥈 Silver',
            x=top_athletes['name'],
            y=top_athletes[silver_col],
            marker=dict(
                color=COLORS['silver'],
                line=dict(color=COLORS['background'], width=2)
            ),
            text=top_athletes[silver_col].astype(int),
            textposition='inside',
            textfont=dict(size=14, color='black', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>🥈 Silver: %{y}<extra></extra>'
        ))
    
    if bronze_col in top_athletes.columns:
        fig.add_trace(go.Bar(
            name='🥉 Bronze',
            x=top_athletes['name'],
            y=top_athletes[bronze_col],
            marker=dict(
                color=COLORS['bronze'],
                line=dict(color=COLORS['background'], width=2)
            ),
            text=top_athletes[bronze_col].astype(int),
            textposition='inside',
            textfont=dict(size=14, color='black', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>🥉 Bronze: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=20, color=COLORS['paris_green'], family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Athlete',
        yaxis_title='Number of Medals',
        template='plotly_dark',
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family='Arial Black'),
        height=550,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=15, family='Arial Black'),
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor=COLORS['paris_green'],
            borderwidth=2
        ),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12)
        ),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig, top_athletes