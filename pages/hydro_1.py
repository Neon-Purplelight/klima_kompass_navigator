# Import necessary libraries and modules
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
# Define the full path of the data folder to load raw data
shapefile_folder_months = 'data/originalData/ice_shields/ice_shields_2023_jan_dec/'
shapefile_folder_years = 'data/originalData/ice_shields/ice_shields_2007_2023/'

# Liste der verfügbaren Monate
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

# Liste der Anzeigenamen für die Checkbox
display_names_months = [
    'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
]

# Liste der verfügbaren Jahre
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

# Liste der Anzeigenamen für die Checkbox
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
# Define the layout structure with navigation bar, sidebar, settings, and selected graph container
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  # Navigation Bar
        dbc.Row(
            [
                dbc.Col(lf.make_klima_1_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_hydro_1_settings(),
                        # Move the card with month checklist here
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Wähle Monate aus", className="card-title"),
                                dbc.Checklist(
                                    id='month-checklist',
                                    options=[{'label': month, 'value': month} for month in display_names_months],
                                    value=[],  # Keine Auswahl standardmäßig
                                    inline=True,
                                    style={'margin-bottom': '20px'}
                                ),
                                html.Iframe(
                                    id='map-iframe_months',
                                    style={
                                        'width': '100%',  # Set the width to 100%
                                        'height': '550px',  # Set the height to your desired value
                                        'margin': 'auto',  # Center the iframe
                                        'display': 'block',
                                    }
                                ),
                            ]),
                            style={'text-align': 'center'}  # Center the content within the card
                        ),
                    ],
                    width=8,
                ),
            ]
        ),
        # License banner at the bottom
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)




# ...
# Callbacks
# ...
# Callback to update the selected graph based on the user's choice
@callback(
    Output('map-iframe_months', 'srcDoc'),
    [Input('month-checklist', 'value')]
)
def update_map(selected_items):
    # Use the create_static_map_html_years function to generate the HTML content
    lf.create_static_map_html_months(selected_items, available_months, display_names_months, shapefile_folder_months)
    # Read the generated HTML content and return it
    with open('data\originalData\map_with_selected_months.html', 'r') as file:        
        map_html = file.read()

    return map_html