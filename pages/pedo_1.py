# Importieren Sie die erforderlichen Bibliotheken und Module
import base64
from datetime import datetime, timedelta
from io import BytesIO

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from utils import dataManager as dm
from utils import layoutFunctions as lf
from dash.exceptions import PreventUpdate

# Setzen Sie den Matplotlib-Backend für den nicht-interaktiven Gebrauch
import matplotlib
matplotlib.use('Agg')

# ------------------------------------------------------------------------------
# Laden Sie die erforderlichen Daten
# ------------------------------------------------------------------------------
topsoil_file_path = 'data\originalData\SMI_Oberboden_monatlich.nc'
lats_oberboden, lons_oberboden, data_oberboden, date_values_oberboden = dm.preprocess_netcdf_data(topsoil_file_path)

# Laden Sie Daten für Gesamtboden
# total_soil_file_path = 'data\originalData\SMI_Gesamtboden_monatlich.nc'
# lats_gesamtboden, lons_gesamtboden, data_gesamtboden, date_values_gesamtboden = dm.preprocess_netcdf_data(total_soil_file_path)

# ...
# LAYOUT
# ...
# Definieren Sie die Layout-Struktur mit Navigationsleiste, Seitenleiste, Einstellungen und ausgewähltem Graph-Container
layout = html.Div(
    [
        # Navigationsleiste
        dbc.Row(lf.make_NavBar()),

        # Hauptinhalt
        dbc.Row(
            [
                # Seitenleiste
                dbc.Col(lf.make_pedo_1_sidebar(), width=4),

                # Hauptinhalt-Bereich
                dbc.Col(
                    [
                        # Einstellungen und Informationen
                        lf.make_pedo_1_settings(),
                        html.Div([
                            dbc.Button("ℹ️ Info", id="info-button_hydro_1_settings", color="primary", className="mr-1"),
                            dbc.Collapse(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.P("Lorem"),
                                            html.P("Ipsum"),
                                        ],
                                        className="card-text",
                                    ),
                                ),
                                id="info-card_hydro_1_settings",
                            ),
                        ]),
                        # # Tabs for Timescale and Vergleich
                        # dcc.Tabs([
                        #     dcc.Tab(label='Timescale', children=[
                        #         dcc.Slider(
                        #             id='time-slider-oberboden',
                        #             min=0,
                        #             max=len(date_values_oberboden) - 1,
                        #             step=1,
                        #             marks={i: date_values_oberboden[i].strftime("%d.%m.%Y") for i in range(0, len(date_values_oberboden), len(date_values_oberboden)//10)},
                        #             value=0,
                        #             tooltip={'placement': 'bottom', 'always_visible': True},
                        #         ),
                        #         html.Div([
                        #             html.Div(id='plots-container-timescale'),
                        #         ], style={'display': 'flex'}),
                        #     ]),

                        #     dcc.Tab(label='Vergleich', children=[
                        #         dcc.Dropdown(
                        #             id='time-dropdown-gesamtboden',
                        #             options=[
                        #                 {'label': date.strftime("%d.%m.%Y"), 'value': date} for date in date_values_gesamtboden
                        #             ],
                        #             multi=True,
                        #             value=None,
                        #             placeholder='Select time',
                        #         ),
                        #         dcc.Dropdown(
                        #             id='data-dropdown-gesamtboden',
                        #             options=[
                        #                 {'label': 'Gesamtboden', 'value': 'gesamtboden'},
                        #                 {'label': 'Oberboden', 'value': 'oberboden'},
                        #             ],
                        #             value=None,
                        #             multi=True,
                        #             placeholder='Select data',
                        #         ),
                        #         html.Div([
                        #             html.Div(id='plots-container-gesamtboden'),
                        #         ], style={'display': 'flex'}),
                        #     ]),
                        # ]),
                    ]
                ),
            ]
        ),
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)

# ...
# Callbacks
# ...
# @callback(
#     Output('plots-container-timescale', 'children'),
#     [Input('time-slider-oberboden', 'value')]
# )
# def update_maps_timescale(time_idx):
#     plots = []
#     plt.clf()
#     plt.cla()

