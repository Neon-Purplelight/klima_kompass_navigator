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
                dbc.Col(lf.make_start_page_sidebar(), width=4),
                
                # Main content area with settings and selected graph container
                dbc.Col(
                    [
                        lf.make_start_page_2_settings(),
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

# Callback to update the selected graph based on the user's choice
@callback(
    Output('selected-graph-container', 'children'),
    Input('klima-1-plot-selector', 'value')
)
def update_selected_graph(selected_plot):
    if selected_plot == 'average_temp':
        return lf.plot_average_temp(df_temp)
    elif selected_plot == 'co2_emissions':
        return lf.plot_co2_data(df_co2)
    elif selected_plot == 'correlations':
        return lf.plot_scatter_with_ols(df_co2, df_temp)
    elif selected_plot == 'final_presentation':
        return lf.create_dual_axis_plot_bar_line(df_temp, df_co2)
    else:
        return html.Div("No graph selected")

# Callbacks for toggling the visibility of info cards and the more info section
@callback(
    Output("info-card_klima_1_co2", "style"),
    Input("info-button_klima_1_co2", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_co2(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

@callback(
    Output("info-card_klima_1_temp", "style"),
    Input("info-button_klima_1_temp", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_temp(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

@callback(
    Output("info-card_klima_1_cor", "style"),
    Input("info-button_klima_1_cor", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_cor(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

@callback(
    Output("info-card_klima_1_barplot", "style"),
    Input("info-button_klima_1_barplot", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_barplot(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

# Callback to toggle the collapse state of the more info section
@callback(
    Output('collapse_more_info_klima_1', 'is_open'),
    Input('more_info_button_klima_1', 'n_clicks'),
    State('collapse_more_info_klima_1', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open
