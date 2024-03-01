from dash import html, Output, Input, State, callback
import dash_bootstrap_components as dbc
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------

# Welcome Modal
welcome_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.H2("Willkommen auf dem Klima-Kompass-Navigator", style={'font-size': '28px', 'color': 'black'})),
        dbc.ModalBody(
            html.P(
                [
                    "Der Klima-Kompass-Navigator ist eine Sammlung verschiedener Dashboards, die sich mit dem Klimawandel "
                    "und seinen Auswirkungen auf die Umwelt auseinandersetzen. Der Grundaufbau der jeweiligen Dashboards "
                    "ist dabei immer derselbe. Über die Navigationsleiste am oberen Bildschirmrand können Sie zwischen den "
                    "thematischen Hauptseiten Klimatologie (Luft), Hydrologie (Wasser) und Pedologie (Böden) wechseln. Über eine weitere Navigationsleiste oberhalb "
                    "des Informationsbereichs am linken Bildschirmrand können Sie weiter zwischen verschiedenen Unterkategorien "
                    "wechseln. Diese Einführungsseite enthält weitere Informationen zum Verständnis der wichtigsten Funktionen."
                ]
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Okay", id="close-welcome-modal-button", className="ms-auto", n_clicks=0)
        ),
    ],
    id="welcome-modal",
    is_open=True,
    size="xl",
)

# Layout
layout = html.Div(
    [
        welcome_modal,
        dbc.Row(lf.make_NavBar()),
        dbc.Row(
            [
                dbc.Col(lf.make_start_page_1_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_interactive_controls_example(),
                        lf.make_iframe(),
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_footer()]),
    ],
    style={
        'background-image': 'url("/assets/wallpaper.jpg")',
        'background-size': 'cover', 'background-repeat': 'no-repeat',
        'background-position': 'center',
        'height': '150vh', 'margin': 0
    },
)

# Callbacks
@callback(
    Output('welcome-modal', 'is_open'),
    [Input('close-welcome-modal-button', 'n_clicks')],
    [State('welcome-modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_welcome_modal(n_clicks, is_open):
    if n_clicks > 0:
        return not is_open
    return is_open

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

@callback(
    Output('collapse_more_info_start_page', 'is_open'),
    Input('more_info_button_start_page', 'n_clicks'),
    State('collapse_more_info_start_page', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open

@callback(
    Output('mcc-carbon-clock-modal', 'is_open'),
    [Input('open-mcc-carbon-clock-modal-button', 'n_clicks'), Input('close-mcc-carbon-clock-modal-button', 'n_clicks')],
    [State('mcc-carbon-clock-modal', 'is_open')]
)
def toggle_mcc_carbon_clock_modal(open_n_clicks, close_n_clicks, is_open):
    if open_n_clicks or close_n_clicks:
        return not is_open
    return is_open