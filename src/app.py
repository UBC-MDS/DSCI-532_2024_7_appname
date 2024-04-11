import dash
import dash_bootstrap_components as dbc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.layouts import layout

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server  # Expose server for deployments
app.layout = layout

from src.callbacks import *

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
#if __name__ == '__main__':
#    app.run(debug=False)
