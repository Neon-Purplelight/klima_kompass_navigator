import base64
from io import BytesIO
import matplotlib.pyplot as plt
import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import numpy as np
from utils import dataManager as dm
from utils import layoutFunctions as lf

# Setzen Sie den Matplotlib-Backend für den nicht-interaktiven Gebrauch
import matplotlib
matplotlib.use('Agg')

# ------------------------------------------------------------------------------
# Laden Sie die erforderlichen Daten
# ------------------------------------------------------------------------------
topsoil_file_path = 'data/processedData/pedo_1/filtered_SMI_Oberboden_monatlich.nc'
lats_oberboden, lons_oberboden, data_oberboden, date_values_oberboden = dm.preprocess_netcdf_data(topsoil_file_path)

total_soil_file_path = 'data/processedData/pedo_1/filtered_SMI_Gesamtboden_monatlich.nc'
lats_gesamtboden, lons_gesamtboden, data_gesamtboden, date_values_gesamtboden = dm.preprocess_netcdf_data(total_soil_file_path)

# ...

# LAYOUT
# ...
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
                                            html.P("Aus den Karten wird deutlich, dass die Bodenfeuchte in Deutschland im Winter in der Regel höher ist als im Sommer. Dies hängt mit der innerjährlichen Niederschlagsverteilung, der sehr niedrigen Verdunstung im Winter und den höheren Niederschlagsintensitäten im Sommer zusammen."),
                                            html.Hr(),
                                            html.P("Auf die Oberboden- Karten wird jeweils der Bodenfeuchteindex des Oberbodens (bis 25 cm Tiefe) dargestellt. Dieser reagiert schneller auf kurzfristige Niederschlagsereignisse. Der Gesamtboden (bis 2 m Tiefe) ‘regeneriert’ hingegen langsamer als der Oberboden, da dieser Aufgrund seiner größeren Wasserspeicherkapazität und die langsamere Durchlässigkeit in tiefere Bodenschichten weniger stark auf kurzfristige Regenereignisse reagiert. Somit hat das aktuelle Wetter größeren Einfluss auf die Oberböden, längerfristige klimatische Trends hingegen, lassen sich besser am Gesamtboden ablesen."),
                                            html.Hr(),                                           
                                            html.P("2018 hat erstmalig seit 1976 wieder eine großflächige Dürre in Deutschland sowohl im Oberboden als auch über die gesamte Bodentiefe gebracht. Sommer und Herbst 2018 waren trockener als in allen vorherigen Jahren seit 1951. Da auch die folgenden Jahre die heißesten seit Beginn der Aufzeichnungen sind, konnte sich der Boden nicht mehr wirklich vollständig erholen. Im Zuge des Klimawandels sind weitere Dürren in Zukunft wahrscheinlicher."),
                                        ],
                                        className="card-text",
                                    ),
                                ),
                                id="info-card_hydro_1_settings",
                            ),
                        ]),
                        # Tabs für Timescale und Vergleich
                        lf.make_drought_tabs(date_values_oberboden, date_values_gesamtboden),
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
# Callbacks
@callback(
    Output('plots-container-timescale', 'children'),
    [Input('time-slider-drought', 'value')]
)
def update_timescale_tab(time_idx):
    plots = []
    plt.clf()
    plt.cla()

    fig, axs = plt.subplots(1, 2, figsize=(22, 11))  

    # Oberboden
    data_slice_oberboden = data_oberboden[time_idx, :, :]
    img_oberboden = axs[0].imshow(data_slice_oberboden, 
                                   extent=(lons_oberboden.min(), lons_oberboden.max(), 
                                           lats_oberboden.min(), lats_oberboden.max()), 
                                   origin='lower', 
                                   cmap='YlOrRd_r')  # Umgekehrtes Farbschema
    axs[0].set_title(f'Oberboden - {dm.translate_month(date_values_oberboden[time_idx])}')
    axs[0].axis('off')  

    # Gesamtboden
    data_slice_gesamtboden = data_gesamtboden[time_idx, :, :]
    img_gesamtboden = axs[1].imshow(data_slice_gesamtboden, 
                                     extent=(lons_gesamtboden.min(), lons_gesamtboden.max(), 
                                             lats_gesamtboden.min(), lats_gesamtboden.max()), 
                                     origin='lower', 
                                     cmap='YlOrRd_r')  # Umgekehrtes Farbschema
    axs[1].set_title(f'Gesamtboden - {dm.translate_month(date_values_gesamtboden[time_idx])}')
    axs[1].axis('off') 

    # Colorbar für Oberboden
    cax = fig.add_axes([0.5, 0.1, 0.02, 0.8])
    fig.colorbar(img_oberboden, cax=cax, label='SMI-Werte')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    plots.append(html.Img(src=f'data:image/png;base64,{img_base64}', className="img-fluid"))  

    plt.close()  # Close the Matplotlib figure

    return plots

