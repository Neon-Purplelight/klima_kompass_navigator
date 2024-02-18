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
    # # Example usage
input_json_path = 'data/originalData/klima_2/world-countries.json'
output_json_path = 'data/processedData/klima_2/processed_world-countries.json'
dm.process_and_save_json(input_json_path, output_json_path)

# Extract valid country names from the processed JSON
country_names = dm.extract_country_names(output_json_path)

# Process and save the CSV
input_file_path_csv = 'data/originalData/klima_2/owid-co2-data.csv'
output_file_path_csv = 'data/processedData/klima_2/processed_data.csv'
dm.process_and_save_csv(input_file_path_csv, output_file_path_csv, country_names)

df = pd.read_csv('data/processedData/klima_2/processed_data.csv')
with open('data/processedData/klima_2/processed_world-countries.json') as f:
    countries_json = json.load(f)

min_year = df['year'].min()
max_year = df['year'].max()

# ------------------------------------------------------------------------------
# Initialize utility objects and useful functions
# ------------------------------------------------------------------------------
# Erstellen Sie eine Liste aller einzigartigen Länder aus dem DataFrame
countries = df['country'].unique()

country_name_translation = {
    "Afghanistan": "Afghanistan",
    "Albania": "Albanien",
    "Algeria": "Algerien",
    "Andorra": "Andorra",
    "Angola": "Angola",
    "Antigua and Barbuda": "Antigua und Barbuda",
    "Argentina": "Argentinien",
    "Armenia": "Armenien",
    "Australia": "Australien",
    "Austria": "Österreich",
    "Azerbaijan": "Aserbaidschan",
    "Bahamas": "Bahamas",
    "Bahrain": "Bahrain",
    "Bangladesh": "Bangladesch",
    "Barbados": "Barbados",
    "Belarus": "Weißrussland",
    "Belgium": "Belgien",
    "Belize": "Belize",
    "Benin": "Benin",
    "Bhutan": "Bhutan",
    "Bolivia": "Bolivien",
    "Bosnia and Herzegovina": "Bosnien und Herzegowina",
    "Botswana": "Botswana",
    "Brazil": "Brasilien",
    "Brunei": "Brunei",
    "Bulgaria": "Bulgarien",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Cambodia": "Kambodscha",
    "Cameroon": "Kamerun",
    "Canada": "Kanada",
    "Cape Verde": "Kap Verde",
    "Central African Republic": "Zentralafrikanische Republik",
    "Chad": "Tschad",
    "Chile": "Chile",
    "China": "China",
    "Colombia": "Kolumbien",
    "Comoros": "Komoren",
    "Congo": "Kongo",
    "Costa Rica": "Costa Rica",
    "Croatia": "Kroatien",
    "Cuba": "Kuba",
    "Cyprus": "Zypern",
    "Czech Republic": "Tschechische Republik",
    "Denmark": "Dänemark",
    "Djibouti": "Dschibuti",
    "Dominica": "Dominica",
    "Dominican Republic": "Dominikanische Republik",
    "East Timor": "Osttimor",
    "Ecuador": "Ecuador",
    "Egypt": "Ägypten",
    "El Salvador": "El Salvador",
    "Equatorial Guinea": "Äquatorialguinea",
    "Eritrea": "Eritrea",
    "Estonia": "Estland",
    "Eswatini": "Eswatini",
    "Ethiopia": "Äthiopien",
    "Fiji": "Fidschi",
    "Finland": "Finnland",
    "France": "Frankreich",
    "Gabon": "Gabun",
    "Gambia": "Gambia",
    "Georgia": "Georgien",
    "Germany": "Deutschland",
    "Ghana": "Ghana",
    "Greece": "Griechenland",
    "Grenada": "Grenada",
    "Guatemala": "Guatemala",
    "Guinea": "Guinea",
    "Guinea-Bissau": "Guinea-Bissau",
    "Guyana": "Guyana",
    "Haiti": "Haiti",
    "Honduras": "Honduras",
    "Hungary": "Ungarn",
    "Iceland": "Island",
    "India": "Indien",
    "Indonesia": "Indonesien",
    "Iran": "Iran",
    "Iraq": "Irak",
    "Ireland": "Irland",
    "Israel": "Israel",
    "Italy": "Italien",
    "Ivory Coast": "Elfenbeinküste",
    "Jamaica": "Jamaika",
    "Japan": "Japan",
    "Jordan": "Jordanien",
    "Kazakhstan": "Kasachstan",
    "Kenya": "Kenia",
    "Kiribati": "Kiribati",
    "Kosovo": "Kosovo",
    "Kuwait": "Kuwait",
    "Kyrgyzstan": "Kirgisistan",
    "Laos": "Laos",
    "Latvia": "Lettland",
    "Lebanon": "Libanon",
    "Lesotho": "Lesotho",
    "Liberia": "Liberia",
    "Libya": "Libyen",
    "Liechtenstein": "Liechtenstein",
    "Lithuania": "Litauen",
    "Luxembourg": "Luxemburg",
    "Madagascar": "Madagaskar",
    "Malawi": "Malawi",
    "Malaysia": "Malaysia",
    "Maldives": "Malediven",
    "Mali": "Mali",
    "Malta": "Malta",
    "Marshall Islands": "Marshallinseln",
    "Mauritania": "Mauretanien",
    "Mauritius": "Mauritius",
    "Mexico": "Mexiko",
    "Micronesia": "Mikronesien",
    "Moldova": "Moldawien",
    "Monaco": "Monaco",
    "Mongolia": "Mongolei",
    "Montenegro": "Montenegro",
    "Morocco": "Marokko",
    "Mozambique": "Mosambik",
    "Myanmar": "Myanmar",
    "Namibia": "Namibia",
    "Nauru": "Nauru",
    "Nepal": "Nepal",
    "Netherlands": "Niederlande",
    "New Zealand": "Neuseeland",
    "Nicaragua": "Nicaragua",
    "Niger": "Niger",
    "Nigeria": "Nigeria",
    "North Macedonia": "Nordmazedonien",
    "Norway": "Norwegen",
    "Oman": "Oman",
    "Pakistan": "Pakistan",
    "Palau": "Palau",
    "Palestine": "Palästina",
    "Panama": "Panama",
    "Papua New Guinea": "Papua-Neuguinea",
    "Paraguay": "Paraguay",
    "Peru": "Peru",
    "Philippines": "Philippinen",
    "Poland": "Polen",
    "Portugal": "Portugal",
    "Qatar": "Katar",
    "Romania": "Rumänien",
    "Russia": "Russland",
    "Rwanda": "Ruanda",
    "Saint Kitts and Nevis": "St. Kitts und Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent and the Grenadines": "St. Vincent und die Grenadinen",
    "Samoa": "Samoa",
    "San Marino": "San Marino",
    "São Tomé and Príncipe": "São Tomé und Príncipe",
    "Saudi Arabia": "Saudi-Arabien",
    "Senegal": "Senegal",
    "Serbia": "Serbien",
    "Seychelles": "Seychellen",
    "Sierra Leone": "Sierra Leone",
    "Singapore": "Singapur",
    "Slovakia": "Slowakei",
    "Slovenia": "Slowenien",
    "Solomon Islands": "Salomonen",
    "Somalia": "Somalia",
    "South Africa": "Südafrika",
    "South Sudan": "Südsudan",
    "Spain": "Spanien",
    "Sri Lanka": "Sri Lanka",
    "Sudan": "Sudan",
    "Suriname": "Suriname",
    "Sweden": "Schweden",
    "Switzerland": "Schweiz",
    "Syria": "Syrien",
    "Taiwan": "Taiwan",
    "Tajikistan": "Tadschikistan",
    "Tanzania": "Tansania",
    "Thailand": "Thailand",
    "Togo": "Togo",
    "Tonga": "Tonga",
    "Trinidad and Tobago": "Trinidad und Tobago",
    "Tunisia": "Tunesien",
    "Turkey": "Türkei",
    "Turkmenistan": "Turkmenistan",
    "Tuvalu": "Tuvalu",
    "Uganda": "Uganda",
    "Ukraine": "Ukraine",
    "United Arab Emirates": "Vereinigte Arabische Emirate",
    "United Kingdom": "Vereinigtes Königreich",
    "United States": "Vereinigte Staaten",
    "Uruguay": "Uruguay",
    "Uzbekistan": "Usbekistan",
    "Vanuatu": "Vanuatu",
    "Vatican City": "Vatikanstadt",
    "Venezuela": "Venezuela",
    "Vietnam": "Vietnam",
    "Yemen": "Jemen",
    "Zambia": "Sambia",
    "Zimbabwe": "Simbabwe"
}

