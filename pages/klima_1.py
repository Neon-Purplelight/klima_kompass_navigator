from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pathlib import Path
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
dataFolder = Path(__file__).parent.parent.absolute() / 'data'

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
df_temp = dm.read_temp_data(dataFolder/'originalData/GLB.Ts+dSST.csv')
df_co2 = dm.read_co2_data(dataFolder/'originalData/owid-co2-data.csv')

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------
df_co2 = dm.preprocess_co2_data(df_co2)
#df_temp = dm.preprocess_temperature_data(df_temp)

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------

# Main layout structure with navigation bar, sidebar, settings, and selected graph container
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  
        dbc.Row(
            [
                # Sidebar for the klima-1 page
                dbc.Col(lf.make_klima_1_sidebar(), width=4),
                
                # Main content area with settings and selected graph container
                dbc.Col(
                    [
                        lf.make_klima_1_settings(),
                        html.Div(id='selected-graph-container', style={'height': '100vh'})
                    ],
                    width=8,
                ),
            ]
        ),
        
        # Row containing the Creative Commons license banner
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)

# ...
# Callbacks
# ...

