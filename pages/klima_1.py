# Import necessary libraries and modules
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pathlib import Path
import pandas as pd
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
# Load CO2 and continent datasets
df_co2 = dm.read_co2_data(dataFolder/'originalData/owid-co2-data.csv')
df_continents = dm.read_continental_data(dataFolder/'originalData/continents-according-to-our-world-in-data.csv')

# ------------------------------------------------------------------------------
# Perform some preprocessing
# ------------------------------------------------------------------------------
# Merge the dataframes based on 'iso_code' and 'Code'
merged_data = pd.merge(df_co2, df_continents, left_on='iso_code', right_on='Code', how='left')

# Rename columns to match the desired structure
merged_data.rename(columns={'Continent': 'continent'}, inplace=True)

# Drop unnecessary columns from the merged dataframe
merged_data.drop(['Entity', 'Code', 'Year'], axis=1, inplace=True)

# Reorder the columns
column_order = ['country', 'continent'] + [col for col in merged_data.columns if col not in ['country', 'continent']]
merged_data = merged_data[column_order]

# Filter out rows without continents
df = merged_data 

# Define the list of valid continent values
valid_continents = [
    'Africa', 'Asia', 'Europe', 'High-income countries', 'International transport',
    'Low-income countries', 'Lower-middle-income countries', 'North America', 'Oceania',
    'South America', 'Upper-middle-income countries', 'World'
]

# Filter rows based on the 'continent' column
df_filtered = df[df['continent'].isin(valid_continents)]

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------

# Define the layout structure with navigation bar, sidebar, settings, and selected graph container
def generate_default_graph():
    return lf.create_co2_treemap(df_filtered)

layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  # Navigation Bar
        dbc.Row(
            [
                dbc.Col(lf.make_klima_1_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_klima_1_settings(),
                        html.Div(id='selected-graph-container_klima_2',
                                 children=generate_default_graph())  # Set default graph content
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)

# ------------------------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------------------------

# Callback to update the selected graph based on the user's choice
@callback(
    Output('selected-graph-container_klima_2', 'children'),
    Input('klima-2-plot-selector', 'value'),
    prevent_initial_call=True
)
def update_selected_graph(selected_plot):
    if selected_plot == 'co2_emissions_per_country':
        return lf.create_co2_treemap(df_filtered), False
    elif selected_plot == 'co2_emissions_historic':
        return lf.create_co2_treemap_historic(df_filtered), False
    elif selected_plot == 'co2_emissions_per_capita':
        return lf.create_co2_treemap_per_capita(df_filtered), False
    else:
        return html.Div("No graph selected"), False

# Callbacks for toggling the visibility of info cards and the more info section
@callback(
    Output("info-card_klima_2_co2_treemap", "style"),
    Input("info-button_klima_2_co2_treemap", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_treemap_co2(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

@callback(
    Output("info-card_klima_2_historic_treemap", "style"),
    Input("info-button_klima_2_historic_treemap", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_treemap_historic(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

@callback(
    Output("info-card_klima_2_per_capita_treemap", "style"),
    Input("info-button_klima_2_per_capita_treemap", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_treemap_per_capita(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

# Callback to toggle the collapse state of the more info section
@callback(
    Output('collapse_more_info_klima_2', 'is_open'),
    Input('more_info_button_klima_2', 'n_clicks'),
    State('collapse_more_info_klima_2', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open



