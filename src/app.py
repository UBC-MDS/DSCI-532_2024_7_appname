# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from dash import dcc, html, Input, Output

df = pd.read_csv('data/raw/ds_salaries.csv')

# Data Wrangling
iso3166_to_continent = {
    'DE': 'Europe',
    'JP': 'Asia',
    'GB': 'Europe',
    'HN': 'North America',
    'US': 'North America',
    'HU': 'Europe',
    'NZ': 'Oceania',
    'FR': 'Europe',
    'IN': 'Asia',
    'PK': 'Asia',
    'CN': 'Asia',
    'GR': 'Europe',
    'AE': 'Asia',
    'NL': 'Europe',
    'MX': 'North America',
    'CA': 'North America',
    'AT': 'Europe',
    'NG': 'Africa',
    'ES': 'Europe',
    'PT': 'Europe',
    'DK': 'Europe',
    'IT': 'Europe',
    'HR': 'Europe',
    'LU': 'Europe',
    'PL': 'Europe',
    'SG': 'Asia',
    'RO': 'Europe',
    'IQ': 'Asia',
    'BR': 'South America',
    'BE': 'Europe',
    'UA': 'Europe',
    'IL': 'Asia',
    'RU': 'Europe',
    'MT': 'Europe',
    'CL': 'South America',
    'IR': 'Asia',
    'CO': 'South America',
    'MD': 'Europe',
    'KE': 'Africa',
    'SI': 'Europe',
    'CH': 'Europe',
    'VN': 'Asia',
    'AS': 'Oceania',
    'TR': 'Asia',
    'CZ': 'Europe',
    'DZ': 'Africa',
    'EE': 'Europe',
    'MY': 'Asia',
    'AU': 'Oceania',
    'IE': 'Europe'
}
df_country_continent = pd.DataFrame.from_dict(iso3166_to_continent, orient='index', columns=['Continent'])
df_country_continent = df_country_continent.reset_index()
df_country_continent.columns = ['Code', 'Continent']
df = pd.merge(df, df_country_continent, left_on='company_location', right_on='Code', how='left')
df = df.drop('Code', axis=1, inplace=True)

def data_mapping_replace(df, col_name, dict):
    df[col_name] = df[col_name].replace(dict)

data_mapping_replace(df, "remote_ratio", {100: 'Full-Remote', 50: 'Hybrid', 0:'In-Person'})
data_mapping_replace(df, "experience_level", {'EN': 'Entry-Level', 'SE': 'Lower-Middle', 'MI':'Mid-Level', 'EX': 'Executive-Level'})
data_mapping_replace(df, "employment_type", {'FT': 'Full-Time', 'PT': 'Part-Time', "FL":'Freelance', "CT": "Contract"})

current_date = datetime.datetime.now().strftime("%B %d, %Y")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

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
        html.Footer([
            html.Hr(style={'borderTop': '1px solid #ccc', 'marginBottom': '10px'}),
            html.P("This app provides data-driven insights into data science compensation. Created by Dan Zhang, Doris Cai, Joradn Cairns, Sho Inagaki.", 
                style={'fontSize': '12px', 'margin': '0', 'padding': '2px 0'}),
            html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_7_ds-compensation", target="_blank", 
                style={'fontSize': '10px', 'display': 'block', 'margin': '0', 'padding': '2px 0'}),
            html.P(f"Last updated: {current_date}", 
                style={'fontSize': '8px', 'margin': '0', 'padding': '2px 0'})
        ], style={'textAlign': 'center', 'marginTop': '20px', 'paddingTop': '10px', 'paddingBottom': '10px'})
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
        Input("company-size", "value")
    ]
)
def update_graphs(selected_experience_levels, selected_employment_types, selected_job_titles, selected_company_locations, selected_company_sizes):
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
    
    currency_selection = "USD"
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

#if __name__ == '__main__':
#    app.run_server(debug=True, host='127.0.0.1')
if __name__ == '__main__':
    app.run(debug=False)
