# Import necessary libraries and modules
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
# Load logging dataset
df = dm.process_logging_data('data/processedData/hydro_2/merged_schadholz_niederschlag.csv')

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
                dbc.Col(lf.make_hydro_2_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_hydro_2_settings(),
                        lf.make_hydro_2_info_button(),
                        html.Div([
                            dcc.Tabs([
                            dcc.Tab(label='Liniendiagramm', children=[
                            dcc.Graph(id='line-chart', figure=lf.hydro_2_line_chart(df, colors))
                            ]),
                            dcc.Tab(label='Gestapeltes Liniendiagramm', children=[
                            dcc.Graph(id='stacked-line-chart', figure=lf.hydro_2_stacked_line_chart(df, colors))
                            ]),
                            dcc.Tab(label='Gestapeltes Balkendiagramm', children=[
                            dcc.Graph(id='stacked-bar-chart', figure=lf.hydro_2_stacked_bar_chart(df, colors))
                            ]),
                        ])
                    ])
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_footer()]),
    ],
)

# ...
# Callbacks
# ...
@callback(
    Output("collapse-video", "is_open"),
    [Input("toggle-video-button", "n_clicks")],
    [State("collapse-video", "is_open")],
)
def toggle_video(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("info-card-hydro-2", "style"),
    [Input("info-button-hydro-2", "n_clicks")],
    [State("info-card-hydro-2", "style")],
)
def toggle_info_card(n, style):
    if n and n % 2:  # Wenn n ungerade ist (d.h. nach jedem ersten Klick)
        # Die Karte einblenden, indem der 'display'-Stil auf 'block' gesetzt wird
        return {"display": "block"}
    # Die Karte ausblenden, indem der 'display'-Stil auf 'none' gesetzt wird
    return {"display": "none"}

@callback(
    Output('schadholz-modal', 'is_open'),
    [Input('open-schadholz-modal-button', 'n_clicks'), Input('close-schadholz-modal-button', 'n_clicks')],
    [State('schadholz-modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output("niederschlag-modal", "is_open"),
    [Input("open-niederschlag-modal-button", "n_clicks"), Input("close-niederschlag-modal-button", "n_clicks")],
    [State("niederschlag-modal", "is_open")],
)
def toggle_niederschlag_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open