translated_country_options = [{'label': country_name_translation.get(country, country), 'value': country} for country in countries]

df['translated_country'] = df['country'].apply(lambda x: country_name_translation.get(x, x))

chart_type_buttons = dbc.ButtonGroup(
    [
        dbc.Button("Weltkarte", id='button-map', color="primary", className="me-1"),
        dbc.Button("Liniendiagramm", id='button-line', color="primary"),
    ],
    className="mb-3",
    style={'color': 'white'}  # Setzen Sie die Schriftfarbe auf Weiß für nicht ausgewählte Buttons
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
                dbc.Col(lf.make_klima_2_sidebar(), width=4),
                dbc.Col(
                    [
                        lf.make_co2_world_map(translated_country_options, min_year, max_year, chart_type_buttons),
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row([lf.make_footer()]),
    ],
)

# ------------------------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------------------------
@callback(
    [Output('chart-type-status', 'children'),
     Output('button-map', 'style'),
     Output('button-line', 'style')],
    [Input('button-map', 'n_clicks'),
     Input('button-line', 'n_clicks')],
    [State('chart-type-status', 'children')]
)
def update_chart_type_and_button_styles(button_map, button_line, current_status):
    ctx = dash.callback_context

    # Standardstyles für nicht ausgewählte Buttons
    default_style = {'color': 'white'}
    # Style für den ausgewählten Button
    selected_style = {'color': '#7fff00'}

    # Wenn der Callback zum ersten Mal ausgelöst wird, werden Standardwerte zurückgegeben
    if not ctx.triggered:
        # Angenommen, die Weltkarte ist die Standardansicht
        return 'map', selected_style, default_style

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'button-map':
        return 'map', selected_style, default_style
    else:
        return 'line', default_style, selected_style

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
            hover_name="translated_country",
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
            color='translated_country',
            title=f"CO2 Emissions by {selected_co2_type} Over Time"
        )

    return fig

@callback(
    Output('world-countries-modal', 'is_open'),
    [Input('open-world-countries-modal-button', 'n_clicks'), Input('close-world-countries-modal-button', 'n_clicks')],
    [State('world-countries-modal', 'is_open')]
)
def toggle_world_countries_modal(open_n_clicks, close_n_clicks, is_open):
    if open_n_clicks or close_n_clicks:
        return not is_open
    return is_open