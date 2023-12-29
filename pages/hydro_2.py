# Import necessary libraries and modules
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
# Define the full path of the data folder to load raw data
dataFolder = Path(__file__).parent.parent.absolute() / 'data'

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
# Load temperature and CO2 datasets
df_temp = dm.read_temp_data(dataFolder/'originalData/GLB.Ts+dSST.csv')
df_co2 = dm.read_co2_data(dataFolder/'originalData/owid-co2-data.csv')

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------
# Preprocess CO2 data
df_co2 = dm.preprocess_co2_data(df_co2)
# Uncomment the line below if temperature data preprocessing is required
# df_temp = dm.preprocess_temperature_data(df_temp)

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
                        html.Div(id='selected-graph-container', style={'height': '100vh'})
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
