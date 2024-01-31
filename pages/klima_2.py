import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
df = pd.read_csv('data\originalData\processed_data.csv')
with open('data\originalData\processed_world-countries.json') as f:
    countries_json = json.load(f)

min_year = df['year'].min()
max_year = df['year'].max()

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
# Erstellen Sie eine Liste aller einzigartigen Länder aus dem DataFrame
countries = df['country'].unique()

chart_type_buttons = dbc.ButtonGroup(
    [
        dbc.Button("Weltkarte", id='button-map', color="primary", className="me-1"),
        dbc.Button("Liniendiagramm", id='button-line', color="secondary"),
    ],
    className="mb-3",
)

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
                dbc.Col(lf.make_klima_2_sidebar(), width=4),
                
                # Main content area with settings and selected graph container
                dbc.Col(
                    [
                        lf.make_co2_world_map(countries, min_year, max_year, chart_type_buttons)
                    ],
                    width=8,
                ),
            ]
        ),
        
        # Row containing the Creative Commons license banner
        dbc.Row([lf.make_CC_licenseBanner()]),
    ],
)

# ------------------------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------------------------
@callback(
    Output('chart-type-status', 'children'),
    [Input('button-map', 'n_clicks'),
     Input('button-line', 'n_clicks')],
    [State('chart-type-status', 'children')]
)
def update_chart_type_status(button_map, button_line, current_status):
    ctx = dash.callback_context

    # Wenn der Callback zum ersten Mal ausgelöst wird, wird der Standardwert zurückgegeben
    if not ctx.triggered:
        return 'map'

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return 'map' if button_id == 'button-map' else 'line'

# Callback zum Aktualisieren des Diagramms
@callback(
    Output('chart', 'figure'),
    [Input('co2-type-selector', 'value'),
     Input('year-slider', 'value'),
     Input('country-selector', 'value'),
     Input('chart-type-status', 'children')]  # Direktes Lesen des Diagrammtyps aus dem Status
)
def update_chart(selected_co2_type, selected_year_range, selected_countries, chart_type):
    min_year, max_year = selected_year_range
    filtered_df = df[(df['year'] >= min_year) & (df['year'] <= max_year)]

    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

    if chart_type == 'map':
        fig = px.choropleth(
            filtered_df,
            locations="iso_code",
            geojson=countries_json,
            color=selected_co2_type,
            hover_name="country",
            title=f"World CO2 Emissions by {selected_co2_type} from {min_year} to {max_year}",
            color_continuous_scale="YlOrRd"  # Hier ändern Sie die Farbskala
        )
        fig.update_layout(
            margin={"r":0, "t":0, "l":0, "b":0},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="center",
                x=0.5
            )
        )
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            showcountries=True,
            showcoastlines=True,
            showland=True,
            landcolor="LightGrey",
            showocean=True,
            oceancolor="LightBlue"
        )
    elif chart_type == 'line':
        fig = px.line(
            filtered_df,
            x='year',
            y=selected_co2_type,
            color='country',
            title=f"CO2 Emissions by {selected_co2_type} Over Time"
        )

    return fig