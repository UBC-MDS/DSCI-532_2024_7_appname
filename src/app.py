import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, Input, Output

df = pd.read_csv('../data/raw/ds_salaries.csv')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        html.Div([
            dbc.Label("Experience Level"),
            dcc.Dropdown(
                id="filter-experience-level",
                options=[{"label": level, "value": level} for level in df['experience_level'].unique()],
                value=None,
                multi=True,
                placeholder="Select Experience Level(s)",
            ),
        ]),
        html.Div([
            dbc.Label("Employment Type"),
            dcc.Dropdown(
                id="filter-employment-type",
                options=[{"label": emp_type, "value": emp_type} for emp_type in df['employment_type'].unique()],
                value=None,
                multi=True,
                placeholder="Select Employment Type(s)",
            ),
        ]),
        html.Div([
            dbc.Label("Job Title"),
            dcc.Dropdown(
                id="filter-job-title",
                options=[{"label": title, "value": title} for title in df['job_title'].unique()],
                value=None,
                multi=True,
                placeholder="Select Job Title(s)",
            ),
        ]),
        html.Div([
            dbc.Label("Company Location"),
            dcc.Dropdown(
                id="filter-company-location",
                options=[{"label": location, "value": location} for location in df['company_location'].unique()],
                value=None,
                multi=True,
                placeholder="Select Company Location(s)",
            ),
        ]),
        html.Div([
            dbc.Label("Salary Currency"),
            dcc.RadioItems(
                id="currency-selection",
                options=[
                    {"label": "USD", "value": "USD"},
                    {"label": "Local Currency", "value": "Local"},
                ],
                value="USD",
                inline=True,
            ),
        ]),
        html.Div([
            dbc.Label("Company Size"),
            dcc.Dropdown(
                id="company-size",
                options=[
                    {"label": "Small", "value": "S"},
                    {"label": "Medium", "value": "M"},
                    {"label": "Large", "value": "L"},
                ],
                value=None,
                multi=True,
                placeholder="Select Company Size",
            ),
        ]),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("DS Compensations Insights"),
        html.Hr(),
        dbc.Row([
            dbc.Col(controls, md=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col(dcc.Graph(id="scatter-plot"), md=6),
                    dbc.Col(dcc.Graph(id="avg-salary-by-job-title"), md=6),
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id="salary-distribution"), md=6),
                    dbc.Col(dcc.Graph(id="salary-by-company-location"), md=6),
                ]),
            ], md=9),
        ], align="start"),
    ],
    fluid=True,
)

@app.callback(
    [
        Output("scatter-plot", "figure"),
        Output("avg-salary-by-job-title", "figure"),
        Output("salary-distribution", "figure"),
        Output("salary-by-company-location", "figure"),
    ],
    [
        Input("filter-experience-level", "value"),
        Input("filter-employment-type", "value"),
        Input("filter-job-title", "value"),
        Input("filter-company-location", "value"),
        Input("currency-selection", "value"),
        Input("company-size", "value")
    ]
)
def update_graphs(selected_experience_levels, selected_employment_types, selected_job_titles, selected_company_locations, currency_selection, selected_company_sizes):
    filtered_df = df.copy()
    if selected_experience_levels:
        filtered_df = filtered_df[filtered_df['experience_level'].isin(selected_experience_levels)]
    if selected_employment_types:
        filtered_df = filtered_df[filtered_df['employment_type'].isin(selected_employment_types)]
    if selected_job_titles:
        filtered_df = filtered_df[filtered_df['job_title'].isin(selected_job_titles)]
    if selected_company_locations:
        filtered_df = filtered_df[filtered_df['company_location'].isin(selected_company_locations)]
    
    if selected_company_sizes:
        filtered_df = filtered_df[filtered_df['company_size'].isin(selected_company_sizes)]
    
    salary_column = "salary_in_usd" if currency_selection == "USD" else "salary"
    
    fig_size = {'height': 350, 'width': 550}
    
    scatter_plot = px.scatter(filtered_df, x="experience_level", y=salary_column, color="employment_type", title=f"Salary by Experience Level ({'USD' if currency_selection == 'USD' else 'Local Currency'})", **fig_size)
    
    avg_salary_by_job_title_df = filtered_df.groupby("job_title")[salary_column].mean().reset_index()
    avg_salary_by_job_title_df = avg_salary_by_job_title_df.sort_values(by=salary_column, ascending=False)
    avg_salary_by_job_title = px.bar(
        avg_salary_by_job_title_df, 
        x="job_title", 
        y=salary_column, 
        title=f"Avg Salary by Job Title ({'USD' if currency_selection == 'USD' else 'Local Currency'})", 
        **fig_size
    )
    avg_salary_by_job_title.update_layout(
        title={'text': f"Avg Salary by Job Title ({'USD' if currency_selection == 'USD' else 'Local Currency'})", 'font': {'size': 16}},
        xaxis=dict(title='Job Title', title_font={'size': 14}, tickfont={'size': 9}),
        yaxis=dict(title='Salary', title_font={'size': 14}, tickfont={'size': 12}),
        #xaxis_tickangle=45
    )
    
    salary_distribution = px.histogram(filtered_df, x=salary_column, title=f"Salary Distribution ({'USD' if currency_selection == 'USD' else 'Local Currency'})", **fig_size)
    
    salary_by_company_location = px.box(filtered_df, x="company_location", y=salary_column, title=f"Salary by Company Location ({'USD' if currency_selection == 'USD' else 'Local Currency'})", **fig_size)
    #salary_by_company_location.update_layout(xaxis_tickangle=45)
    
    return scatter_plot, avg_salary_by_job_title, salary_distribution, salary_by_company_location

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
