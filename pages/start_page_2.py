from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from utils import dataManager as dm
from utils import layoutFunctions as lf

# Load necessary data
df_temp = dm.read_temp_data('data/originalData/start_page_2/GLB.Ts+dSST.csv')
df_co2 = dm.read_co2_data('data/originalData/start_page_2/owid-co2-data.csv')

# Perform preprocessing
df_co2 = dm.preprocess_co2_data(df_co2)

# Layout
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),
        dbc.Row(
            [
                dbc.Col(lf.make_start_page_2_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_start_page_2_settings(),
                        html.Div(id='selected-graph-container', style={'height': '100vh'})
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_footer()]),
    ],
)

# Callbacks
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

def toggle_info_card(info_button_id, info_card_id):
    @callback(
        Output(info_card_id, "style"),
        Input(info_button_id, "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_info_card_style(n_clicks):
        if n_clicks is None:
            return {"display": "none"}
        elif n_clicks % 2 == 0:
            return {"display": "none"}
        else:
            return {}

toggle_info_card("info-button_klima_1_co2", "info-card_klima_1_co2")
toggle_info_card("info-button_klima_1_temp", "info-card_klima_1_temp")
toggle_info_card("info-button_klima_1_cor", "info-card_klima_1_cor")
toggle_info_card("info-button_klima_1_barplot", "info-card_klima_1_barplot")

@callback(
    Output('collapse_more_info_klima_1', 'is_open'),
    Input('more_info_button_klima_1', 'n_clicks'),
    State('collapse_more_info_klima_1', 'is_open'),
    prevent_initial_call=True
)
def toggle_collapse_more_info(n_clicks, is_open):
    return not is_open

def toggle_modal(modal_id, modal_open_button_id, modal_close_button_id):
    @callback(
        Output(modal_id, "is_open"),
        [Input(modal_open_button_id, "n_clicks"), Input(modal_close_button_id, "n_clicks")],
        [State(modal_id, "is_open")],
        prevent_initial_call=True
    )
    def toggle_modal_state(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

toggle_modal("modal", "open-modal-button", "close-modal-button")

toggle_modal("gistemp-modal", "open-gistemp-modal-button", "close-gistemp-modal-button")

