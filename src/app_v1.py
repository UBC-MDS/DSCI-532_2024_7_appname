# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import datetime
from dash import dcc, html, Input, Output
import altair as alt
import top_job_bar_chart

df = pd.read_csv('../data/raw/ds_salaries.csv')
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
df['continent'] = df['company_location'].map(iso3166_to_continent)
df['remote_ratio'] = df['remote_ratio'].replace({100: 'Full-Remote', 50: 'Hybrid', 0:'In-Person'})
df['experience_level'] = df['experience_level'].replace({'EN': 'Entry-Level', 'SE': 'Lower-Middle', 'MI':'Mid-Level', 'EX': 'Executive-Level'})
df['employment_type'] = df['employment_type'].replace({'FT': 'Full-Time', 'PT': 'Part-Time', "FL":'Freelance', "CT": "Contract"})


current_date = datetime.datetime.now().strftime("%B %d, %Y")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        html.H1("DS Compensations Insights"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Label("Continent"),
                    dcc.Dropdown(
                        id="filter-continent",
                        options=[{"label": level, "value": level} for level in df['continent'].unique()],
                        value=None,
                        multi=True,
                        placeholder="All",
                    ),
                ]), md=3),
            
            dbc.Row([
                dbc.Col(dcc.Graph(id="map_plot")),
                dbc.Col(dcc.Graph(id="salary-distribution")),
            ]),

            dbc.Row([
                dbc.Col(dcc.Graph(id="box_plot_by_experience")),
                dbc.Col(dcc.Graph(id="box_plot_by_work_arrangement")), 
                dbc.Col([
                    html.Div([
                        dcc.Graph(id='top-jobs-bar-chart'),
                    dcc.Slider(
                        id='point-slider',
                        min=0,
                        max=10,
                        step=1,
                        value=0,
                        marks={i: str(i) for i in range(10)}
                    )
                    ])
                ])
            ])
        ]),
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

#if __name__ == '__main__':
#    app.run_server(debug=True, host='127.0.0.1')
if __name__ == '__main__':
    app.run(debug=False)
