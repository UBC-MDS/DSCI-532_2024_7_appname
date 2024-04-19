# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/ls
import pandas as pd
import json
import plotly.express as px
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.app import app
from src.data import df, geojson, df_grouped_by_company_location
from dash.dependencies import Input, Output
from Flask-Caching import Cache

cache = Cache(
    app.server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'tmp'
    }
)

@app.callback(
    Output("heatmap_salary", "figure"),
    Input("filter-continent", "value"),
)
@cache.memoize()
def update_heatmap_salary(selected_continents):
    if not selected_continents:
        empty_plot = px.choropleth_mapbox(
            geojson=geojson,
            locations=[],
            featureidkey="properties.ADMIN",
            color_continuous_scale="Viridis",
            mapbox_style="carto-positron",
            zoom=1, center={"lat": 38.9637, "lon": 35.2433},
            opacity=0.5
        )
        empty_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return empty_plot

    filtered_df = df_grouped_by_company_location[df_grouped_by_company_location['continent'].isin(selected_continents)][['company_location', 'salary']]
    
    heatmap_plot = px.choropleth_mapbox(
        filtered_df, 
        geojson=geojson, 
        locations="company_location", 
        featureidkey="properties.ADMIN",
        color="salary",
        color_continuous_scale="Viridis",
        range_color=(filtered_df["salary"].min(), filtered_df["salary"].max()),
        mapbox_style="carto-positron",
        zoom=1, center={"lat": 38.9637, "lon": 35.2433},
        opacity=0.5,
        labels={'mean': 'Average Salary'}
    )
    heatmap_plot.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    return heatmap_plot

@app.callback(
    Output("histogram_salary", "figure"),
    Input("filter-continent", "value"),
)
def update_histogram_salary(selected_continents):
    if selected_continents:
        filtered_df = df[df['continent'].isin(selected_continents)]
    
    salary_distribution = px.histogram(
        filtered_df, 
        x="salary", 
        labels={
            "count": "Number of Jobs",
            "salary": "Average Salary (USD)"
        }
    )

    salary_distribution.update_layout(
        yaxis_title="Number of Jobs",
        xaxis_title="Average Salary (USD)",
        xaxis=dict(autorange=False, range=[0, filtered_df['salary'].max() + 10])
    )

    median_salary = filtered_df['salary'].median()
    salary_distribution.add_vline(x=median_salary, line_dash="dash", line_color="red", 
                                  annotation_text=f'Median Salary: ${median_salary:,.2f}', 
                                  annotation_position="top",
                                  annotation_font=dict(color="red", size=12)
                                 )
    
    return salary_distribution

@app.callback(
    Output("bar_chart_top_jobs", "figure"),
    Input("filter-continent", "value"),
    Input("job_title_range_slider", "value")
)
def update_bar_chart_top_jobs(selected_continents, slider_range):
    if selected_continents:
        filtered_df = df[df['continent'].isin(selected_continents)]
    
    df_grouped_by_job_title = filtered_df.groupby("job_title")["salary"].mean().reset_index().sort_values(by='salary', ascending=False)
    
    # Slice the dataframe to include only the range of job titles selected
    if slider_range:
        df_grouped_by_job_title = df_grouped_by_job_title.iloc[slider_range[0]:slider_range[1]]

    df_grouped_by_job_title = df_grouped_by_job_title.sort_values(by='salary', ascending=True)

    bar_chart_top_jobs_plot = px.bar(
        df_grouped_by_job_title, 
        y="job_title", 
        x="salary", 
        labels={
            "job_title": "Job Title",
            "salary": "Average Salary (USD)"
        }
    )
    
    return bar_chart_top_jobs_plot

@app.callback(
    Output("job_title_range_slider", "max"),
    Output("job_title_range_slider", "value"),
    Input("filter-continent", "value"),
)
def update_range_slider(selected_continents):
    if selected_continents:
        filtered_df = df[df['continent'].isin(selected_continents)]
    job_titles = filtered_df['job_title'].unique()
    max_value = len(job_titles)
    default_range = [0, 10] if max_value >= 10 else [0, max_value] if max_value > 0 else [0, 0]
    return max_value, default_range

@app.callback(
    Output("box_plot_by_work_arrangement", "figure"),
    Input("filter-continent", "value")
)
def update_box_plot_by_work_arrangement(selected_continents):
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]
    
    box_plot_work_arrangement = px.box(
        filtered_df, 
        x="remote_ratio",
        y="salary", 
        labels={
            "remote_ratio": "Remote Ratio",
            "salary": "Average Salary (USD)"
        }
    )
   
    return box_plot_work_arrangement

@app.callback(
    Output("box_plot_by_experience", "figure"),
    Input("filter-continent", "value")
)
def update_box_plot_by_experience(selected_continents):
    if selected_continents:
        filtered_df = df[df['continent'].isin(selected_continents)]
    
    box_plot_experience = px.box(
        filtered_df, 
        x="experience_level",
        y="salary", 
        labels={
            "experience_level": "Experience",
            "salary": "Average Salary (USD)"
        },
        category_orders={
            "experience_level": ["Entry-Level", "Mid-Level", "Senior-Level", "Executive-Level"]
        }
    )

    return box_plot_experience
