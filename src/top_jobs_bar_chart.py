import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import datetime
from dash import dcc, html, Input, Output
import altair as alt
import top_job_bar_chart

@app.callback(
    Output('top_jobs_bar_chart', 'figure'),
    [
        Input("filter-continent", "value"),
        Input("point-slider", "value"),
    ]
)
def updated_chart(selected_continent, selected_top_n):
    print(selected_continent, selected_top_n)
    filtered_df = df.copy()
    if selected_continent:
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continent)]
        average_salaries = pd.DataFrame(filtered_df.groupby('job_title')['salary_in_usd'].mean())
        sorted_df = average_salaries.sort_values(by='salary_in_usd', ascending=False)
        top_n = sorted_df.head(selected_top_n).reset_index()

    fig = px.bar(top_n, x='salary_in_usd', y='job_title', orientation='h',
                 title=f'The top {selected_top_n} Highest Paying Jobs',
                 labels={'salary_in_usd': 'Average Salary (USD)', 'job_title': 'Job Title'})
    return fig

    # updated_chart = alt.Chart(top_n).mark_bar().encode(
    #     y= alt.Y('job_title:N', sort='-x', title='Job Title'),  
    #     x= alt.X('salary_in_usd:Q', title='Average Salary (USD)'),
    #     tooltip=[
    #         alt.Tooltip('salary_in_usd:Q', title='Average Salaries (USD)'),
    #         alt.Tooltip('job_title:N', title='Job Title')
    #     ] 
    # ).properties(
    #     title=f'Top {selected_top_n} Highest Paying Jobs')
        
    # return av.display(updated_chart.to_json(), inline=False)