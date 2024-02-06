from dash import html, Output, Input, State, callback
import dash_bootstrap_components as dbc
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------

# Main layout structure with navigation bar, sidebar, interactive controls, and license banner.
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  
        dbc.Row(
            [
                # Sidebar for the start page
                dbc.Col(lf.make_start_page_1_sidebar(), width=4),
                
                # Main content area with interactive controls and iframe
                dbc.Col(
                    [
                        lf.make_interactive_controls_example(),
                        lf.make_iframe(),  
                    ],
                    width=8,
                ),
            ]
        ),
        
        # Row containing the Creative Commons license banner
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
    # Styling for the background image
    style={
        'background-image': 'url("/assets/wallpaper.jpg")',
        'background-size': 'cover', 'background-repeat': 'no-repeat',
        'background-position': 'center',
        'height': '120vh', 'margin': 0
    },
)

# ...
# Callbacks
# ...

# Callback for toggling the visibility of the info card iframe on the start page
@callback(
    Output("info-card_start_page_iframe", "style"),
    Input("info-button_start_page_iframe", "n_clicks"),
    prevent_initial_call=True
)
def toggle_info_card_iframe(n_clicks):
    if n_clicks is None:
        return {"display": "none"}
    elif n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {}

# Callback for toggling the collapse state of more info section on the start page
@callback(
    Output('collapse_more_info_start_page', 'is_open'),
    Input('more_info_button_start_page', 'n_clicks'),
    State('collapse_more_info_start_page', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open
