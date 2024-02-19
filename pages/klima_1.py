# Import necessary libraries and modules
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from utils import dataManager as dm
from utils import layoutFunctions as lf

# ------------------------------------------------------------------------------
# Load the necessary data
# ------------------------------------------------------------------------------
# Load CO2 and continent datasets
df_co2 = dm.read_co2_data('data/originalData/klima_1/owid-co2-data.csv')
df_continents = dm.read_continental_data('data/originalData/klima_1/continents-according-to-our-world-in-data.csv')

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

continent_name_translation = {
    "Africa": "Afrika",
    "Asia": "Asien",
    "Europe": "Europa",
    "High-income countries": "Hochverdienende Länder",
    "International transport": "Internationaler Transport",
    "Low-income countries": "Niedrigverdienende Länder",
    "Lower-middle-income countries": "Länder mit niedrigem mittlerem Einkommen",
    "North America": "Nordamerika",
    "Oceania": "Ozeanien",
    "South America": "Südamerika",
    "Upper-middle-income countries": "Länder mit oberem mittlerem Einkommen",
    "World": "Welt"
}


# Filter rows based on the 'continent' column
df_filtered = df[df['continent'].isin(valid_continents)]

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

df_filtered = df_filtered.copy()
df_filtered['country'] = df_filtered['country'].map(country_name_translation).fillna(df_filtered['country'])
df_filtered['continent'] = df_filtered['continent'].map(continent_name_translation).fillna(df_filtered['continent'])


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
        dbc.Row([lf.make_footer()]),
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



