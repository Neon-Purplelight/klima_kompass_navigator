# Import necessary libraries and modules
from dash import html, dcc
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
# Load logging dataset
df = dm.process_logging_data('data/originalData/holzeinschlag-wetter.csv')

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------
# Farben festlegen
colors = {
    'Insekten': 'darkblue',
    'Wind/Sturm': 'steelblue',
    'Schnee/Duft': 'lightblue',
    'Sonstige Ursachen': 'gray',
    'Trockenheit': 'red'
}

# Gesamtdaten berechnen und runden
df['Gesamt'] = df[['Insekten', 'Wind/Sturm', 'Schnee/Duft', 'Sonstige Ursachen', 'Trockenheit']].sum(axis=1)
df = df.round(2)

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------
# Define the layout structure with navigation bar, sidebar, settings, and selected graph container
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  # Navigation Bar
        dbc.Row(
            [
                dbc.Col(lf.make_klima_1_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_klima_1_settings(),
                        html.Div([
                            dcc.Tabs([
                            dcc.Tab(label='Liniendiagramm', children=[
                                dcc.Graph(id='line-chart', figure=lf.hydro_2_line_chart(df, colors))
                            ]),
                            dcc.Tab(label='Gestapeltes Balkendiagramm', children=[
                                dcc.Graph(id='stacked-bar-chart', figure=lf.hydro_2_stacked_bar_chart(df, colors))
                            ]),
                            dcc.Tab(label='Gestapeltes Liniendiagramm', children=[
                                dcc.Graph(id='stacked-line-chart', figure=lf.hydro_2_stacked_line_chart(df, colors))
                            ])
                        ])
                    ])
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)

# ...
# Callbacks
# ...
