# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/ls
import pandas as pd
import json
import plotly.express as px
from urllib.request import urlopen
from dash.dependencies import Input, Output
from app import app

df = pd.read_csv('data/clean/ds_salaries.csv')
with urlopen('https://github.com/datasets/geo-countries/blob/master/data/countries.geojson?raw=true') as response:
    geojson = json.load(response)

@app.callback(
    Output("heatmap_salary", "figure"),
    Input("filter-continent", "value"),
)
def update_heatmap_salary(selected_continents):
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]
    
    df_grouped_by_company_location = filtered_df.groupby(by=['company_location'])["salary"].mean().reset_index()
    
    heatmap_plot = px.choropleth_mapbox(
        df_grouped_by_company_location, 
        geojson=geojson, 
        locations="company_location", 
        featureidkey="properties.ADMIN",
        color="salary",
        color_continuous_scale="Viridis",
        range_color=(df_grouped_by_company_location["salary"].min(), df_grouped_by_company_location["salary"].max()),
        mapbox_style="carto-positron",
        zoom=1, center={"lat": 38.9637, "lon": 35.2433},
        opacity=0.5,
        labels={'company_location':'Country'}
    )
    heatmap_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return heatmap_plot

@app.callback(
    Output("histogram_salary", "figure"),
    Input("filter-continent", "value"),
)
def update_histogram_salary(selected_continents):
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]
    
    salary_distribution = px.histogram(
        filtered_df, 
        x="salary", 
        labels={
            "count": "Count",
            "salary": "Average Salary (USD)"
        }
    )
    
    return salary_distribution

@app.callback(
    Output("bar_chart_top_jobs", "figure"),
    Input("filter-continent", "value"),
    Input("job_title_range_slider", "value")
)
def update_bar_chart_top_jobs(selected_continents, slider_range):
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]
    
    df_grouped_by_job_title = filtered_df.groupby("job_title")["salary"].mean().reset_index().sort_values(by='salary', ascending=False)
    
    # Slice the dataframe to include only the range of job titles selected
    if slider_range:
        df_grouped_by_job_title = df_grouped_by_job_title.iloc[slider_range[0]:slider_range[1]]

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
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]
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