#     fig, axs = plt.subplots(1, 2, figsize=(22, 11))  

#     # Oberboden
#     data_slice_oberboden = data_oberboden[time_idx, :, :]
#     img_oberboden = axs[0].imshow(data_slice_oberboden, extent=(lons_oberboden.min(), lons_oberboden.max(), lats_oberboden.min(), lats_oberboden.max()), origin='lower', cmap='YlOrRd')
#     axs[0].set_title(f'Oberboden - {date_values_oberboden[time_idx].strftime("%d.%m.%Y")}')
#     axs[0].axis('off')  

#     # Gesamtboden
#     data_slice_gesamtboden = data_gesamtboden[time_idx, :, :]
#     img_gesamtboden = axs[1].imshow(data_slice_gesamtboden, extent=(lons_gesamtboden.min(), lons_gesamtboden.max(), lats_gesamtboden.min(), lats_gesamtboden.max()), origin='lower', cmap='YlOrRd')
#     axs[1].set_title(f'Gesamtboden - {date_values_gesamtboden[time_idx].strftime("%d.%m.%Y")}')
#     axs[1].axis('off') 

#     # Colorbar
#     cax = fig.add_axes([0.5, 0.1, 0.02, 0.8])
#     fig.colorbar(img_oberboden, cax=cax, label='SMI-Werte')

#     img_buf = BytesIO()
#     plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
#     img_buf.seek(0)
#     img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

#     plots.append(html.Img(src=f'data:image/png;base64,{img_base64}', className="img-fluid"))  

#     return plots

# @callback(
#     Output('plots-container-gesamtboden', 'children'),
#     [Input('data-dropdown-gesamtboden', 'value'),
#      Input('time-dropdown-gesamtboden', 'value')]
# )
# def update_maps_gesamtboden(selected_datasets, selected_times):
#     if selected_times is None or not selected_times:
#         raise PreventUpdate

#     plots_container = []

#     for selected_time in selected_times:
#         selected_time = selected_time.split('T')[0]

#         if selected_time not in [date.strftime("%Y-%m-%d") for date in date_values_gesamtboden]:
#             print(f"DEBUG: Selected time {selected_time} not in date_values_gesamtboden.")
#             continue

#         time_idx = [date.strftime("%Y-%m-%d") for date in date_values_gesamtboden].index(selected_time)
#         plots = []

#         for selected_dataset in selected_datasets or []:
#             plt.clf()
#             plt.cla()

#             if selected_dataset == 'gesamtboden':
#                 if time_idx >= len(data_gesamtboden):
#                     print(f"DEBUG: time_idx {time_idx} is out of bounds for data_gesamtboden.")
#                     continue

#                 data_slice = data_gesamtboden[time_idx, :, :]
#                 lats, lons = lats_gesamtboden, lons_gesamtboden
#                 title_prefix = 'Gesamtboden'
#             elif selected_dataset == 'oberboden':
#                 if time_idx >= len(data_oberboden):
#                     print(f"DEBUG: time_idx {time_idx} is out of bounds for data_oberboden.")
#                     continue

#                 data_slice = data_oberboden[time_idx, :, :]
#                 lats, lons = lats_oberboden, lons_oberboden
#                 title_prefix = 'Oberboden'
#             else:
#                 continue

#             fig, ax = plt.subplots(figsize=(7, 4))
#             img = ax.imshow(data_slice, extent=(lons.min(), lons.max(), lats.min(), lats.max()), origin='lower', cmap='YlOrRd')
#             plt.colorbar(img, ax=ax, label='SMI-Werte')
#             plt.axis('off')
#             plt.title(f'{title_prefix} - {selected_time}')
#             ax.set_adjustable('datalim')

#             img_buf = BytesIO()
#             plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
#             img_buf.seek(0)
#             img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

#             plots.append(html.Div(html.Img(src=f'data:image/png;base64,{img_base64}', className="img-fluid")))

#             plt.close()  

#         plots_container.extend(plots)

#     return [html.Div(plots_container, style={'display': 'flex', 'flexWrap': 'wrap'})]

