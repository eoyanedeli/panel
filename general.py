## Dash

import dash
from dash import no_update
# import jupyter_dash
from dash import Dash, dash_table, dcc, callback, Output, Input, html
import dash_daq as daq

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

import plotly.express as px
import plotly.graph_objects as go

# import math

import pandas as pd

import sqlite3, base64


from datetime import datetime
from datetime import timedelta


# jupyter_dash.default_mode="external"

conn = sqlite3.connect('https://github.com/eoyanedeli/panel/raw/main/students.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM hitos")
my_data = cursor.fetchall()
conn.close()

current_date = datetime.now().date()

df = pd.DataFrame([{'Hito': task[1], 'Inicio': task[2], 'Término': task[3], 'Persona a cargo': task[4], 'Porcentaje': task[5]} for task in my_data[:10]])

from random import randint
df_pc = pd.DataFrame([{'Plataforma' : f'plataforma_{i}', 'Documentación' : randint(0,10)} for i in range(1,9)])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

fig_1 = px.timeline(
    df,
    x_start = "Inicio",
    x_end = "Término",
    y = "Hito",
    title = "Hitos",
    color = 'Porcentaje',
    color_continuous_scale = 'rdylgn',
    range_color = [20,100]
)

fig_2 = px.timeline(
    df,
    x_start = "Inicio",
    x_end = "Término",
    y = "Hito",
    title = "VPN",
    color = 'Porcentaje',
    color_continuous_scale = 'rdylgn',
    range_color = [20,100]
)

fig_1.add_shape(
    go.layout.Shape(
        type="line",
        x0=current_date,
        x1=current_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", width=2)
    )
)

fig_2.add_shape(
    go.layout.Shape(
        type="line",
        x0=current_date,
        x1=current_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", width=2)
    )
)

server = app.server

app.layout = dbc.Container([
    html.Div(className='row', children='Panel de control de licitaciones.',
             style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}),
    html.Div(className='row', children='Resumen.',
             style={'textAlign': 'center', 'color': 'black', 'fontSize': 25}),
    html.Div(className='row', children=[
            dbc.Button('Resumen', id='button-resumen', style={'width': '100px', 'height': '40px'}),
            dbc.Button('VPN', id='button-vpn', style={'width': '100px', 'height': '40px'}),
            dbc.Button('Hitos', id='button-hitos', style={'width': '100px', 'height': '40px'}),
            dbc.Button('Informes', id='button-informes', style={'width': '100px', 'height': '40px'}),
            dbc.Button('Pagos', id='button-pagos', style={'width': '100px', 'height': '40px'}),
            dbc.Button('Documentación', id='button-documentacion', style={'width': '150px', 'height': '40px'}),
            dcc.Dropdown(
                id='seleccion-de-plataforma',
                options=[
                    {'label': 'General', 'value': 'general'},
                    {'label': 'Centros', 'value': 'centros'},
                    {'label': 'DataCiencia', 'value': 'dataciencia'},
                    {'label': 'ISSN', 'value': 'issn'},
                    {'label': 'Latindex', 'value': 'latindex'},
                    {'label': 'Portal del Investigador', 'value': 'pdi'},
                    {'label': 'Repositorio', 'value': 'repositorio'},
                    {'label': 'Scielo', 'value': 'scielo'},
                    {'label': 'Territorios', 'value': 'territorios'},
                ],
                value='general',
                style={'width': '300px', 'margin-left': '20px'}
            ),
        ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                figure = fig_1,
                style = {'height': '400px', 'width': '600px'}
            ),
            width = 6
        ),
        dbc.Col(
            dcc.Graph(
                figure = fig_2,
                style = {'height': '400px', 'width': '600px'}
            ),
            width = 6
        )
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Br(),
            html.Div(
                children='Panel de control de licitaciones.',
                style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}
            ),
            html.Center(
                daq.Gauge(
                    min=0,
                    max=10,
                    value=6,
                    color=theme['primary'],
                    id='darktheme-daq-gauge',
                    className='dark-theme-control'
                )
            )
        ],
            width = 6
        ),
        dbc.Col(
            dcc.Graph(
                figure = px.pie(
                    df_pc,
                    values = 'Documentación',
                    names = 'Plataforma',
                    title = 'Documentación por plataforma'
                ),
                style = {'height': '400px', 'width': '600px'}
            ),
            width = 4
        )
    ])
])

# @app.callback(

# )

# def update_output():
#     return

# if __name__ == '__main__':
#     app.run_server(debug=True)

if __name__ == '__main__':
    try:
        app.run_server(port=8050, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")