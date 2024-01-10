from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import dataManager as dm
from utils import layoutFunctions as lf
from dash import dcc
from dash.dependencies import Input, Output, State
import os
import base64
from dash_extensions import BeforeAfter
import dash_bootstrap_components as dbc
import dash

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
# Define the full path of the data folder to load raw data
dataFolder = Path(__file__).parent.parent.absolute() / 'assets/batagaika_crater'

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
# Daten für die Satellitenbilder
satellite_data = [
    {'label': '13.08.1991', 'value': '19910813_Crater.png'},
    {'label': '27.08.1999', 'value': '19990827_Crater.png'},
    {'label': '20.08.2005', 'value': '20050820_Crater.png'},
    {'label': '15.06.2010', 'value': '20100615_Crater.png'},
    {'label': '11.07.2014', 'value': '20140711_Crater.png'},
    {'label': '07.08.2018', 'value': '20180807_Crater.png'},
    {'label': '10.08.2022', 'value': '20220810_Crater.png'},
    {'label': '11.08.2022', 'value': '20220811_Crater.png'},
]

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------

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
                            html.H1("Batagaika Krater Bilder"),
                            dcc.Tabs([
                                dcc.Tab(label='Zeitraffer', children=[
                                    html.Div([
                                        # Play, Stopp und Vorwärts-Buttons über dem Iframe
                                        html.Div([
                                            html.Button('Play', id='play-button', n_clicks=0, style={'margin-right': '10px'}),
                                            html.Button('Stopp', id='stop-button', n_clicks=0, style={'display': 'none', 'margin-right': '10px'}),
                                            html.Button('Vorwärts', id='next-button', n_clicks=0),
                                        ], style={'text-align': 'center', 'margin-top': '10px'}),
                                        # Iframe für die Anzeige des Bildes
                                        html.Iframe(id='image-display', style={'width': '80%', 'height': '80vh', 'border': 'none'}),
                                        # Intervall für die Play-Funktion
                                        dcc.Interval(id='play-interval', interval=300, n_intervals=0, disabled=True),
                                    ], style={'text-align': 'center'}),
                                ]),

                                dcc.Tab(label='Vergleich', children=[
                                    dbc.Container([
                                        dbc.Row(
                                            dbc.Col(html.H1("Vorher- Nachher Vergleich", style={'textAlign': 'center'}), width=12)
                                        ),
                                        html.Hr(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.H2("Aufnahme für Vorher-Vergleich auswählen"),
                                                dcc.RadioItems(
                                                    id='before-radio',
                                                    options=[
                                                        {'label': data['label'], 'value': data['value']} for data in satellite_data
                                                    ],
                                                    value='19910813_Crater.png',
                                                    labelStyle={'display': 'block'},
                                                ),
                                            ], width=3),
                                            dbc.Col([
                                                BeforeAfter(id='image-slider', width=612, height=512, defaultProgress=0.5),
                                            ], width=6),
                                            dbc.Col([
                                                html.H2("Aufnahme für Nachher-vergleich auswählen"),
                                                dcc.RadioItems(
                                                    id='after-radio',
                                                    options=[
                                                        {'label': data['label'], 'value': data['value']} for data in satellite_data
                                                    ],
                                                    value='20220811_Crater.png',
                                                    labelStyle={'display': 'block'},
                                                ),
                                            ], width=3),
                                        ]),
                                    ]),
                                ]),
                            ]),
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
# Callbacks für die Interaktivität des Dashboards
@callback(
    Output('image-display', 'srcDoc'),
    Output('play-button', 'style'),
    Output('stop-button', 'style'),
    Input('play-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    Input('next-button', 'n_clicks'),
    Input('play-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_image(n_clicks_play, n_clicks_stop, n_clicks_next, n_intervals):
    ctx = dash.callback_context
    trigger_id = ctx.triggered_id
    changed_id = trigger_id.split('.')[0] if trigger_id else None

    if changed_id == 'play-interval':
        # Automatisches Abspielen der Bilder
        selected_index = n_intervals % len(satellite_data)
    elif changed_id == 'play-button':
        # Manuelle Navigation durch die Bilder (Play)
        selected_index = n_clicks_play % len(satellite_data)
    elif changed_id == 'stop-button':
        # Stoppen des Abspielens
        selected_index = n_clicks_stop % len(satellite_data)
    elif changed_id == 'next-button':
        # Manuelle Navigation durch die Bilder (Vorwärts)
        selected_index = n_clicks_next % len(satellite_data)
    else:
        # Standardmäßig das erste Bild anzeigen
        selected_index = 0

    selected_data = satellite_data[selected_index]
    image_path = os.path.join(dataFolder, selected_data['value'])

    # Umwandlung des Bilds in ein base64-codiertes Bild
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')

    # Erstellen Sie den HTML-Code für das iframe mit dynamischer Größe und Datum
    iframe_code = f'''
        <div style="position: relative;">
            <img src="data:image/png;base64,{encoded_image}" style="width:80%; height:80vh;">
            <div style="position: absolute; top: 10px; right: 300px; font-size: 18px; color: black; background-color: white; padding: 5px; z-index: 1;">{selected_data['label']}</div>
        </div>
    '''

    # Anzeigen/Verstecken von Play/Stopp-Buttons je nach Status
    play_style = {'display': 'none'} if n_intervals > 0 else {'display': 'inline-block'}
    stop_style = {'display': 'inline-block'} if n_intervals > 0 else {'display': 'none'}

    return iframe_code, play_style, stop_style

# Callback für die Play-Funktion (Intervall)
@callback(
    Output('play-interval', 'disabled'),
    Output('play-interval', 'n_intervals'),
    Input('play-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    State('play-interval', 'n_intervals')
)
def update_play_interval(n_clicks_play, n_clicks_stop, n_intervals_play):
    ctx = dash.callback_context
    trigger_id = ctx.triggered_id

    if trigger_id and trigger_id.split('.')[0] == 'play-button' and n_clicks_play > 0 and n_intervals_play == 0:
        # Starten des Intervalls nur beim ersten Klick auf den Play-Button
        return False, 0
    elif trigger_id and trigger_id.split('.')[0] == 'stop-button':
        # Stoppen des Intervalls nur beim Klick auf den Stopp-Button
        return True, 0
    else:
        # Lassen Sie das Intervall unverändert
        return n_intervals_play > 0, n_intervals_play

# Callback für den Vorher-Nachher-Vergleich
@callback(
    Output('image-slider', 'after'),
    Output('image-slider', 'before'),
    Input('before-radio', 'value'),
    Input('after-radio', 'value')
)
def update_images(before_image, after_image):
    return f'assets/batagaika_crater/{before_image}', f'assets/batagaika_crater/{after_image}'