@callback(
    Output('plots-container-gesamtboden', 'children'),
    [Input('data-dropdown-gesamtboden', 'value'),
     Input('time-dropdown-gesamtboden', 'value')]
)
def update_comparison_tab(selected_datasets, selected_times):
    if selected_times is None or not selected_times:
        raise PreventUpdate

    plots_container = []

    for selected_time in selected_times:
        selected_time = selected_time.split('T')[0]

        if selected_time not in [date.strftime("%Y-%m-%d") for date in date_values_gesamtboden]:
            print(f"DEBUG: Selected time {selected_time} not in date_values_gesamtboden.")
            continue

        time_idx = [date.strftime("%Y-%m-%d") for date in date_values_gesamtboden].index(selected_time)
        plots = []

        for selected_dataset in selected_datasets or []:
            plt.clf()
            plt.cla()

            if selected_dataset == 'gesamtboden':
                if time_idx >= len(data_gesamtboden):
                    print(f"DEBUG: time_idx {time_idx} is out of bounds for data_gesamtboden.")
                    continue

                data_slice = data_gesamtboden[time_idx, :, :]
                lats, lons = lats_gesamtboden, lons_gesamtboden
                title_prefix = 'Gesamtboden'
            elif selected_dataset == 'oberboden':
                if time_idx >= len(data_oberboden):
                    print(f"DEBUG: time_idx {time_idx} is out of bounds for data_oberboden.")
                    continue

                data_slice = data_oberboden[time_idx, :, :]
                lats, lons = lats_oberboden, lons_oberboden
                title_prefix = 'Oberboden'
            else:
                continue

            # Formatierung des Titels für die Karten
            selected_date = date_values_gesamtboden[time_idx]
            month_name = selected_date.strftime("%B").replace("January", "Januar").replace("February", "Februar").replace("March", "März").replace("April", "April").replace("May", "Mai").replace("June", "Juni").replace("July", "Juli").replace("August", "August").replace("September", "September").replace("October", "Oktober").replace("November", "November").replace("December", "Dezember")
            
            fig, ax = plt.subplots(figsize=(7, 4))
            img = ax.imshow(data_slice, extent=(lons.min(), lons.max(), lats.min(), lats.max()), origin='lower', cmap='YlOrRd_r')
            plt.colorbar(img, ax=ax, label='SMI-Werte')
            plt.axis('off')
            plt.title(f'{title_prefix} - {month_name} {selected_date.year}')
            ax.set_adjustable('datalim')

            img_buf = BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
            img_buf.seek(0)
            img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

            plots.append(html.Div(html.Img(src=f'data:image/png;base64,{img_base64}', className="img-fluid")))

            plt.close()  # Close the Matplotlib figure

        plots_container.extend(plots)

    return [html.Div(plots_container, style={'display': 'flex', 'flexWrap': 'wrap'})]
