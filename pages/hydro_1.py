from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
shapefile_folder_months = 'data/originalData/hydro_1/ice_shields/ice_shields_2023_jan_dec/'
shapefile_folder_years = 'data/originalData/hydro_1/ice_shields/ice_shields_2007_2023/'

available_months = [
    'nic_autoc2023001n_pl_a',
    'nic_autoc2023032n_pl_a',
    'nic_autoc2023060n_pl_a',
    'nic_autoc2023091n_pl_a',
    'nic_autoc2023121n_pl_a',
    'nic_autoc2023152n_pl_a',
    'nic_autoc2023182n_pl_a',
    'nic_autoc2023213n_pl_a',
    'nic_autoc2023244n_pl_a',
    'nic_autoc2023274n_pl_a',
    'nic_autoc2023305n_pl_a',
    'nic_autoc2023335n_pl_a',
]

display_names_months = [
    'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
]

available_years = [
    'nic_autoc2007001n_pl_a',
    'nic_autoc2008001n_pl_a',
    'nic_autoc2009001n_pl_a',
    'nic_autoc2010001n_pl_a',
    'nic_autoc2011001n_pl_a',
    'nic_autoc2012001n_pl_a',
    'nic_autoc2013001n_pl_a',
    'nic_autoc2014001n_pl_a',
    'nic_autoc2015001n_pl_a',
    'nic_autoc2016001n_pl_a',
    'nic_autoc2017001n_pl_a',
    'nic_autoc2018001n_pl_a',
    'nic_autoc2019001n_pl_a',
    'nic_autoc2020001n_pl_a',
    'nic_autoc2021001n_pl_a',
    'nic_autoc2022001n_pl_a',
    'nic_autoc2023001n_pl_a',
]

display_names_years = [
    '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
    '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'
]

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------


# ...
# LAYOUT
# ...
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  
        dbc.Row(
            [
                dbc.Col(lf.make_hydro_1_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_hydro_1_settings(),
                        html.Div([
                            dbc.Button("ℹ️ Info", id="info-button_hydro_1_settings", color="primary", className="mr-1"),
                            dbc.Collapse(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.P("Das Laden der jeweiligen Eisschilde kann ein bis zwei Sekunden dauern."),
                                            html.P("Der Standard Kartenausschnitt zentriert um die norwegische Inselgruppe Spitzbergen. Der Beobachtungsraum kann jedoch auch durch klicken und ziehen auf der Karte verschoben werden."),
                                            html.P("Bei Auswahl mehrerer Monate oder Jahre kann es zu Überlappungen kommen. Um einen besseren visuellen Vergleich zu ermöglichen, lassen sich die verschiedenen Eisschilde durch anklicken hervorheben."),
                                        ],
                                        className="card-text",
                                    ),
                                ),
                                id="info-card_hydro_1_settings",
                            ),
                        ]),
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Checklist(
                                    id='month-checklist',
                                    options=[{'label': month, 'value': month} for month in display_names_months],
                                    value=[],  
                                    inline=True,
                                    style={'margin-bottom': '20px'}
                                ),
                                html.Iframe(
                                    id='map-iframe_months',
                                    style={
                                        'width': '100%',  
                                        'height': '550px',  
                                        'margin': 'auto',  
                                        'display': 'block',
                                    }
                                ),
                            ]),
                            style={'text-align': 'center'}  
                        ),
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
    [Output('month-checklist', 'options'),
     Output('map-iframe_months', 'srcDoc')],
    [Input('hydro-1-plot-selector', 'value'),
     Input('month-checklist', 'value')],
    [State('month-checklist', 'value')],
    prevent_initial_call=False  
)
def update_hydro_1_plot(selected_plot, selected_items, prev_checklist_value):
    options = []
    map_html = ""

    if selected_plot == 'months' or selected_plot is None:
        options = [{'label': month, 'value': month} for month in display_names_months]
        lf.create_static_map_html_months(selected_items, available_months, display_names_months, shapefile_folder_months)
        with open('data/originalData/hydro_1/map_with_selected_months.html', 'r') as file:
            map_html = file.read()
    elif selected_plot == 'years':
        options = [{'label': year, 'value': year} for year in display_names_years]
        lf.create_static_map_html_years(selected_items, available_years, display_names_years, shapefile_folder_years)
        with open('data/originalData/hydro_1/map_with_selected_years.html', 'r') as file:
            map_html = file.read()

    return options, map_html

@callback(
    Output("info-card_hydro_1", "style"),
    [Input("info-button_hydro_1", "n_clicks")],
    prevent_initial_call=True
)
def toggle_info_card(n_clicks):
    return {"display": "none"} if n_clicks % 2 == 0 else {"display": "block"}

@callback(
    Output('collapse_more_info_hydro_1', 'is_open'),
    Input('more_info_button_hydro_1', 'n_clicks'),
    State('collapse_more_info_hydro_1', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open

@callback(
    Output("info-card_hydro_1_settings", "style"),
    [Input("info-button_hydro_1_settings", "n_clicks")],
    prevent_initial_call=True
)
def toggle_info_card_settings(n_clicks):
    return {"display": "none"} if n_clicks % 2 == 0 else {"display": "block"}

@callback(
    Output('nic-shp-modal', 'is_open'),
    [Input('open-nic-shp-modal-button', 'n_clicks'), Input('close-nic-shp-modal-button', 'n_clicks')],
    [State('nic-shp-modal', 'is_open')]
)
def toggle_nic_shp_modal(open_n_clicks, close_n_clicks, is_open):
    if open_n_clicks or close_n_clicks:
        return not is_open
    return is_open