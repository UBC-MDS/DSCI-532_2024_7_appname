import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv('../data/raw/ds_salaries.csv')
employment_type_mapping = {
    'FT': 'Full-Time',
    'PT': 'Part-Time',
    'CT': 'Contract',
    'FL': 'Freelance'
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("DS Compensation"),
            dcc.Dropdown(
                id='job-title-dropdown',
                options=[{'label': jt, 'value': jt} for jt in df['job_title'].unique()],
                value=df['job_title'].unique()[0],
                multi=True
            ),
            dcc.Dropdown(
                id='company-location-dropdown',
                options=[{'label': continent, 'value': continent} for continent in df['company_location'].unique()],
                value=df['company_location'].unique()[0],
                clearable=False
            ),
            dcc.Dropdown(
                id='experience-level-dropdown',
                options=[{'label': continent, 'value': continent} for continent in df['experience_level'].unique()],
                value=df['experience_level'].unique()[0],
                clearable=False
            ),
            dcc.RadioItems(
                id='employment-type-radio',
                options=[{'label': employment_type_mapping.get(et, et), 'value': et} for et in df['employment_type'].unique()],
                value=df['employment_type'].unique()[0],
            ),
            dcc.RadioItems(
                id='currency-type-radio',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'Local Currency', 'value': 'LOCAL'}
                ],
                value='USD'
            ),
            dbc.ButtonGroup(
                [dbc.Button("S", id="btn-small"), dbc.Button("M", id="btn-medium"), dbc.Button("L", id="btn-large")],
                size="lg"
            ),
            dcc.Slider(
                id='remote-ratio-slider',
                min=0,
                max=100,
                step=1,
                value=70
            ),
        ], width=3, class_name="h-100 d-inline-block"),
        dbc.Col([
            dcc.Graph(
                id='salary-distribution-pie',
                figure=px.pie(df, values='salary_in_usd', names='company_location', title='Salary Group Distribution')
            )
        ], width=9, class_name="h-100 d-inline-block"),
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')