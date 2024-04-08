# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/ls
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from dash import dcc, html, Input, Output
from urllib.request import urlopen
import json

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
with urlopen('https://github.com/datasets/geo-countries/blob/master/data/countries.geojson?raw=true') as response:
    geojson = json.load(response)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server

app.layout = dbc.Container(
    [
        html.H1("DS Compensations Insights"),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Continents"),
                dcc.Dropdown(
                    id="filter-continent",
                    options=[{"label": level, "value": level} for level in df['experience_level'].unique()],
                    value=None,
                    multi=True,
                    placeholder="Select Continent(s)",
                ),
            ]), width=3)
        ], align="start", style={'paddingBottom': '10px'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id="heatmap-plot"), md=9),
            dbc.Col(dcc.Graph(id="salary-distribution"), md=3),
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
    Output("heatmap-plot", "figure"),
    Output("salary-distribution", "figure"),
    Input("filter-continent", "value"),
)
def update_graphs(selected_continents):
    filtered_df = df.copy()
    if selected_continents:
        filtered_df = filtered_df[filtered_df['experience_level'].isin(selected_continents)]
    
    currency_selection = "USD"
    salary_column = "salary_in_usd" if currency_selection == "USD" else "salary"
    
    df_grouped = df.groupby(by=['company_location'])[salary_column].mean().reset_index()
    
    heatmap_plot = px.choropleth_mapbox(
        df_grouped, 
        geojson=geojson, 
        locations="company_location", 
        featureidkey="properties.ISO_A2",
        color=salary_column,
        color_continuous_scale="Viridis",
        range_color=(df_grouped[salary_column].min(), df_grouped[salary_column].max()),
        mapbox_style="carto-positron",
        zoom=1, center={"lat": 38.9637, "lon": 35.2433},
        opacity=0.5,
        labels={'company_location':'Country'}
    )
    heatmap_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    salary_distribution = px.histogram(filtered_df, x=salary_column, title=f"Salary Distribution ({'USD' if currency_selection == 'USD' else 'Local Currency'})")
    
    return heatmap_plot, salary_distribution

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
#if __name__ == '__main__':
#    app.run(debug=False)
