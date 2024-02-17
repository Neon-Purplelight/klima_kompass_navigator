from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
from utils import dataManager as dm
import numpy as np
import os
import base64

# ------------------------------------------------------------------------------
# make_ FUNCTIONS
# These functions are called only once to create the backbone of the graphical
# plots and elements. Then each element is updated based on callbacks that call
# "update_" functions.
# ------------------------------------------------------------------------------
def make_NavBar():
    """
    Makes the navigation bar
    """
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink('Startseite', href='/', id='navlink')),
            dbc.NavItem(dbc.NavLink('Klimatologie', href='/klima_1', id='navlink')),
            dbc.NavItem(dbc.NavLink('Hydrologie', href='/hydro_1', id='navlink')),
            dbc.NavItem(dbc.NavLink('Pedologie', href='/pedo_1', id='navlink')),
            #dbc.NavItem(dbc.NavLink('Ökologie', href='/oeko_1', id='navlink')),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem('Link zum Quellcode', href='https://github.com/Neon-Purplelight/klima_kompass_navigator'),
                    dbc.DropdownMenuItem('Link zum Studiengang', href='https://www.bht-berlin.de/m-ugis'),
                ],
                nav=True,
                in_navbar=True,
                label='Mehr',
            ),
        ],
        brand='Klima Kompass Navigator',
        brand_href='/',
        color='primary',
        fixed='top',
        dark=True,
        style={'height': '80px', 'font-size': '32px'},
        className='navbar-custom',
        brand_style={'position': 'absolute', 'left': '20px', 'top': '0px'}
    )
    return navbar

def make_footer():
    banner = []

    banner = html.Div([
        html.Hr(className="mt-2 mb-2"),
        html.P([
            "Link zum ",
            dcc.Link("Quellcode",
                     href="https://github.com/Neon-Purplelight/klima_kompass_navigator",
                     target="_blank"),
        ]),
        html.A([
            html.Img([], alt="Creative Commons Lizenz",
                     src="https://i.creativecommons.org/l/by/4.0/88x31.png")],
            rel="license", href="http://creativecommons.org/licenses/by/4.0/", className="border-width:0 me-2"),
        "Dieses Werk ist lizenziert unter ",
        html.A(["Creative Commons Attribution 4.0 International License"],
               rel='license', href="http://creativecommons.org/licenses/by/4.0/")
    ], className='pt-5')

    return banner

# ------------------------------------------------------------------------------
# start_page_1 functions
# ------------------------------------------------------------------------------
def make_start_page_1_sidebar():
    # Bootstrap Sidebar
    # Verwenden Sie Font Awesome-Symbole für Links
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " CO2- Budget"],
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " CO2 und das Klima"],
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/start_page_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
    brand=html.Span([link_icon, " Startseite:"],
        style={"color": "#7fff00"}),
        color="primary",
        dark=True,
        className="d-flex justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                html.P(["Diese Seite bindet die Carbon Uhr des Mercator Research Institute on Global Commons and Climate Change (",
                html.A("MCC", href="https://de.wikipedia.org/wiki/Mercator_Research_Institute_on_Global_Commons_and_Climate_Change", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                ") ein. Diese wurde anhand der neuesten Daten des Intergovernmental Panel on Climate Change (",
                html.A("IPCC", href="https://de.wikipedia.org/wiki/Mercator_Research_Institute_on_Global_Commons_and_Climate_Change", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                ") überarbeitet, um das verbleibende globale Budget für Treibhausgasemissionen anzuzeigen. Dies verdeutlicht den Druck für politische Maßnahmen zur Begrenzung der globalen Erwärmung auf 1,5 und 2 Grad Celsius über dem vorindustriellen Niveau. Die aktualisierte Uhr veranschaulicht, dass das Zeitfenster für entscheidende Maßnahmen zur Begrenzung der Auswirkungen des Klimawandels immer knapper wird."]),
               ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4(" Weitere Informationen", id='more_info_button_klima_2', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                            "Der IPCC kondensiert die Forschungsergebnisse aus rund 14.000 Fachveröffentlichungen zum physikalischen Grundlagen des Klimawandels und identifiziert schwerwiegendere Veränderungen als bisher angenommen. Die CO2-Restbudgets für die 1,5- und 2-Grad-Ziele wurden zuletzt leicht erhöht und liegen nun bei 400 und 1150 Gigatonnen CO2. Die Anhebung des Budgets folgt methodischen Weiterentwicklungen in der Klimaforschung. Die Budgets sind so berechnet, dass sie mit hoher Wahrscheinlichkeit die Temperaturziele erreichen (",
                            html.A("basierend auf zwei Dritteln der untersuchten Szenarien", href="https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM_final.pdf#page=33", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            "). Die Generalsekretärin des MCC Brigitte Knopf betont den enormen Handlungsdruck angesichts der zunehmenden Extremwetterereignisse und des besorgniserregenden Trends im IPCC-Bericht und fordert dringend wirksame Maßnahmen in der globalen Klimapolitik.",
                        ]),
                        html.Hr(),
                        html.H4("Verwendete Datensätze:"),
                        html.P([  
                            "Weitere Informationen zur Carbon Uhr finden sich auf der ",
                            html.A("Website", href="https://www.mcc-berlin.net/en/research/co2-budget.html", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " des Mercator Instituts.",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_klima_2',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_klima_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_iframe():
    # Info Button und Info Card
    info_button_1 = dbc.Button("ℹ️ Info", id="info-button_start_page_iframe", color="primary", className="mr-1")

    info_card_1 = dbc.Card(
        dbc.CardBody(
            [
                html.P("Enthält weitere Informationen zu den jeweiligen Infografiken."),
                html.Hr(),
                html.P([
                        "Die ",
                        html.A("MCC Carbon Clock", href="https://www.mcc-berlin.net/en/research/co2-budget.html"),
                        " zeigt, wie viel CO2 in die Atmosphäre freigesetzt werden kann, um die globale Erwärmung auf maximal 1,5 °C bzw. 2 °C (Im Vergleich zum vorindustriellen Zeitalter) zu begrenzen. Mit nur einem Klick können Sie die Schätzungen für beide Temperaturziele vergleichen und sehen, wie viel Zeit in jedem Szenario noch bleibt."
                        ]),
                html.P([
                        html.A("Das 1,5 °C Ziel", href="https://de.wikipedia.org/wiki/Sonderbericht_1,5_%C2%B0C_globale_Erw%C3%A4rmung"),
                        ", welches im ",
                        html.A("Pariser Klimaabkommen ", href="https://de.wikipedia.org/wiki/%C3%9Cbereinkommen_von_Paris"),
                        " gesetzt wurde, soll verhindern, dass es zu irreversiblen Entwicklungen innerhalb des Klimasystems kommt. Die Wissenschaftler des Weltklimarats (",
                        html.A("IPCC", href="https://de.wikipedia.org/wiki/Intergovernmental_Panel_on_Climate_Change"),
                        ") gehen davon aus, dass solche Kipppunkte jenseits einer Temperaturerhöhung von 1,5 °C nicht mehr ausreichend sicher ausgeschlossen werden können. Der ",
                        html.A("Emissions Gap Report 2021", href="https://www.umweltbundesamt.de/themen/emissions-gap-report-2021-klimazusagen-reichen"),
                        " des Umweltprogramms der Vereinten Nationen (",
                        html.A("UNEP", href="https://de.wikipedia.org/wiki/Umweltprogramm_der_Vereinten_Nationen"),
                        ") warnt, dass die aktuell zugesagten Klimaschutzmaßnahmen zu einem globalen Temperaturanstieg von etwa 2,7 °C bis zum Ende des Jahrhunderts führen würden."
                        ])
            ],
            className="card-text",
        ),
        id="info-card_start_page_iframe",
        style={"display": "none"},
    )

    # Combine info button, info card and the iframe
    iframe_row = html.Div([
        info_button_1,
        info_card_1,
        dbc.Col(html.Iframe(src="https://www.mcc-berlin.net/fileadmin/data/clock/carbon_clock.htm?i=3267263", width="120%", height="800px", style={'margin': '0'}), width=10, align="start"),  # Set width=12 and adjust align
    ])

    return iframe_row

def make_interactive_controls_example():
    # Create exemplary control elements
    controls_example = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Beispielhafte Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Dropdown-Menü:", html_for='dropdown-example', style={'color': 'white'}),
                                            dcc.Dropdown(
                                                id='dropdown-example',
                                                options=[
                                                    {'label': 'Option 1', 'value': 'option1'},
                                                    {'label': 'Option 2', 'value': 'option2'},
                                                    {'label': 'Option 3', 'value': 'option3'},
                                                ],
                                                value='option1',
                                                clearable=False,
                                            ),
                                            html.Div(id='dropdown-output', children=[]),
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Range Slider:", html_for='range-slider-example', style={'color': 'white'}),
                                            dcc.RangeSlider(
                                                id='range-slider-example',
                                                min=0,
                                                max=10,
                                                step=0.5,
                                                value=[3, 7],
                                                marks={i: str(i) for i in range(11)},
                                            ),
                                            html.Div(id='range-slider-output', children=[]),
                                        ],
                                        width=6,
                                    ),
                                ],
                            ),

                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Date Picker Range:", html_for='date-picker-range-example', style={'color': 'white'}),
                                            dcc.DatePickerRange(
                                                id='date-picker-range-example',
                                                start_date='2022-01-01',
                                                end_date='2022-12-31',
                                            ),
                                            html.Div(id='date-picker-range-output', children=[]),
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Input Box:", html_for='input-box-example', style={'color': 'white'}),
                                            dcc.Input(id='input-box-example', value='Default Text', type='text'),
                                            html.Div(id='input-box-output', children=[]),
                                        ],
                                        width=6,
                                    ),
                                ],
                            ),
                        ]
                    ),
                ],
                color="primary",
            ),
        ]
    )

    return controls_example

def make_data_info_start_page_1():
    return html.Div(
        children=[
            html.Hr(className="mt-2 mb-2"),
            html.H5("Lizenzinformationen"),
            html.P(
                """
                Die hier verwendeten Daten zu CO₂- und Treibhausgasemissionen stammen von Our World in Data und basieren auf dem Global Carbon Project. 
                Visualisierungen und Texte sind unter der Creative Commons Lizenz (CC BY) lizenziert, die es Ihnen ermöglicht, die Materialien für jeglichen Zweck frei zu nutzen. 
                Der Code und die Daten sind unter der MIT-Lizenz verfügbar. Für eine detaillierte Nutzung und um die genauen Lizenzbedingungen einzusehen, besuchen Sie bitte direkt das GitHub- Repository sowie die offizielle Website: 
                """
            ),
            html.A("GitHub-Repository", href="https://github.com/owid/co2-data", target="_blank", style={"color": "white", "text-decoration": "underline"}),
            html.Br(),
            html.A("Our World in Data", href="https://ourworldindata.org", target="_blank", style={"color": "white", "text-decoration": "underline"}),
        ],
        className="py-1 bg-primary rounded-1 text-white",
    )
# ------------------------------------------------------------------------------
# start_page_2 functions
# ------------------------------------------------------------------------------
def make_start_page_2_sidebar():
    # Bootstrap Sidebar
    # Verwenden Sie Font Awesome-Symbole für Links
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " CO2- Budget"],
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " CO2 und das Klima"],
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/start_page_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
    brand=html.Span([link_icon, " Startseite:"],
        style={"color": "#7fff00"}),
        color="primary",
        dark=True,
        className="d-flex justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                html.P([
                    "Die Diskussionen über den Klimawandel sind von Emotionen, politischen und wirtschaftlichen Motivationen sowie persönlichen Vorurteilen geprägt. Um einen Beitrag zur Diskussion liefern zu können ist es daher wichtig, die Datengrundlage sowie die Methodik zur Erstellung von Infografiken so transparent und klar wie möglich darzulegen."
                ]),
                html.P([
                    "Einige Skeptiker argumentieren, dass der menschliche Einfluss auf das Klima gering sei und natürliche Faktoren die Hauptursache für Klimaschwankungen darstellen. Sie betonen, dass vertieftes Verständnis natürlicher Prozesse die behauptete Dominanz des menschlichen Einflusses in Frage stellt. Für Häufig vorgebrachte Positionen von Klimaskeptikern siehe auch ",
                    html.A("Sceptical Science", href="https://skepticalscience.com/argument.php", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    "."
                ]),
                html.P([
                    "Demgegenüber weist die wachsende Erkenntnis darauf hin, dass der menschliche Einfluss auf das Klima dominanter ist als zuvor angenommen. Als Belege für den verstärkenden Treibhauseffekt von CO2 dienen verschiedene Messungen, darunter Satellitenmessungen der letzten 40 Jahre. Diese zeigen eine geringere Energieabstrahlung ins Weltall in CO2-bezogenen Wellenlängen und eine zunehmende nach unten gerichtete Infrarotstrahlung an der Erdoberfläche. Diese Daten bestätigen einen direkten, empirischen Zusammenhang zwischen CO2 und der globalen Erwärmung. Ohne wirksame Klimaschutzmaßnahmen droht ein erheblicher Temperaturanstieg im 21. Jahrhundert mit potenziell schwerwiegenden Folgen für Ökosysteme und Gesellschaften. Einen guten Überblick gibt der ",
                    html.A("sechste Sachstandsbericht", href="https://www.ipcc.ch/report/ar6/wg1/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " des IPPC."
                ]),
                html.P([
                    "Kürzlich hat die ",
                    html.A("NASA", href="https://www.nasa.gov/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " Neuigkeiten und Erkenntnisse ",
                    html.A("veröffentlicht", href="https://www.nasa.gov/news-release/nasa-analysis-confirms-2023-as-warmest-year-on-record/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    ", wie zum Beispiel die jährlichen globalen Temperaturanomalie für das Jahr 2023, welche hervorhebt, wie außergewöhnlich die Temperaturen im Vergleich zu historischen Daten waren. Dieses Dashboard soll veranschaulichen, wie sich solche Daten anhand verschiedener Diagramme veranschaulichen lassen."
                ]),
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4(" Weitere Informationen", id='more_info_button_klima_2', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                    html.Br(),
                    html.P([
                        "Die GISS Oberflächentemperaturanalyse Version 4 (",
                        html.A("GISTEMP v4", href="https://data.giss.nasa.gov/gistemp/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ") ist eine wichtige wissenschaftliche Arbeit, die von der NASA durchgeführt wird, um Veränderungen der globalen Oberflächentemperatur zu schätzen. Diese Analyse nutzt aktuelle Daten von meteorologischen Stationen und Ozeanbereichen, um monatlich aktualisierte Grafiken und Tabellen zu erstellen. Ziel ist es, ein klares Bild darüber zu vermitteln, wie sich die Temperaturen auf der Erde über die Zeit verändern.",
                    ]),
                    html.P([
                        "Für Interessierte und Forscher sind neben den Temperaturanomalien auch die verwendeten ",
                        html.A("Programme und der Quellcode", href="https://www.giss.nasa.gov/tools/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " verfügbar, was die Transparenz und Nachvollziehbarkeit der Analyse erhöht. Zudem werden regelmäßige Updates und detaillierte Informationen zu Veränderungen in der Analysemethodik veröffentlicht, um die Aktualität und Genauigkeit der Daten zu gewährleisten."
                    ]),
                                                                  
                    html.Hr(),
                    html.H4("Verwendete Datensätze:"),
                    make_owid_info_modal(),
                    make_gistemp_info_modal(),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}
                ),
                id='collapse_more_info_klima_2',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_klima_2', className='ms-1'),
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_start_page_2_settings(default_value='average_temp', options=None):
    # start_page_1 settings
    if options is None:
        options = [
            {'label': 'Durchschnittstemperatur', 'value': 'average_temp'},
            {'label': 'CO2 Emissionen', 'value': 'co2_emissions'},
            {'label': 'Korrelation', 'value': 'correlations'},
            {'label': 'Aufbereitete Präsentation', 'value': 'final_presentation'}
        ]

    # Card- Group
    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                    dbc.CardBody(
                        [
                            dbc.Label("Wähle Ansicht:", html_for=f'{id}-plot-selector', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='klima-1-plot-selector',
                                options=[{'label': option['label'], 'value': option['value']} for option in options],
                                value=default_value,
                                clearable=False,
                            ),
                            html.Div(id='klima-1-plot-container', children=[]),
                        ]
                    ),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def plot_average_temp(df_temp):
    template = 'plotly_dark'
    graph_id = 'temperature-graph'

    # Create a line plot using Plotly Express
    fig = px.line(df_temp, x='Year', y='JJA', template=template)

    # Modify axis labels
    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Temperatur (°C)'
    )

    # Convert Plotly figure to Dash Graph component with the specified ID
    # Create "ℹ️ Info" button
    info_button_2 = dbc.Button("ℹ️ Info", id="info-button_klima_1_temp", color="primary", className="mr-1")

    # Create the info_card
    info_card_2 = dbc.Card(
        dbc.CardBody(
            [
                html.P([
                    "Die Temperatur Daten wurden von Wissenschaftlern ",
                    html.A("Goddard Institute of Space Studies (GISS)", href="https://www.giss.nasa.gov/"),
                    " der NASA in New York aufgezeichnet und erfassen die Temperaturanomalien für die Monate Juni, Juli und August. Diese Monate gelten als der meteorologische Sommer auf der Nordhalbkugel. Die Daten erstrecken sich von 1880 bis zum aktuellen Jahr und erfassen die Veränderung der Sommertemperaturen im Vergleich zu einem Durchschnitt, der aus den Jahren 1951 bis 1980 berechnet wurde. Gemäß ihrer ",
                    html.A("Pressemitteilung", href="https://www.nasa.gov/press-release/nasa-announces-summer-2023-hottest-on-record"),
                    " waren die Monate Juni, Juli und August des Jahres 2023 zusammen 0,23 Grad Celsius wärmer als jeder andere Sommer zuvor und 1,2 Grad Celsius wärmer als der Durchschnittssommer zwischen 1951 und 1980."
                ]),
                html.Hr(),
                html.P("Ein einfaches Liniendiagramm der Daten zeigt deutlich den allmählichen Anstieg der Temperaturen (hier Nordhalbkugel) an. Die Temperaturen nach 1980 steigen allmählich an, diejenigen vor 1951 liegen größtenteils unter dem Durchschnitt, und diejenigen dazwischen tendieren dazu, um die Durchschnittstemperatur zu schwanken."),
            ],
            className="card-text",
        ),
        id="info-card_klima_1_temp",
        style={"display": "none"},
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_2,
        info_card_2,
        dcc.Graph(
            id=graph_id,
            figure=fig,
            config={'displayModeBar': False},
        )
    ])

    return graph_with_info_button

def plot_co2_data(df_co2):
    # Set default values for parameters
    y_column = "Annual CO₂ emissions"
    template = 'plotly_dark'
    graph_id = 'co2-graph'

    # Create a line plot using Plotly Express
    fig = px.line(df_co2, x='Year', y=y_column, template=template)

    # Update the layout to set the y-axis label
    fig.update_layout(
        yaxis_title="CO₂-Emissionen in Mio. t",
        xaxis_title="Jahr"
    )

    # Convert Plotly figure to Dash Graph component with the specified ID
    # Create "ℹ️ Info" button
    info_button_1 = dbc.Button("ℹ️ Info", id="info-button_klima_1_co2", color="primary", className="mr-1")

    # Create the info_card
    info_card_1 = dbc.Card(
        dbc.CardBody(
            [
                html.P([
                    "Es ist nicht einfach, die genaue Ursache für den unaufhaltsamen Anstieg der globalen Temperaturen durch ein einfaches Diagramm zu visualisieren. ",
                    "Jedoch können wir eine Verbindung zwischen dem Anstieg der CO₂-Emissionen und der Temperaturzunahme aufzeigen. Es ist bekannt, ",
                    "dass die CO₂-Emissionen aufgrund menschlicher Aktivitäten gestiegen sind, und es besteht eine klare Erkenntnis darüber, ",
                    "dass eine erhöhte Konzentration von CO₂ in der Atmosphäre zu einer Erwärmung führen kann."
                ]),
                html.Hr(),
                html.P([
                    "Tragen wir für denselben Zeitraum die atmosphärische CO₂ Konzentration in ein Diagramm ein, ähnelt dieses dem Diagramm zur Temperaturänderung. ",
                    "Es hat einen ähnlich flachen Anfang und einen steileren Anstieg in der zweiten Hälfte des Diagramms."
                ]),
            ],
            className="card-text",
        ),
        id="info-card_klima_1_co2",
        style={"display": "none"},  
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_1,
        info_card_1,
        dcc.Graph(
            id=graph_id,
            figure=fig,
            config={'displayModeBar': False},
        )
    ])

    return graph_with_info_button

def plot_scatter_with_ols(df_co2, df_temp):
    graph_id = 'scatter-plot-ols'

    common_years = set(df_co2['Year']).intersection(set(df_temp['Year']))

    # Filter DataFrames to include only common years
    df_co2_filtered = df_co2[df_co2['Year'].isin(common_years)]
    df_temp_filtered = df_temp[df_temp['Year'].isin(common_years)]

    # Now, use the filtered data for plotting
    fig = px.scatter(x=df_temp_filtered['JJA'], y=df_co2_filtered['Annual CO₂ emissions'], trendline='ols',
                     template='plotly_dark',
                     labels={"x": 'Temperaturänderung', "y": 'CO₂ Emissionen'})

    # Convert Plotly figure to Dash Graph component with the specified ID
    # Create "ℹ️ Info" button
    info_button_3 = dbc.Button("ℹ️ Info", id="info-button_klima_1_cor", color="primary", className="mr-1")

    # Create the info_card
    info_card_3 = dbc.Card(
        dbc.CardBody(
            [
                html.P([
                    "Um die Beziehung zwischen CO₂-Emissionen und Temperaturänderungen zu verstehen, könnten wir die Daten auf zwei Arten darstellen. ",
                    "Ein Datenexperte würde wahrscheinlich ein Streudiagramm verwenden, auf dem man sehen kann, wie sich CO₂-Emissionen im Vergleich ",
                    "zu Temperaturschwankungen entwickeln. Diese Methode mag aber für viele Menschen nicht leicht verständlich sein."
                ]),
                html.P([
                    "Um die Verbindung zwischen CO₂-Emissionen und Temperaturänderungen zu verdeutlichen, stelle dir vor, dass wir die Entwicklung von zwei ",
                    "wichtigen Faktoren im Klimawandel betrachten. Die Temperaturen steigen oder fallen, und gleichzeitig gibt es Veränderungen in der ",
                    "Menge an CO₂, die wir in die Atmosphäre freisetzen. Ein Datenexperte würde normalerweise Punkte auf einem Diagramm platzieren, um zu zeigen, ",
                    "wie diese beiden Faktoren zusammenhängen. Diese Punkte könnten dann durch eine Linie verbunden werden, um den Trend darzustellen."
                ]),
                html.P([
                    "Wenn wir uns das Diagramm anschauen, sieht es so aus, als ob die Punkte, die die CO₂-Mengen darstellen, eine Linie bilden. ",
                    "Das mag seltsam erscheinen, weil wir denken, dass es viele verschiedene Werte gibt. Tatsächlich ist es so, dass die Punkte aufgrund ",
                    "der Menge an Daten eng beieinander liegen und die Linie uns zeigt, wie sich die CO₂-Werte im Laufe der Zeit ändern. So können wir sehen, ",
                    "dass, wenn wir mehr CO₂ ausstoßen, die Temperaturen tendenziell steigen. Das Streudiagramm hilft uns also, diesen Zusammenhang besser zu verstehen. ",
                    "Es zeigt nicht nur, dass die beiden Faktoren miteinander verbunden sind, sondern auch, wie sie sich im Zeitverlauf verändern."
                ]),
            ],
            className="card-text",
        ),
        id="info-card_klima_1_cor",
        style={"display": "none"},  # Karte wird standardmäßig ausgeblendet
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_3,
        info_card_3,
        dcc.Graph(
            id=graph_id,
            figure=fig,
            config={'displayModeBar': False},
        )
    ])

    return graph_with_info_button

def create_dual_axis_plot_bar_line(df_temp, df_co2):
    graph_id = 'dual-axis-plot-bar-line'

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Assuming both DataFrames have a 'Year' column
    common_years = set(df_temp['Year']).intersection(set(df_co2['Year']))

    # Filter DataFrames to include only common years
    df_temp_filtered = df_temp[df_temp['Year'].isin(common_years)]
    df_co2_filtered = df_co2[df_co2['Year'].isin(common_years)]

    # Add traces
    # Bar trace for the first dataset with a color bar
    bar_trace = go.Bar(
        x=df_temp_filtered['Year'],
        y=df_temp_filtered['JJA'],
        name='Temperatur (°C)',
        showlegend=False,
        marker=dict(color=df_temp_filtered['JJA'], colorscale='inferno', colorbar=dict(x=0.48, y=-0.2, orientation='h')),
    )

    # Line trace for the second dataset
    line_trace = go.Scatter(x=df_co2_filtered['Year'],
                            y=df_co2_filtered['Annual CO₂ emissions'],
                            name='CO₂-Emissionen in Mio. t',
                            showlegend=False,
                            line=dict(color='red'))

    # Add traces to the figure
    fig.add_trace(bar_trace, secondary_y=False)
    fig.add_trace(line_trace, secondary_y=True)

    # Add figure title
    fig.update_layout(
        title_text='Temperature / CO₂-Emissionen',
        height=800,  # Set the height of the plot
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Jahr")

    # Set y-axes titles
    fig.update_yaxes(title_text='Temperatur (°C)', secondary_y=False)
    fig.update_yaxes(title_text='CO₂-Emissionen in Mio. t', secondary_y=True)

    # Update layout
    fig.update_layout(
        template='plotly_dark',
    )

    # Convert Plotly figure to Dash Graph component with the specified ID
    # Create "ℹ️ Info" button
    info_button_4 = dbc.Button("ℹ️ Info", id="info-button_klima_1_barplot", color="primary", className="mr-1")

    # Create the info_card
    info_card_4 = dbc.Card(
        dbc.CardBody(
            [
                html.P([
                    "Eine einfachere Alternative wäre, die beiden Diagramme direkt nebeneinander zu zeigen. Du könntest so besser erkennen, ",
                    "wie sich die Temperaturen und CO₂-Emissionen im Laufe der Zeit ändern. Allerdings ist es nicht ganz einfach, diese auf dem gleichen Diagramm abzubilden, ",
                    "da die Temperaturen in Grad Celsius gemessen werden, während die CO₂-Emissionen in Milliarden Tonnen angegeben sind. Um dieses Problem zu lösen, könnten wir ",
                    "ein spezielles Diagramm nutzen, das zwei vertikale Achsen hat, aber dieselbe Zeit auf der horizontalen Achse."
                ]),
                html.Hr(),
                html.P([
                    "Auf diesem Diagramm sind auf der linken Seite die Temperaturentwicklungen und auf der rechten Seite die CO₂-Emissionen abgebildet.",
                    "Das Streudiagramm der CO₂-Emissionen erscheint vielleicht seltsam, aber es dient dazu, den Zusammenhang zwischen den Daten zu verdeutlichen. ",
                    "Für ein allgemeines Publikum könnte jedoch diese Darstellung helfen, die Verbindung zwischen steigenden CO₂-Emissionen und Temperaturveränderungen besser zu verstehen."
                ]),
                html.Hr(),
                html.P([
                    "Wir können den wissenschaftlichen Konsens akzeptieren, dass CO₂-Emissionen die globale Erwärmung verstärkt, müssen jedoch gleichzeitig anerkennen, ",
                    "dass auch andere Faktoren eine Rolle spielen. Temperaturveränderungen sind nicht allein darauf zurückzuführen, dass Menschen Treibhausgase in die Atmosphäre entlassen. ",
                    "Wie die ",
                    html.A("Umweltschutzbehörde der Vereinigten Staaten (EPA)", href="https://www.epa.gov/climatechange-science/causes-climate-change"),
                    " klarstellt, gibt es auch andere Faktoren wie solare Aktivität und Veränderungen in der ",
                    "Reflektivität der Erde, etwa durch das abschmelzen der Pole oder der Entwaldung. Es gibt auch Treibhausgase neben Kohlendioxid, wie Methan und Lachgas. Die EPA stellt hierbei jedoch auch klar, ",
                    "dass keiner der Ursachen außer den menschengenerierten Treibhausgasemissionen das aktuelle Ausmaß des Klimawandels erklären kann."
                ]),
            ],
            className="card-text",
        ),
        id="info-card_klima_1_barplot",
        style={"display": "none"},
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_4,
        info_card_4,
        dcc.Graph(
            id=graph_id,
            figure=fig,
            config={'displayModeBar': False},
        )
    ])

    return graph_with_info_button

def make_owid_info_modal():
    return html.Div(
        children=[
            dbc.Button(
                [html.I(className="fas fa-info-circle"), " CO2 Datensatz"], 
                id="open-modal-button", 
                className="mt-2 mb-2", 
                color="primary"
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("owid-co2-data.csv")),
                    dbc.ModalBody(
                        [
                            html.P(
                                [
                                    "Die hier verwendeten Daten zu CO₂- und Treibhausgasemissionen stammen von ",
                                    html.A("Our World in Data", href="https://ourworldindata.org", target="_blank", className="link-primary"),
                                    " und basieren auf dem ",
                                    html.A("Global Carbon Project", href="https://www.globalcarbonproject.org", target="_blank", className="link-primary"),
                                    " (ausführlichere Informationen zu diesem Basisdatensatz finden sich ",
                                    html.A("hier", href="https://figshare.com/articles/preprint/The_Global_Carbon_Project_s_fossil_CO2_emissions_dataset/16729084", target="_blank", className="link-primary"),
                                    "). Visualisierungen und Texte sind unter der Creative Commons Lizenz (CC BY) lizenziert, die es Ihnen ermöglicht, die Materialien für jeglichen Zweck frei zu nutzen. ",
                                    "Der Code und die Daten sind unter der MIT-Lizenz verfügbar. Für eine detaillierte Nutzung und um die genauen Lizenzbedingungen einzusehen, besuchen Sie bitte direkt das GitHub-Repository sowie die offizielle Website."
                                ]
                            ),
                            html.A("GitHub-Repository", href="https://github.com/owid/co2-data", target="_blank", className="link-primary"),
                            html.Br(),
                            html.A("Our World in Data", href="https://ourworldindata.org", target="_blank", className="link-primary"),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Schließen", id="close-modal-button", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="modal",
                is_open=False,  # Modal ist standardmäßig geschlossen
            ),
        ]
    )

def make_gistemp_info_modal():
    return html.Div(
        children=[
            dbc.Button(
                [html.I(className="fas fa-info-circle"), " Temperaturdatensatz"], 
                id="open-gistemp-modal-button", 
                className="mt-2 mb-2", 
                color="primary"
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("GLB.Ts+dSST.csv")),
                    dbc.ModalBody(
                        [
                            html.P(
                                [
                                    "Die ",
                                    html.A("Temperaturdaten", href="https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt", target="_blank", style={"color": "black", "text-decoration": "underline"}),
                                    " stammen von der National Aeronautics and Space Administration (",
                                    html.A("NASA", href="https://www.nasa.gov/", target="_blank", style={"color": "black", "text-decoration": "underline"}),
                                    ") und stellen eine Schätzung der globalen Veränderung der Oberflächentemperatur dar.",
                                    " Sie beinhalten Temperaturanomalien, die von meteorologischen Stationen und ozeanischen Messpunkten abgeleitet sind (nähre Informationen zum Datensatz finden sich ",
                                    html.A("hier", href="https://data.giss.nasa.gov/gistemp/", target="_blank", style={"color": "black", "text-decoration": "underline"}),
                                    "). Die Daten und Visualisierungen sind gemäß den Richtlinien der NASA zur Verwendung von Bildern und Medien frei nutzbar, wobei eine Quellenangabe erforderlich ist. Programme und der Quellcode der Analyse sind öffentlich zugänglich und dürfen unter Einhaltung der jeweiligen Lizenzbedingungen genutzt werden. Bitte beachten Sie die genauen Nutzungsbedingungen und Referenzierungsanforderungen auf der offiziellen ",
                                    html.A("Goddard Institute for Space Studies-Website", href="https://www.giss.nasa.gov/", target="_blank", className="link-primary"),
                                    "."
                                ]
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Schließen", id="close-gistemp-modal-button", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="gistemp-modal",
                is_open=False,  # Modal ist standardmäßig geschlossen
            ),
        ]
    )
# ------------------------------------------------------------------------------
# klima_1 functions
# ------------------------------------------------------------------------------
def make_klima_1_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " CO2 Emittenten"],
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/klima_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " World Map"], 
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/klima_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
    brand=html.Span([link_icon, " Klimatologie:"],
        style={"text-decoration": "underline", "color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Klimatologie",
        color="primary",
        dark=True,
        className="d-flex justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P("Die Rolle von Kohlendioxidemissionen als Haupttreiber des globalen Klimawandels steht außer Frage. Ein breiter Konsens besteht darüber, dass eine rasche Reduzierung dieser Emissionen unerlässlich ist, um die schlimmsten Auswirkungen des Klimawandels zu verhindern. In internationalen Diskussionen ist die Verteilung der Verantwortung für Emissionsreduktionen jedoch ein kontroverses Thema."),
                    html.P("Die Uneinigkeit erstreckt sich über Regionen, Länder und sogar individuelle Verantwortlichkeiten. Unterschiedliche Vergleichsmethoden tragen zu vielfältigen Erzählungen bei. Die Analyse jährlicher Emissionen pro Land gibt Einblicke in nationale Beiträge, während die Betrachtung von Emissionen pro Person individuelle Verantwortlichkeiten verdeutlicht. Historische Emissionsbeiträge werfen zudem die Frage auf, wer historisch gesehen maßgeblich zur aktuellen Klimakrise beigetragen hat."),
                    html.P("Diese vielschichtigen Ansätze spiegeln die Herausforderungen wider, die mit der fairen Verteilung der Bürde zur Emissionsreduktion einhergehen. Internationale Bemühungen, ein ausgewogenes und gerechtes System zu schaffen, stehen im Fokus, um gemeinsam die globale Erwärmung zu begrenzen und die planetarische Gesundheit zu erhalten."),
                ],
                className='mb-3',
                #style={'max-width': '600px'}
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_klima_2', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                            "Die Rekonstruktion historischer CO2-Emissionen aus fossilen Brennstoffen seit dem Jahr 1751 beruht auf einer Zusammenstellung von Energiestatistiken und Handelsdaten. Die Grundlage dieser Rekonstruktion bilden Produktionsmengen von Kohle, Braunkohle, Torf und Rohöl, die in nationale Analysen der fossilen Brennstoffproduktion und CO2-Emissionen einfließen. Für aktuellere Daten greift man auf Informationen der ",
                            html.A("UN-Statistikabteilung", href="https://unstats.un.org/UNSDWebsite/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " zurück, die offizielle nationale Veröffentlichungen sowie jährliche Fragebögen nutzt."
                        ]),
                        
                        html.P([
                            "Die Berücksichtigung von Daten zur Zementproduktion und Gasfackelung erfolgt auf Basis von UN-Daten, dem ",
                            html.A("Geological Survey (USGS)", href="https://www.usgs.gov/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " und der ",
                            html.A("US-Energieinformationsverwaltung", href="https://www.eia.gov/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ". Um genaue Schätzungen der CO2-Emissionen zu erhalten, ist eine zuverlässige Abdeckung von Inlands- und Handelsenergie entscheidend, wobei das Verständnis in den letzten beiden Jahrhunderten zunehmend präzisiert wurde."
                        ]),
                        
                        html.P([
                            "Der Internationale Ausschuss für Klimaänderungen (",
                            html.A("IPCC", href="https://www.ipcc.ch/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ") bietet klare Richtlinien für die nationale Messung von CO2-Emissionen. Dennoch bleiben Unsicherheitsquellen bestehen, vor allem in Bezug auf die Berichterstattung über den Energieverbrauch und die Annahme von Emissionsfaktoren. Die Größe eines Landes und die Unsicherheit in den Berechnungen beeinflussen maßgeblich die Genauigkeit globaler Emissionszahlen."
                        ]),
                        
                        html.P([
                            "Ein Beispiel für solche Unsicherheiten zeigt sich in Chinas Emissionsbericht von 2013. Hier führte die Verwendung globaler Durchschnittsemissionsfaktoren zu einer Überbewertung um 10%. Insgesamt liegt die Unsicherheit bei globalen CO2-Emissionen üblicherweise im Bereich von 2-5%, was die Komplexität und Herausforderungen bei der präzisen Erfassung dieser entscheidenden Umweltindikatoren verdeutlicht."
                        ]),
                        
                        html.Hr(),
                        html.H4("Verwendete Datensätze:"),
                        html.P([
                            "Daten für die hier verwendeten Treemaps stützen sich auf Datensätze von ",
                            html.A("Our World in Data", href="https://ourworldindata.org/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ". Weitere Informationen zur Zusammenstellung sowie Prozessierung des Datensatzes finden sich ",
                            html.A("hier", href="https://github.com/owid/co2-data", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ".",
                        ]),

                        html.P([  
                            "Der umfangreiche Owid Datensatz wurde nur teilweise übernommen, umstrukturiert und um einige ",
                            html.A("Datenpunkte", href="https://github.com/owid/owid-datasets/tree/master/datasets/Countries%20Continents", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " zur Zuordnung einzelner Länder zu ihren jeweiligen Kontinenten ergänzt. Ausführlichere Informationen zur Prozessierung der Datensätze finden sich im ",
                            html.A("Quellcode", href="https://github.com/Neon-Purplelight/klima_kompass_navigator/blob/main/utils/dataManager.py", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ".",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}
                ),
                id='collapse_more_info_klima_2',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_klima_2', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar and second row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_klima_1_settings(default_value='co2_emissions_per_country', options=None):
    if options is None:
        options = [
            {'label': 'Durchschnittliche CO₂-Emissionen der letzten 5 Jahre', 'value': 'co2_emissions_per_country'},
            {'label': 'Historischer CO₂ Gesamtausstoß', 'value': 'co2_emissions_historic'},
            {'label': 'CO₂ Ausstoß pro Kopf', 'value': 'co2_emissions_per_capita'}
        ]

    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                    dbc.CardBody(
                        [
                            dbc.Label("Wähle Ansicht:", html_for='klima-2-plot-selector', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='klima-2-plot-selector',
                                options=[{'label': option['label'], 'value': option['value']} for option in options],
                                value=default_value,
                                clearable=False,
                            ),
                            html.Div(id='klima-2-plot-container', children=[]),
                        ]
                    ),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def create_co2_treemap(df_filtered):    
    # Fixed height value
    height = 1000

    # Filter the DataFrame to include the last 5 years
    last_5_years_data = df_filtered[df_filtered['year'] >= df_filtered['year'].max() - 4].copy()

    # Create a new column for the top level (in this case, "world")
    last_5_years_data['world'] = 'World'

    # Calculate the log transformation, handling NaN values
    last_5_years_data.loc[:, 'log_co2'] = np.log1p(last_5_years_data['co2'])

    # Group by country and continent and calculate the mean for each group
    average_co2_data = last_5_years_data.groupby(['world', 'continent', 'country']).agg(
        {'co2': 'mean', 'log_co2': 'mean'}).reset_index()

    # Calculate the percentage of CO2 contribution for each country and continent relative to the world
    total_world_co2 = average_co2_data[average_co2_data['world'] == 'World']['co2'].sum()
    average_co2_data['percentage_co2'] = (average_co2_data['co2'] / total_world_co2) * 100

    # Create the Plotly Express treemap figure
    fig = px.treemap(average_co2_data, path=['world', 'continent', 'country'], values='co2',
                     labels={'co2': 'CO₂-Emissionen'},
                     color='log_co2',
                     color_continuous_scale='RdYlGn_r',
                     custom_data=['continent', 'country', 'co2', 'percentage_co2'],
                     height=height, 
                     template='plotly',
    )

    # Update traces to make corners round
    fig.update_traces(marker=dict(cornerradius=5))

    # Update hover template to display continent name for continents and country name for countries
    fig.update_traces(hovertemplate='<b>%{label}</b><br>CO₂-Emissionen: %{customdata[2]:,.2f} Mrd. t<br>Prozentualer Anteil am weltweiten Ausstoß: %{customdata[3]:.2f} %', selector=dict(type='treemap'))

    # Update hover template for the third level to an empty string
    fig.update_traces(hovertemplate='', selector=dict(type='treemap', level='current entries'))

    # Remove colorscale bar
    fig.update_coloraxes(showscale=False)

    # Create "ℹ️ Info" button
    info_button_1 = dbc.Button("ℹ️ Info", id="info-button_klima_2_co2_treemap", color="primary", className="mr-1")

    # Create the info_card
    info_card_1 = dbc.Card(
        dbc.CardBody(
            [
                html.P("Durchschnittliche CO2-Emissionen der letzten 5 Jahre visualisiert durch eine 'Baumkarte'. Jedes Rechteck repräsentiert ein Land, gruppiert nach den jeweiligen Kontinenten. Die Größe der Rechtecke entsprechen hierbei ihren relativen Beitrag zum Weltweiten Gesamtausstoß."),
                html.Hr(),
                html.Strong("Asien:"),
                html.Ul(
                    [
                        html.Li("Jährliche CO2-Emissionen von etwa 20,7 Milliarden Tonnen."),
                        html.Li("Beherbergt 60% der Weltbevölkerung."),
                        html.Li("Pro-Kopf-Emissionen in Asien daher leicht unter dem weltweiten Durchschnitt."),
                    ]
                ),
                html.Strong("China:"),
                html.Ul(
                    [
                        html.Li("Größter Emittent weltweit."),
                        html.Li("Jährliche CO2-Emissionen von etwa 10,7 Milliarden Tonnen."),
                        html.Li("Trägt mehr als ein Viertel zu den globalen Emissionen bei."),
                    ]
                ),
                html.Strong("Nordamerika:"),
                html.Ul(
                    [
                        html.Li("Zweigrößter regionaler Emittent weltweit."),
                        html.Li("Jährliche CO2-Emissionen von etwa 6,3 Milliarden Tonnen."),
                        html.Li("USA dominieren den Beitrag zu den nordamerikanischen Emissionen."),
                    ]
                ),
                html.Strong("Europa:"),
                html.Ul(
                    [
                        html.Li("Drittgrößter regionaler Emittent weltweit."),
                        html.Li("Jährliche CO2-Emissionen von etwa 5,4 Milliarden Tonnen."),
                    ]
                ),
                html.Strong("Afrika und Südamerika:"),
                html.Ul(
                    [
                        html.Li("Beide Regionen tragen jeweils 3-4% zu den globalen Emissionen bei."),
                        html.Li("Emissionen in etwa vergleichbar mit internationalem Flugverkehr und Schifffahrt."),
                        html.Li("Diese sind hier explizit ausgelassen, da nicht eindeutig zugeordnet werden kann, ob sie dem Land der Abreise, dem Herkunftsland oder anderen beteiligten Ländern zuzuordnen sind."),
                    ]
                ),
                html.Hr(),
            ],
            className="card-text",
        ),
        id="info-card_klima_2_co2_treemap",
        style={"display": "none"},  # Karte wird standardmäßig ausgeblendet
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_1,
        info_card_1,
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={'height': height}
        )
    ])

    return graph_with_info_button

def create_co2_treemap_historic(df_filtered):

    height = 1000

    # Find the last available year in the DataFrame
    last_year = df_filtered['year'].max()

    # Filter the DataFrame to include only the data for the last available year
    last_year_data = df_filtered[df_filtered['year'] == last_year].copy()

    # Create a new column for the top level (in this case, "world")
    last_year_data['world'] = 'World'

    # Calculate the log transformation, handling NaN values
    last_year_data.loc[:, 'log_cumulative_co2'] = np.log1p(last_year_data['cumulative_co2'])

    # Calculate the percentage of CO2 contribution for each country and continent relative to the world
    total_world_co2 = last_year_data[last_year_data['world'] == 'World']['cumulative_co2'].sum()
    last_year_data['percentage_cumulative_co2'] = (last_year_data['cumulative_co2'] / total_world_co2) * 100

    fig = px.treemap(last_year_data, path=['world', 'continent', 'country'], values='cumulative_co2',
                     labels={'cumulative_co2': 'Cumulative CO₂-Emissionen'},
                     color='log_cumulative_co2',
                     color_continuous_scale='RdYlGn_r',
                     custom_data=['continent', 'country', 'cumulative_co2', 'percentage_cumulative_co2'],
                     height=height
    )

    # Update traces to make corners round
    fig.update_traces(marker=dict(cornerradius=5))

    # Update hover template to display continent name for continents and country name for countries
    fig.update_traces(hovertemplate='<b>%{label}</b><br>CO₂ Gesamt- Emissionen: %{customdata[2]:,.2f} Mrd. t<br>Prozentualer Anteil am weltweiten Ausstoß: %{customdata[3]:.2f}%', selector=dict(type='treemap'))

    # Update hover template for the third level to an empty string
    fig.update_traces(hovertemplate='', selector=dict(type='treemap', level='current entries'))

    # Remove colorscale bar
    fig.update_coloraxes(showscale=False)

    # Create "ℹ️ Info" button
    info_button_2 = dbc.Button("ℹ️ Info", id="info-button_klima_2_historic_treemap", color="primary", className="mr-1")

    # Create the info_card
    info_card_2 = dbc.Card(
        dbc.CardBody(
            [
                html.P("Seit 1751 hat die Welt über 1,5 Billionen Tonnen CO2 emittiert, und es ist dringend notwendig, die Emissionen zu reduzieren, um das Klimaziel von maximal 2°C Temperaturanstieg zu erreichen. Einige sind der Meinung, dass die reichen Länder, welche historisch betrachtet am meisten zum CO2 ausgestoßen haben, eine größere Verantwortung tragen sollten."),
                html.Hr(),
                html.Strong("1. USA als größter Emittent:"),
                html.P("Die Vereinigten Staaten haben mit etwa 421 Milliarden Tonnen seit 1751 mehr CO2 emittiert als jedes andere Land, was rund ein Viertel der historischen Emissionen ausmacht. Dies ist fast doppelt so viel wie der Beitrag Chinas."),

                html.Strong("2. Europa, Asien und Nordamerika:"),
                html.P("Europa und Asien haben historisch betrachtet ähnliche Beiträge zu den globalen Emissionen geleistet und liegen somit beide insgesamt noch vor Nordamerika."),

                html.Strong("3. Aktuelle große Emittenten:"),
                html.P("Länder wie Indien und Brasilien, die heute zu den größten jährlichen Emittenten gehören, haben historisch gesehen einen geringeren Beitrag zu den kumulierten (aufaddierten) Emissionen geleistet."),

                html.Strong("4. Deutschlands Beitrag:"),
                html.P("Wenn man die kumulierten Emissionen betrachtet, steht Deutschland im historisch verglichen mit seinen aktuellen Emissionen, welche zwischen 5 % und 6 % ausmachen, schlechter da."),

                html.Strong("5. Afrikas Beitrag:"),
                html.P("Aufgrund sehr niedriger pro-Kopf-Emissionen ist der Beitrag Afrikas zu den globalen Emissionen sowohl historisch als auch aktuell relativ gering."),
                html.Hr(),
                html.P("Diese Repräsentation von CO2 Emissionen betonen die Notwendigkeit einer globalen Anstrengung, insbesondere von Ländern mit höheren historischen Emissionen, um die Emissionen zu reduzieren und das Klimaziel zu erreichen."),
            ],
            className="card-text",
        ),
        id="info-card_klima_2_historic_treemap",
        style={"display": "none"},
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_2,
        info_card_2,
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={'height': height}
        )
    ])

    return graph_with_info_button

def create_co2_treemap_per_capita(df_filtered):
    
    height = 1000

    # Find the last available year in the DataFrame
    last_year = df_filtered['year'].max()

    # Filter the DataFrame to include only the data for the last available year
    last_year_data = df_filtered[df_filtered['year'] == last_year].copy()

    # Create a new column for the top level (in this case, "world")
    last_year_data['world'] = 'World'

    # Calculate the log transformation, handling NaN values
    last_year_data.loc[:, 'log_co2_per_capita'] = np.log1p(last_year_data['co2_per_capita'])

    # Calculate the percentage of CO2 contribution for each country and continent relative to the world
    total_world_co2 = last_year_data[last_year_data['world'] == 'World']['co2_per_capita'].sum()
    last_year_data['percentage_co2_per_capita'] = (last_year_data['co2_per_capita'] / total_world_co2) * 100

    fig = px.treemap(last_year_data, path=['world', 'continent', 'country'], values='co2_per_capita',
                     labels={'co2_per_capita': 'CO₂-Emissionen pro Kopf'},
                     color='log_co2_per_capita',
                     color_continuous_scale='RdYlGn_r',
                     custom_data=['continent', 'country', 'co2_per_capita', 'percentage_co2_per_capita'],
                     height=height
    )

    # Update traces to make corners round
    fig.update_traces(marker=dict(cornerradius=5))

    # Update hover template to display continent name for continents and country name for countries
    fig.update_traces(hovertemplate='<b>%{label}</b><br>CO₂ pro Kopf: %{customdata[2]:,.2f} t<br>Prozentualer Anteil am weltweiten Ausstoß: %{customdata[3]:.2f}%', selector=dict(type='treemap'))

    # Update hover template for the third level to an empty string
    fig.update_traces(hovertemplate='', selector=dict(type='treemap', level='current entries'))

    # Remove colorscale bar
    fig.update_coloraxes(showscale=False)

    # Create "ℹ️ Info" button
    info_button_3 = dbc.Button("ℹ️ Info", id="info-button_klima_2_per_capita_treemap", color="primary", className="mr-1")

    # Create the info_card
    info_card_3 = dbc.Card(
        dbc.CardBody(
            [
                html.P("Die weltweiten durchschnittlichen Pro Kopf CO2-Emissionen errechnen sich aus den Gesamtemissionen geteilt durch die Bevölkerung. Die Pro Kopf Emissionen variieren stark. Die größten pro Kopf-Emittenten sind oft ölproduzierende Länder, hauptsächlich in der Nahostregion. Länder mit niedriger Bevölkerung, wie viele Ölproduzenten, haben insgesamt jedoch niedrige Emissionen, während bevölkerungsreiche Länder wie die USA, Australien und Kanada trotz niedrigeren pro Kopf-Emissionen insgesamt überproportional zu den Gesamtemissionen beitragen."),
                html.Hr(),
                html.Ul(
                    [
                        html.Li("Katar führt mit 35 Tonnen pro Person an, gefolgt von Ländern wie Trinidad und Tobago, Kuwait, den Vereinigten Arabischen Emiraten, Brunei, Bahrain und Saudi-Arabien."),
                        html.Li("Australien hatte eine durchschnittliche pro Kopf-Emission von 15 Tonnen, gefolgt von den USA mit knapp unter 15 Tonnen und Kanada mit rund 14 Tonnen – mehr als das Dreifache des globalen Durchschnitts (etwa 4,8 Tonnen)."),
                        html.Li("In Europa gibt es erhebliche Unterschiede, wobei einige Länder wie Portugal, Frankreich und das Vereinigte Königreich niedrigere Emissionen als vergleichbare Länder wie Deutschland (etwa 8 Tonnen) aufweisen."),
                        html.Li("Wieder haben viele arme Länder im Süden die niedrigsten Emissionen. Gleichzeitig leiden sie jedoch oft am stärksten unter den Auswirkungen des Klimawandels"),
                    ]
                ),
                html.Hr(),
                html.P("Wohlstand ist ein Haupttreiber von CO2-Emissionen, aber politische und technologische Entscheidungen spielen ebenfalls eine Rolle. Insgesamt gibt es erhebliche Unterschiede in den pro Kopf-Emissionen zwischen Ländern mit ähnlichem Lebensstandard."),
                html.P(
                    ["Doch auch innerhalb der Länder können die Pro Kopf Emissionen sehr ungleich verteilt sein. Laut des ",
                    html.A("World Inequality Reports 2022", href="https://wir2022.wid.world/www-site/uploads/2021/12/WorldInequalityReport2022_Full_Report.pdf"),
                    " stößt reichste Hundertstel der Deutschen pro Kopf im Jahr 117,8 Tonnen an Klimagasen aus. Die obersten 10 % kommen im Durchschnitt auf 34,1 Tonnen, die “Mitte” auf 12.2 Tonnen und die unteren 50 % nur auf 5,9 Tonnen. Die Reichen produzieren also 20-mal so viel CO2 wie die Armen."]), 
                html.P("Der Pro Kopf Ausstoß spielt auch eine wichtige Rolle hinsichtlich des Zeitpunktes an dem ein Land Klimaneutral werden muss, um das 1,5 °Grad Ziel zu erreichen. Im Falle Deutschlands wäre dies beispielsweise das Jahr 2035. Indien hingegen erst um 2090, da der CO2 Pro- Kopf- Ausstoß bei nur 1,9 Tonnen liegt."),
            ],
            className="card-text",
        ),
        id="info-card_klima_2_per_capita_treemap",
        style={"display": "none"},
    )

    # Combine the button, info_card, and graph
    graph_with_info_button = html.Div([
        info_button_3,
        info_card_3,
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={'height': height}
        )
    ])

    return graph_with_info_button


# ------------------------------------------------------------------------------
# klima_2 functions
# ------------------------------------------------------------------------------
def make_klima_2_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " CO2 Emittenten"],
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/klima_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " World Map"], 
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/klima_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
    brand=html.Span([link_icon, " Klimatologie:"],
        style={"text-decoration": "underline", "color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Klimatologie",
        color="primary",
        dark=True,
        className="d-flex justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_klima_2', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
                        ]),
                        html.Hr(),
                        html.H4("Verwendete Datensätze:"),
                        html.P([  
                            "Lorem Ipsum",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_klima_2',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_klima_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_co2_world_map(translated_country_options, min_year, max_year, chart_type_buttons):
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                        dbc.CardBody([
                            html.Label("Beobachtungsgegenstand:", htmlFor='co2-type-selector', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='co2-type-selector',
                                options=[
                                    {'label': 'Bevölkerung', 'value': 'population'},
                                    {'label': 'BIP', 'value': 'gdp'},
                                    {'label': 'CO2', 'value': 'co2'},
                                    {'label': 'Kohle-CO2', 'value': 'coal_co2'},
                                    {'label': 'Öl-CO2', 'value': 'oil_co2'},
                                    {'label': 'Gas-CO2', 'value': 'gas_co2'},
                                    {'label': 'Zement-CO2', 'value': 'cement_co2'},
                                    {'label': 'Fackel-CO2', 'value': 'flaring_co2'},
                                    {'label': 'CO2 pro Kopf', 'value': 'co2_per_capita'},
                                    {'label': 'Landnutzungsänderung CO2', 'value': 'land_use_change_co2'},
                                    {'label': 'Anteil am globalen CO2', 'value': 'share_global_co2'},
                                    {'label': 'Temperaturänderung durch CO2', 'value': 'temperature_change_from_co2'},
                                    {'label': 'Gesamte Treibhausgase', 'value': 'total_ghg'},
                                    {'label': 'Gesamte Treibhausgase ohne LUCF', 'value': 'total_ghg_excluding_lucf'}
                                ],
                                value='co2',
                                className="mb-3",
                                style={'color': 'black'}  # Textfarbe auf Schwarz ändern
                            ),

                            dcc.Dropdown(
                                id='country-selector',
                                options=translated_country_options,  # Verwenden der übersetzten Optionen
                                value=[],
                                multi=True,
                                className="mb-3",
                                style={'color': 'black'}  # Textfarbe auf Schwarz ändern
                            ),
                            html.Label("Zeitraum:", htmlFor='year-slider', style={'color': 'white'}),
                            dcc.RangeSlider(
                                id='year-slider',
                                min=min_year,
                                max=max_year,
                                value=[min_year, max_year],
                                marks={str(year): str(year) for year in range(min_year, max_year+1, 5)},
                            ),
                        ])
                    ],
                    color="primary",
                    style={'color': 'white'}
                )
            ),
        ]),
        chart_type_buttons,
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='chart', style={'height': '70vh'}),
                width=12
            )
        ]),
        html.Div(id='slider-output'),
        html.Div(id='chart-type-status', style={'display': 'none'})
    ], fluid=True)
    return layout

# ------------------------------------------------------------------------------
# hydro_1 functions
# ------------------------------------------------------------------------------
def make_hydro_1_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    # Verwenden Sie d-flex und justify-content-center, um Elemente zu zentrieren
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " Arktischer Eisschild"], 
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/hydro_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " Waldökosysteme und ihr Wasserhaushalt"], 
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/hydro_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
    brand=html.Span([link_icon, " Hydrologie:"],
        style={"text-decoration": "underline","color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Hydrologie",
        color="primary",
        dark=True,
        className="d-flex flex-column justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P([
                    "Die Dashboards auf dieser Seite bieten Einblicke in die dynamischen Veränderungen des arktischen Eisschildes um die norwegische Inselgruppe ",
                    html.A("Spitzbergen ", href="https://de.wikipedia.org/wiki/Spitzbergen_(Inselgruppe)", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    "(Sie können auf der Karte jedoch auch andere Regionen betrachten). Die Darstellung findet zum einen auf einer monatlichen Basis (Januar bis Dezember 2023) und zum anderen auf einer jährlichen Basis (2007 bis 2023) statt. Die Darstellung der monatlichen Veränderungen von Januar bis Dezember vermittelt den Eindruck, als ob der arktische Eisschild 'atmet', da er auf Wetterbedingungen reagiert. Dieser dynamische Prozess zeigt, wie sich das Eis im Laufe eines Jahres entwickelt und verändert. Die Analyse der jährlichen Veränderungen über den Zeitraum von 2007 bis 2023 bietet einen tieferen Einblick in die langfristigen Trends des arktischen Eisschildes. Hier wird der Fokus auf klimatische Veränderungen gelegt, wodurch Muster und Trends sichtbar werden. Dieser Ansicht gibt einen Überblick über die Entwicklung des Eisschildes im Kontext des Klimawandels und ermöglicht es, längerfristige Trends und Veränderungen zu identifizieren.",
                    ]),
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_hydro_1', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                        "Der Klimawandel hat erhebliche Auswirkungen auf die arktischen Eisschilde, die eine zentrale Rolle im globalen Klimasystem spielen. Die steigenden Temperaturen in der Arktis führen zu einer ",
                        html.A("beschleunigten Eisschmelze", href="https://www.ardalpha.de/wissen/umwelt/klima/klimawandel/eisschmelze-antarktis-arktis-polkappen-schmelzen-nordpol-suedpol-100.html", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ", insbesondere auf Grönland und der Arktischen Ozeanregion. Dies hat weitreichende Konsequenzen, da die schwindenden Eismassen den Meeresspiegel ansteigen lassen und potenziell zu katastrophalen Überschwemmungen in küstennahen Gebieten führen können. Darüber hinaus, hat der Rückgang der Eismassen auch Auswirkungen auf ",
                        html.A("Meeresströmungen", href="https://www.sueddeutsche.de/wissen/golfstrom-klimawandel-amoc-groenland-1.5374481", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ", welche einen bedeutenden Einfluss im globalen Klimasystem ausüben."
                        ]),
                        html.P([
                            "Schließlich spielt die Arktis auch eine entscheidende Rolle hinsichtlich ihrer ",
                            html.A("Albedo-Funktion", href="https://studyflix.de/erdkunde/albedo-5698", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " , d.h. ihrer Fähigkeit Sonnenlicht zu reflektieren. Das helle Eis der arktischen Region reflektiert einen beträchtlichen Teil der einfallenden Sonnenstrahlung zurück ins Weltall. Mit zunehmender Eisschmelze und dem Rückgang der Eisbedeckung reduziert sich die Albedo der Arktis jedoch, da dunklere Wasseroberflächen mehr Sonnenlicht absorbieren und somit zusätzlich zur Erwärmung des Wassers beiträgt, was wiederum die Eisschmelze weiter vorantreibt."
                        ]),      
                        html.Hr(),
                        html.H4("Verwendete Datensätze:"),
                        html.P([  
                            "Die verwendeten Shapefiles basieren auf den täglichen Eisanalysen des U.S. National Ice Center (",
                            html.A("USNIC", href="https://usicecenter.gov/About", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ") Den vollen Datenkatalog der USNIC finden Sie ",
                            html.A("hier", href="https://usicecenter.gov/Products/ArcticData", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ".",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_hydro_1',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_hydro_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_hydro_1_settings(default_value='months', options=None):
    if options is None:
        options = [
            {'label': 'Veränderungen des arktischen Eisschildes innerhalb eines Jahres', 'value': 'months'},
            {'label': 'Veränderungen des arktischen Eisschildes innerhalb mehrerer Jahre', 'value': 'years'},
        ]

    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                    dbc.CardBody(
                        [
                            dbc.Label("Wähle Ansicht:", html_for='hydro-1-plot-selector', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='hydro-1-plot-selector',
                                options=[{'label': option['label'], 'value': option['value']} for option in options],
                                value=default_value,
                                clearable=False,
                            ),
                            html.Div(id='hydro-1-plot-container', children=[]),
                        ]
                    ),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def create_static_map_html_months(selected_months=[], available_months=[], display_names_months=[], shapefile_folder_months=[]):
    # Define the bounding box coordinates
    bounding_box = [
        [74, 4],
        [81, 4],
        [81, 39],
        [74, 39]
    ]

    # Define the Esri World Imagery basemap
    esri_imagery_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    esri_imagery_options = {
        'attribution': 'Map data &copy; <a href="https://www.esri.com/">Esri</a>',
        'maxZoom': 18
    }
    esri_imagery_layer = f'L.tileLayer("{esri_imagery_url}", {esri_imagery_options}).addTo(map)'

    # Generate the Leaflet map HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard with Static Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body>

    <!-- Create a map div with a specific id -->
    <div id="map" style="width: 100%; height: 500px; margin: auto; display: block;"></div>

    <script>
        // Define the bounding box coordinates
        var boundingBox = {bounding_box};

        // Calculate the center of the bounding box
        var centerLat = (boundingBox[0][0] + boundingBox[2][0]) / 2;
        var centerLon = (boundingBox[0][1] + boundingBox[2][1]) / 2;

        // Create the Leaflet map centered at the calculated center with an initial zoom level of 4
        var map = L.map('map').setView([centerLat, centerLon], 4);

        // Add a tile layer (Esri World Imagery in this case)
        {esri_imagery_layer}

        // Add Zoom Control
        L.control.zoom({{ position: 'topright' }}).addTo(map);
    """

    # Add GeoJSON layers for the selected months
    for selected_month in selected_months:
        # Find the corresponding filename from available_months
        if selected_month not in display_names_months:
            continue  # Skip if the selected_month is not in the list

        filename = available_months[display_names_months.index(selected_month)]
        shapefile_path = os.path.join(shapefile_folder_months, f'{filename}.shp')

        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f'Shapefile not found: {shapefile_path}')

        gdf = gpd.read_file(shapefile_path)

        # Convert the GeoDataFrame to GeoJSON
        geojson_data = gdf.to_crs(epsg='4326').to_json()

        # Add the GeoJSON data as a GeoJSON layer to the Leaflet map with style options
        geojson_layer = f'''
        var geojsonLayer_{selected_month} = L.geoJSON({geojson_data}, {{
            style: {{
                color: 'white',
                fillOpacity: 0.8,
                weight: 0
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip('<b>{selected_month}</b>', {{ sticky: true }});
                var isOrange = false;  // Flag to track color state

                layer.on('click', function () {{
                    if (isOrange) {{
                        layer.setStyle({{
                            color: 'white',
                            fillOpacity: 0.8,
                            weight: 0
                        }});
                    }} else {{
                        layer.setStyle({{
                            color: 'orange',
                            fillOpacity: 0.8,
                            weight: 2
                        }});
                    }}
                    isOrange = !isOrange;  // Toggle the flag
                }});
            }}
        }}).addTo(map);
        '''
        html_content += geojson_layer

    # Complete the HTML content
    html_content += """
    </script>

    <!-- You can add more content to your dashboard here -->

    </body>
    </html>
    """

    # Set the output file path within the data\originalData directory
    output_file = os.path.join('data', 'originalData', 'hydro_1', 'map_with_selected_months.html')

    # Save the HTML content to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

def create_static_map_html_years(selected_years=[], available_years=[], display_names_years=[], shapefile_folder_years=[]):
    # Define the bounding box coordinates
    bounding_box = [
        [74, 4],
        [81, 4],
        [81, 39],
        [74, 39]
    ]

    # Define the Esri World Imagery basemap
    esri_imagery_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    esri_imagery_options = {
        'attribution': 'Map data &copy; <a href="https://www.esri.com/">Esri</a>',
        'maxZoom': 18
    }
    esri_imagery_layer = f'L.tileLayer("{esri_imagery_url}", {esri_imagery_options}).addTo(map)'

    # Generate the Leaflet map HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard with Static Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body>

    <!-- Create a map div with a specific id -->
    <div id="map" style="width: 100%; height: 500px; margin: auto; display: block;"></div>

    <script>
        // Define the bounding box coordinates
        var boundingBox = {bounding_box};

        // Calculate the center of the bounding box
        var centerLat = (boundingBox[0][0] + boundingBox[2][0]) / 2;
        var centerLon = (boundingBox[0][1] + boundingBox[2][1]) / 2;

        // Create the Leaflet map centered at the calculated center with an initial zoom level of 4
        var map = L.map('map').setView([centerLat, centerLon], 4);

        // Add a tile layer (Esri World Imagery in this case)
        {esri_imagery_layer}
    """

    # Add GeoJSON layers for the selected years
    for selected_year in selected_years:
        # Find the corresponding filename from available_years
        if selected_year not in display_names_years:
            continue  # Skip if the selected_year is not in the list

        filename = available_years[display_names_years.index(selected_year)]
        shapefile_path = os.path.join(shapefile_folder_years, f'{filename}.shp')

        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f'Shapefile not found: {shapefile_path}')

        gdf = gpd.read_file(shapefile_path)

        # Convert the GeoDataFrame to GeoJSON
        geojson_data = gdf.to_crs(epsg='4326').to_json()

        # Add the GeoJSON data as a GeoJSON layer to the Leaflet map with style options
        geojson_layer = f'''
        var geojsonLayer_{selected_year} = L.geoJSON({geojson_data}, {{
            style: {{
                color: 'white',
                fillOpacity: 0.8,
                weight: 0
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip('<b>{selected_year}</b>', {{ sticky: true }});
                var isOrange = false;  // Flag to track color state

                layer.on('click', function () {{
                    if (isOrange) {{
                        layer.setStyle({{
                            color: 'white',
                            fillOpacity: 0.8,
                            weight: 0
                        }});
                    }} else {{
                        layer.setStyle({{
                            color: 'orange',
                            fillOpacity: 0.8,
                            weight: 2
                        }});
                    }}
                    isOrange = !isOrange;  // Toggle the flag
                }});
            }}
        }}).addTo(map);
        '''
        html_content += geojson_layer

    # Complete the HTML content
    html_content += """
    </script>

    <!-- You can add more content to your dashboard here -->

    </body>
    </html>
    """

    # Set the output file path within the data\originalData directory
    output_file = os.path.join('data', 'originalData', 'hydro_1', 'map_with_selected_years.html')

    # Save the HTML content to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# ------------------------------------------------------------------------------
# hydro_2 functions
# ------------------------------------------------------------------------------
def make_hydro_2_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Video-Icon Button
    video_icon_button = dbc.Button(
        children=[html.I(className="fa fa-play-circle")], 
        id="toggle-video-button", 
        color="info", 
        className="mb-2",
        style={"margin": "auto", "display": "block"}  # Zentriert den Button
    )

    # Video in dbc.Collapse
    video_collapse = dbc.Collapse(
        dbc.Card(
            dbc.CardBody(
                html.Iframe(src="https://www.youtube.com/embed/UTP99X3e7-A", width="100%", height="315", style={"border": "none"})
            )
        ),
        id="collapse-video",
        is_open=False
    )

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    # Verwenden Sie d-flex und justify-content-center, um Elemente zu zentrieren
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " Arktischer Eisschild"], 
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/hydro_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " Waldökosysteme und ihr Wasserhaushalt"], 
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/hydro_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
        brand=html.Span([link_icon, " Hydrologie:"], 
        style={"text-decoration": "underline", "color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Hydrologie",
        color="primary",
        dark=True,
        className="d-flex flex-column justify-content-center",
    )

    # Infotext und Video
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P([
                        "Der Klimawandel führt zu veränderten Niederschlagsmustern und erhöhten Temperaturen, was die Verfügbarkeit von Wasser in den Wäldern beeinflusst. In vielen Regionen Deutschlands hat die Zunahme von Trockenperioden bereits spürbare Auswirkungen auf die Waldgesundheit.",
                    ]),
                    html.Hr(),
                    video_icon_button,  # Fügen Sie den Button hier ein
                    video_collapse,     # und das ein-/ausklappbare Video
                    html.Hr(),
                    html.P([
                        "Diese Veränderungen im Wasserhaushalt wirken sich nicht nur auf das Wachstum und die Entwicklung der Bäume aus, sondern auch auf die Biodiversität und die Ökosystemdienstleistungen, die der Wald erbringt. Wasser ist dabei nicht nur Grundlage für die Photosynthese, sondern spielt darüber hinaus eine entscheidende Rolle für die allgemeine Gesundheit und Widerstandsfähigkeit gegenüber Schädlingen, wie dem Borkenkäfer, Unwetterereignissen oder Waldbränden.",
                        "Folgendes Dashboard veranschaulicht mittels unterschiedlicher Diagramme Statistiken zum Schadholzeinschlag. Unter Schadholzeinschlag versteht man die Entnahme von Bäumen aus einem Wald, die durch Schädlinge, Krankheiten, Sturm, Feuer oder andere schädigende Ereignisse beeinträchtigt oder zerstört wurden. ",
                    ]), 
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_hydro_1', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                        "Früher waren vor allem Unwetterereignisse (wie etwa 2007 der ",
                        html.A("Orkan Kyrill", href="https://de.wikipedia.org/wiki/Orkan_Kyrill", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " oder 2015 ",
                        html.A("Sturmtief Niklas", href="https://de.wikipedia.org/wiki/Orkan_Niklas", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ") die Hauptursache für Schadholz. Orkane oder Stürme sind meist Singuläre Ereignisse, welche von Jahr zu Jahr starken Schwankungen unterworfen sein können, sich daher aber auch deutlich in den Diagrammen ablesen lassen. Seit der großen Dürre von 2018 sind vor allem Schädlinge die Einschlagsursache Nummer 1. Ihr Anteil hat seit 2018 deutlich zugenommen und 2021 mit 81,4 % einen vorläufigen Höchststand erreicht (2012 hatte er noch bei 17,8 % gelegen)."
                        " Als Einschlagsursache wird schlussendlich lediglich die finale Ursache erfasst. Durch Trockenheit geschwächte Bäume sind anfälliger für alle anderen in der Statistik geführten Schadholzeinschlagsursachen. Daher wird Trockenheit seit 2020 auch als separate Schadholzkategorie geführt."
                        ]),  
                        html.P([
                        "Der Schadholzeinschlag berechnet sich auf Grundlage der ",
                        html.A("Holzeinschlagsstatistik", href="https://www.destatis.de/DE/Methoden/Qualitaet/Qualitaetsberichte/Land-Forstwirtschaft-Fischerei/holzeinschlagsstatistik.pdf?__blob=publicationFile", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " des statistischen Bundesamtes (",
                        html.A("Destatis", href="https://www.destatis.de/DE/Home/_inhalt.html", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        "). Diese jährliche Erhebung von Daten zum Rohholzaufkommen in Deutschland umfasst alle Betriebe, die Rohholz erzeugen, und berücksichtigt planmäßigen sowie schadensbedingten Einschlag. Die Datengewinnung kombiniert Verwaltungsdaten, direkte Befragung und Schätzungen. Die Genauigkeit variiert nach Waldeigentumsart und Erhebungsmethode. Die Datenerhebung erfolgt also einerseits über Verwaltungsdaten, die eine relativ hohe Genauigkeit aufweisen, und andererseits über Schätzungen und Stichprobenerhebungen, die mit gewissen Unsicherheiten behaftet sind. Besonders im Privatwald, wo die Waldflächen oft kleiner und die Bewirtschaftung nicht regelmäßig ist, müssen Schätzungen und Hochrechnungen vorgenommen werden."
                        ]),    
                        html.Hr(),
                        html.H4("Verwendete Datensätze:"),
                        html.P([  
                            "Die verwendeten Daten zur Menge des Schadholzeinschlages finden sich unter der Datenbank des statistischen Bundesamtes (",
                            html.A("GENESIS", href="https://www-genesis.destatis.de/genesis//online?operation=table&code=41261-0003&bypass=true&levelindex=0&levelid=1707070432276#abreadcrumb", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            "). Der Datensatz wurde um ",
                            html.A("Niederschlags- Daten", href="https://www.dwd.de/DE/leistungen/zeitreihen/zeitreihen.html#buehneTop", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            " des Deutschen Wetterdienstes (",
                            html.A("DWD", href="https://www.dwd.de/DE/Home/home_node.html", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ") erweitert. Weitere details zur genauen Prozessierung der Datensätze finden sich im ",
                            html.A("Quellcode", href="https://github.com/Neon-Purplelight/klima_kompass_navigator/blob/main/utils/dataManager.py", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ".",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_hydro_1',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_hydro_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_hydro_2_settings():
    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def make_hydro_2_info_button():
    # Info Button
    info_button_hydro_2 = dbc.Button(
        "ℹ️ Info", 
        id="info-button-hydro-2", 
        color="primary", 
        className="mr-1"
    )

    # Info Card
    info_card_hydro_2 = dbc.Card(
        dbc.CardBody(
            [
                html.P("In folgendem Dashboard wird derselbe Datensatz auf drei verschiedene Diagrammtypen visualisiert. Obwohl es sich jeweils um den exakt gleichen Datensatz handelt, legt jede der Ansichten den Betrachtungsfokus etwas anders."),
                html.Hr(),
                html.Ul([
                    html.Li("Anhand des Liniendiagramms lassen sich die zeitliche Entwicklung und Trends besonders gut ablesen."),
                    html.Li("Anhand des gestapelten Liniendiagramms lässt sich schnell ein Überblick darüber verschaffen, wie sich die Zusammensetzung der Schäden im Laufe der Zeit verändert hat."),
                    html.Li("Anhand des gestapelten Balkendiagramms können die Beiträge einzelner Schadensursachen in den jeweiligen Jahren verglichen, bzw. gut Unterschiede in deren Zusammensetzung ausgemacht werden.")
                ]),
                html.Hr(),
                html.P("Durch Anklicken der einzelnen Schadholzkategorien unterhalb der Legende, lassen sich diese entfernen, hinzufügen oder durch Doppelklick hervorheben.")
            ]
        ),
        id="info-card-hydro-2",
        style={"display": "none"},
    )

    # Statt einer Liste von Komponenten, geben Sie eine einzelne Komponente zurück, die eine Liste als children hat.
    return html.Div([info_button_hydro_2, info_card_hydro_2])

def hydro_2_line_chart(df, colors):
# Tab 1: Liniendiagramm
    return {
            'data': [
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Durchschnittsniederschlag'], 
                    mode='lines',
                    name='Durchschnittsniederschlag', 
                    line={'color': 'Blue', 'dash': 'dashdot'},
                    hovertemplate='<b>%{y:.2f} l/m²</b>',
                    yaxis='y2'
                ),
                go.Scatter(
                    x=df[df['Jahr'] >= 2020]['Jahr'], 
                    y=df[df['Jahr'] >= 2020]['Trockenheit'], 
                    mode='lines', 
                    name='Trockenheit', 
                    marker={'color': colors['Trockenheit'], 'size': 8}, 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'
                ),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Sonstige Ursachen'], 
                    mode='lines', 
                    name='Sonstige Ursachen', 
                    marker={'color': colors['Sonstige Ursachen'], 'size': 8}, 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'
                ),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Schnee/Duft'], 
                    mode='lines', 
                    name='Schnee/Duft', 
                    marker={'color': colors['Schnee/Duft'], 'size': 8}, 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'
                ),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Wind/Sturm'], 
                    mode='lines', 
                    name='Wind/Sturm', 
                    marker={'color': colors['Wind/Sturm'], 'size': 8}, 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'
                ),                
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Insekten'], 
                    mode='lines', 
                    name='Insekten', 
                    marker={'color': colors['Insekten'], 'size': 8}, 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'
                ),
            ],
        'layout': go.Layout(
            title='Schadholzeinschlag nach Einschlagsursachen',
            yaxis={'title': 'Mill. m³', 'side': 'right', 'range': [0, 60], 'tickvals': list(range(0, 61, 10))},
            yaxis2={'title': 'l/m²', 'side': 'left', 'overlaying': 'y', 'range': [0, 1000], 'tickvals': [0, 200, 400, 600, 800, 100]},
            xaxis={'title': 'Jahr', 'tickmode': 'linear', 'tick0': df['Jahr'].min(), 'dtick': 1},
            legend={'x': 0, 'y': -0.2, 'orientation': 'h', 'traceorder': 'reversed'},
            hovermode='x unified',
            hoverlabel={'namelength': -1, 'bgcolor': 'white', 'bordercolor': 'black'}
        )
    }

def hydro_2_stacked_bar_chart(df, colors):
    # Berechnung der Gesamtsumme für jedes Jahr zur Bestimmung der prozentualen Anteile
    df['Gesamt'] = df[['Trockenheit', 'Sonstige Ursachen', 'Schnee/Duft', 'Wind/Sturm', 'Insekten']].sum(axis=1)
    
    # Erstellen der Balken für das gestapelte Balkendiagramm
    bar_data = [
        go.Bar(
            x=df['Jahr'], 
            y=df[ursache].round(2), 
            name=ursache,
            marker={'color': colors[ursache]},
            hovertemplate='<b>%{y:.2f} Mill. m³ (%{text:.2f}%)</b>',
            text=(df[ursache] / df['Gesamt'] * 100).round(2)
        ) for ursache in ['Trockenheit', 'Sonstige Ursachen', 'Schnee/Duft', 'Wind/Sturm', 'Insekten']
    ]

    # Hinzufügen der Linie für den Durchschnittsniederschlag
    line_data = go.Scatter(
        x=df['Jahr'], 
        y=df['Durchschnittsniederschlag'].round(2), 
        mode='lines',
        name='Durchschnittsniederschlag', 
        line={'color': 'Blue', 'dash': 'dashdot'},
        hovertemplate='<b>%{y:.2f} l/m²</b>',
        yaxis='y2'
    )

    # Kombinieren der Daten
    data = bar_data + [line_data]

    # Anpassen der Layout-Einstellungen für das gestapelte Balkendiagramm
    layout = go.Layout(
        title='Schadholzeinschlag nach Einschlagsursachen',
        yaxis={'title': 'Mill. m³', 'side': 'right', 'range': [0, df['Gesamt'].max() * 1.1]},
        yaxis2={'title': 'l/m²', 'side': 'left', 'overlaying': 'y', 'range': [0, df['Durchschnittsniederschlag'].max() * 1.1]},
        xaxis={'title': 'Jahr', 'tickmode': 'linear', 'tick0': df['Jahr'].min(), 'dtick': 1},
        barmode='stack',
        legend={'x': 0, 'y': -0.2, 'orientation': 'h', 'traceorder': 'reversed'},
        hovermode='x unified',
        hoverlabel={'namelength': -1, 'bgcolor': 'white', 'bordercolor': 'black'}
    )

    return {'data': data, 'layout': layout}

def hydro_2_stacked_line_chart(df, colors):
# Tab 3: Gestapeltes Liniendiagramm
    return {
            'data': [
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Durchschnittsniederschlag'], 
                    mode='lines',  # Linie für den Niederschlag
                    name='Durchschnittsniederschlag', 
                    line={'color': 'Blue', 'dash': 'dashdot'},
                    hovertemplate='<b>%{y:.2f} l/m²</b>',  # Hier werden Zahlen und Einheiten im Fettdruck angezeigt
                    yaxis='y2'  # Verwenden Sie die rechte Y-Achse für den Niederschlag
                ),                
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Gesamt'], 
                    mode='lines',  # Nur eine gestrichelte Linie für 'Gesamt'
                    name='Gesamteinschlag', 
                    line={'color': 'black', 'dash': 'dot'},  # fein gestrichelte Linie
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>',  # Hier werden Zahlen und Einheiten im Fettdruck angezeigt
                    visible=True,  # Die "Gesamt"-Linie wird initial sichtbar sein
                ),
                go.Scatter(
                    x=df[df['Jahr'] >= 2020]['Jahr'],
                    y=df[df['Jahr'] >= 2020]['Trockenheit'],
                    mode='markers',
                    name='Trockenheit',
                    marker={'color': colors['Trockenheit'], 'size': 8}, 
                    #visible='legendonly', 
                    stackgroup='one', 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Sonstige Ursachen'], 
                    mode='markers', 
                    name='Sonstige Ursachen', 
                    marker={'color': colors['Sonstige Ursachen'], 'size': 8}, 
                    #visible='legendonly', 
                    stackgroup='one', 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Schnee/Duft'], 
                    mode='markers', 
                    name='Schnee/Duft', 
                    marker={'color': colors['Schnee/Duft'], 'size': 8}, 
                    #visible='legendonly', 
                    stackgroup='one', 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Wind/Sturm'], 
                    mode='markers', 
                    name='Wind/Sturm', 
                    marker={'color': colors['Wind/Sturm'], 'size': 8}, 
                    #visible='legendonly', 
                    stackgroup='one', 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'),
                go.Scatter(
                    x=df['Jahr'], 
                    y=df['Insekten'], 
                    mode='markers', 
                    name='Insekten', 
                    marker={'color': colors['Insekten'], 'size': 8}, 
                    #visible='legendonly', 
                    stackgroup='one', 
                    hovertemplate='<b>%{y:.2f} Mill. m³</b>'),
            ],
        'layout': go.Layout(
            title='Schadholzeinschlag nach Einschlagsursachen (Gestapelt)',
            yaxis={'title': 'Mill. m³', 'side': 'right', 'range': [0, 60], 'tickvals': list(range(0, 61, 10))},
            yaxis2={'title': 'l/m²', 'side': 'left', 'overlaying': 'y', 'range': [0, 1000], 'tickvals': [0, 200, 400, 600, 800, 100]},
            xaxis={'title': 'Jahr', 'tickmode': 'linear', 'tick0': df['Jahr'].min(), 'dtick': 1},
            legend={'x': 0, 'y': -0.2, 'orientation': 'h'},
            hovermode='x unified',
            hoverlabel={'namelength': -1, 'bgcolor': 'white', 'bordercolor': 'black'}
        )
    }
# ------------------------------------------------------------------------------
# pedo_1 functions
# ------------------------------------------------------------------------------
def make_pedo_1_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    # Verwenden Sie d-flex und justify-content-center, um Elemente zu zentrieren
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " Dürre Monitor"], 
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/pedo_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " Permafrostböden"], 
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/pedo_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
        brand=html.Span([link_icon, " Pedologie:"], 
        style={"text-decoration": "underline", "color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Bodenkunde",
        color="primary",
        dark=True,
        className="d-flex flex-column justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P([
                    "Der Boden spielt eine entscheidende Rolle in unserem Ökosystem, und seine Feuchtigkeit beeinflusst maßgeblich die Umwelt. Durch die Analyse von Standardized Moisture Index (",
                    html.A("SMI", href="https://journals.ametsoc.org/view/journals/hydr/14/1/jhm-d-12-075_1.xml", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    ")- Werten für Ober- und Gesamtböden in Deutschland können wir den Einfluss des Klimawandels auf Dürren besser verstehen. Der SMI ist ein Indikator, der die Bodenfeuchte im Vergleich zu historischen Werten bewertet. Niedrige SMI-Werte deuten auf Trockenheit hin, was wiederum Auswirkungen auf die Landwirtschaft, Wasserversorgung und Ökosysteme haben kann.",
                    ]),
                    html.P([
                    "Das Dashboard ermöglicht einen eingehenden historischen Vergleich von Dürren in Deutschland anhand von SMI-Werten. Frühere Jahre zeigen eine stabile Bodenfeuchte, während neuere Daten (Insbesondere seit der ",
                    html.A("Dürre 2018", href="https://de.wikipedia.org/wiki/D%C3%BCrre_und_Hitze_in_Europa_2018", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " auf eine sukzessive Austrocknung der insbesondere der Gesamtböden hindeuten. Analysen von Dürren sind von entscheidender Bedeutung, um etwaige Muster zu erkennen und künftige Herausforderungen im Zusammenhang mit dem Klimawandel vorherzusagen. Eine verbesserte Kenntnis der Dürreentwicklung kann dazu beitragen, geeignete Anpassungs- und Schutzmaßnahmen zu entwickeln.",
                    ]),                    
                    html.P([
                    "Diese Erkenntnisse verdeutlichen, dass der Klimawandel bereits messbare Auswirkungen auf die Bodenfeuchte in Deutschland hat. Im Jahr 2023 rechneten laut ",
                    html.A("agrarheute", href="https://www.agrarheute.com/pflanze/getreide/duerreschaeden-weizen-wassernot-aktuell-schlimmsten-608544", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " Experten mit regionalen Ernteeinbußen von bis zu 17 Prozent und ",
                    html.A("laut des Statistischen Bundesamtes", href="https://www.destatis.de/DE/Themen/Querschnitt/Hitze/_inhalt.html", target="_blank", style={"color": "white", "text-decoration": "underline"}),                  
                      " nutzten landwirtschaftliche Betriebe im Jahr 2019 bereits 38,4 % mehr Wasser zur Bewässerung der Anbauflächen, als noch 3 Jahre zuvor. Um dieser Herausforderung zu begegnen, ist eine nachhaltige Bewirtschaftung unserer Ressourcen unerlässlich. Dies könnte die Förderung wassersparender landwirtschaftlicher Praktiken, den Schutz natürlicher Wassereinzugsgebiete und die Entwicklung innovativer Technologien zur Wasserrückgewinnung umfassen.",
                    ]),
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_hydro_1', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                        "Die Identifikation von Dürrebedingungen in Deutschland basiert auf einem Bodenfeuchteindex (SMI), der über das hydrologische Modell ",
                        html.A("mHM", href="https://www.ufz.de/index.php?en=40114", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " berechnet wird und die Bodenfeuchteverteilung über einen 65-jährigen Zeitraum seit 1951 zeigt. Die Farben kennzeichnen hierbei die Stärke der Dürren: ",
                        ]),
                        html.P([
                            html.Li("SMI 0,20 - 0,30 = ungewöhnliche Trockenheit (Vorwarnstufe)"),
                            html.Li("SMI 0,10 - 0,20 = moderate Dürre"),
                            html.Li("SMI 0,05 - 0,10 = schwere Dürre"),
                            html.Li("SMI 0,02 - 0,05 = extreme Dürre"),
                            html.Li("SMI 0,00 - 0,02 = außergewöhnliche Dürre"),
                        ]),
                        html.P([
                            "Hierbei wird Dürre als Abweichung vom langjährigen Erwartungswert geschätzt. Erst wenn die aktuelle Bodenfeuchte unter das langjährige 20-Perzentil fällt, also den Wert, der nur in 20% der Jahre in einer langen Zeitreihe erreicht wird, spricht man von Dürre. So bedeutet also ein Wert von 0.3 (ungewöhnliche Trockenheit), dass die aktuelle Bodenfeuchte so niedrig wie in 30% der Fälle von 1951-2015 ist. Genauso bedeutet ein SMI von 0.02 (außergewöhnliche Dürre), dass der Wert nur in 2% der langjährigen Simulationswerte unterschritten wird."
                        ]),
                        html.P([
                        "Das  ",
                        html.A("Helmholtz- Zentrum für Umweltforschung", href="https://www.ufz.de/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ", hat hierzu ein informatives ",
                        html.A("Kurzvideo", href="https://www.youtube.com/watch?v=FGLs0VmM3Xc", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " veröffentlicht.",
                        ]),
                        html.H4("Verwendeter Datensatz:"),
                        html.P([
                        "Die historischen, monatlichen SMI-Daten von 1951-2022 können im  ",
                        html.A("Netcdf-Format", href="https://de.wikipedia.org/wiki/NetCDF", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " ",
                        html.A("hier ", href="https://www.ufz.de/index.php?de=37937", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " heruntergeladen werden. Die Daten basieren auf ", 
                        html.A("Zink et al. 2015 (ERL) ", href="https://www.ufz.de/export/data/2/126777_2016-Zink-Soil_Moisture_Droughts_in_Germany.pdf", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        "und enthalten den Bodenfeuchteindex (SMI, soil moisture index) skaliert zwischen [0-1], sowie Koordinaten in den Formaten Gauß-Krüger Zone 4 (EPSG: 31468) [variablen easting/northing] als auch Lat/Lon Informationen (EPSG:4326).",
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_hydro_1',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_hydro_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_pedo_1_settings():
    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def make_drought_tabs(date_values_oberboden, date_values_gesamtboden):
    # Reverse the order of date_values_gesamtboden
    reversed_date_values_gesamtboden = date_values_gesamtboden[::-1]

    # Format dates in the desired format with German month names
    formatted_dates = [date.strftime("%B %Y").replace("January", "Januar").replace("February", "Februar").replace("March", "März").replace("April", "April").replace("May", "Mai").replace("June", "Juni").replace("July", "Juli").replace("August", "August").replace("September", "September").replace("October", "Oktober").replace("November", "November").replace("December", "Dezember") for date in reversed_date_values_gesamtboden]

    return dcc.Tabs(
        style={'color': 'primary'},
        children=[
            dcc.Tab(
                label='Zeitskala',
                children=[
                    # Hier setzen Sie Ihren dcc.Slider Code ein
                    dcc.Slider(
                        id='time-slider-drought',
                        min=0,
                        max=len(date_values_oberboden) - 1,
                        step=1,
                        marks={
                            i: {
                                'label': dm.translate_month(date_values_oberboden[i]),
                                'style': {
                                    'transform': 'rotate(45deg)',
                                    'white-space': 'nowrap'
                                }
                            } for i in range(0, len(date_values_oberboden), max(1, len(date_values_oberboden)//10))
                        },
                        value=0,
                        tooltip={'placement': 'bottom', 'always_visible': True},
                        className='my-custom-slider slider slider-success',
                    ),
                    html.Div([
                        html.Div(id='plots-container-timescale'),
                    ], style={'display': 'flex'}),
                ]),

            dcc.Tab(label='Vergleich', children=[
                dcc.Dropdown(
                    id='time-dropdown-gesamtboden',
                    options=[
                        {'label': formatted_date, 'value': date} for formatted_date, date in zip(formatted_dates, reversed_date_values_gesamtboden)
                    ],
                    multi=True,
                    value=None,
                    placeholder='Wähle Datum',
                ),
                dcc.Dropdown(
                    id='data-dropdown-gesamtboden',
                    options=[
                        {'label': 'Gesamtboden', 'value': 'gesamtboden'},
                        {'label': 'Oberboden', 'value': 'oberboden'},
                    ],
                    value=None,
                    multi=True,
                    placeholder='Wähle Daten',
                ),
                html.Div([
                    html.Div(id='plots-container-gesamtboden'),
                ], style={'display': 'flex'}),
            ]),
        ],
    )

# ------------------------------------------------------------------------------
# pedo_2 functions
# ------------------------------------------------------------------------------
def make_pedo_2_sidebar():
    # Bootstrap Sidebar
    link_icon = html.I(className="fa fa-arrow-circle-right", style={'color': '#7fff00'})

    # Erstellen Sie die Sidebar mit den Links und Symbolen
    # Verwenden Sie d-flex und justify-content-center, um Elemente zu zentrieren
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([link_icon, " Dürre Monitor"], 
                                    style={"text-decoration": "underline", "color": "white"},
                                    href="/pedo_1", 
                                    id="navlink-1", 
                                    className="nav-link-custom")),
            dbc.NavItem(dbc.NavLink([link_icon, " Permafrostböden"], 
                                    style={"text-decoration": "underline", "color": "#7fff00"},
                                    href="/pedo_2", 
                                    id="navlink-2", 
                                    className="nav-link-custom")),
        ],
        brand=html.Span([link_icon, " Pedologie:"], 
        style={"text-decoration": "underline", "color": "#7fff00"}),
        brand_href="https://de.wikipedia.org/wiki/Bodenkunde",
        color="primary",
        dark=True,
        className="d-flex flex-column justify-content-center",
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P([
                    "Permafrostböden werden als Böden definiert, die mindestens zwei Jahre lang durchgehend gefroren sind. Sie bedecken etwa ein Fünftel der Erdoberfläche und sind besonders anfällig für Degradation und das Auftauen im Zuge des Klimawandels ",
                    html.A("Link", href="https://www.researchgate.net/publication/339929486_Multisensory_satellite_observations_of_the_expansion_of_the_Batagaika_crater_and_succession_of_vegetation_in_its_interior_from_1991_to_2018", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    ]),
                    html.P([
                    "Der ",
                    html.A("Batagaika-Krater", href="https://de.wikipedia.org/wiki/Batagaika-Krater", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " (von Einheimischen oft “Das Tor zur Unterwelt” genannt) ",
                    html.A("befindet sich in Sibirien", href="https://www.google.de/maps/place/Batagaika+crater/@67.5786202,134.7822196,7564m/data=!3m1!1e3!4m12!1m5!3m4!2zNjfCsDM0JzQ3LjYiTiAxMzTCsDQ2JzE3LjgiRQ!8m2!3d67.5798889!4d134.7716111!3m5!1s0x5bbfe98a616b146b:0x100d1ed2d264a68c!8m2!3d67.5783832!4d134.7728567!16s%2Fg%2F11fn4n5bg1?entry=ttu", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " und ist der größte Klimawandel- induzierte Permafrost-Krater der Welt(",
                    html.A("Videolink", href="https://www.youtube.com/watch?v=lbvTmLBrdps", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    "). Ursprünglich in den 1950er und 1960er Jahren durch Mineralerkundung und Abholzung für Brennholz ausgelöst, hat sich der Krater aufgrund warmer Sommer und kürzerer Winter in der Region rapide vergrößert. Die stetige Erderwärmung führt zum Auftauen des Permafrosts, wodurch der Boden auf den Hängen nachgibt und erodiert. Der Krater, der mittlerweile beeindruckende Ausmaße von etwa 1 km Länge, 800 m Breite, wächst jährlich um mehr als 10 Meter. Die Kraterwand des aufgetautem Permafrostbodens, die in einigen Bereichen mehr als 85 Meter hoch ist, bietet Forschern einen einzigartigen Einblick in vergangene Klimabedingungen."
                    ]),
                    html.P([
                    "Darüber hinaus hat das Phänomem jedoch auch ernsthaften Konsequenzen hinsichtlich des Klimawandels. Denn das Auftauen des Permafrosts setzt bedeutende Mengen an Treibhausgasen wie Kohlendioxid, Methan und Lachgas frei, was wiederum Rückwirkend den Klimawandel antreibt. Dieser Teufelkreis gilt zudem als einer der möglichen ",
                    html.A("Klimakipppunkte", href="https://de.wikipedia.org/wiki/Kippelemente_im_Erdklimasystem#Methan-_und_Kohlendioxidemissionen_aus_tauenden_Permafrostb%C3%B6den", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                    " und ist auch in anderen Permafrostregionen zu beobachten. Der Batagaika-Krater dient somit als eindrückliches Beispiel für die drängende Notwendigkeit, Maßnahmen zur Eindämmung des Klimawandels zu ergreifen, um solche katastrophalen Umweltauswirkungen zu minimieren."
                    ]),
                    html.P([
                    "Das Dashboard ermöglicht einen historischen Vergleich verschiedener Sattelitenaufnahmen des Batagaika- Kraters und führt vor Augen, wie der Krater Jahr für Jahr wächst",
                    ]),
                ],
                className='mb-3',
                #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_hydro_1', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                html.Div(
                    [
                        html.P([
                        "Die Beobachtung und Überwachung solcher Phänomene, insbesondere in ausgedehnten und schwer zugänglichen Regionen, stellen eine Herausforderung dar. Hierbei spielt die Fernerkundung, beispielsweise durch Satellitenbilder, eine entscheidende Rolle. Optische Satellitenbeobachtungen ermöglichen es, große Gebiete effektiv zu überwachen und Veränderungen zu kartieren. Hierfür werden multisensorische Satellitenbilder verwendet, die von verschiedenen Institutionen wie dem United States Geological Survey (",
                        html.A("USGS", href="https://www.usgs.gov/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ") auch der Öffentlichkeit frei zugänglich gemacht werden."
                        ]),
                        html.P([
                        "Die Nutzung solcher Satellitendaten bringt jedoch auch eigene Herausforderungen mit sich, die eine kontinuierliche Beobachtung erschweren können. Optische Sensoraufnahmen können beispielsweise nur an wolkenfreien Tagen erfolgen, und die Qualität der Aufnahmen kann durch unterschiedliche Beleuchtungsverhältnisse, Wetterbedingungen oder jahreszeitliche Unterschiede beeinflusst werden. Darüber hinaus können Fehler bei der Datenübertragung, Verarbeitung oder anderen technischen Aspekten auftreten. Ein Beispiel für solche technischen Fehler sind die Aufnahmen von 2005 und 2010. Die Artefakte (Bildstörungen) auf diesen beiden Aufnahmen resultieren aus einer Hardware-Fehlfunktion des Landsat 7 Satelliten, wodurch die Vorwärtsbewegung des Satelliten auf seiner Umlaufbahn nicht korrekt ausgeglichen wurde (",
                        html.A("Link", href="https://www.usgs.gov/faqs/what-landsat-7-etm-slc-data", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ")."
                        ]),
                        html.H4("Verwendete Daten:"),
                        html.P([
                        "Die hier verwendeten Satellitendaten stammen aus einer vorab ausgewählten Sammlung des US Geological Survey (USGS) (",
                        html.A("Link", href="https://eros.usgs.gov/earthshots/the-craters-size", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        ") und sind Teil der Satellitenmissionen ",
                        html.A("Landsat 5", href="https://de.wikipedia.org/wiki/Landsat_5", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " (1991), ", 
                        html.A("Landsat 7", href="https://de.wikipedia.org/wiki/Landsat_7", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " (1999, 2005, 2010), ",
                        html.A("Landsat 8", href="https://de.wikipedia.org/wiki/Landsat_8", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " (2014, 2018, 2022) sowie ",
                        html.A("Sentinel-2A", href="https://de.wikipedia.org/wiki/Sentinel-2", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                        " (2022)."
                        ]),
                    ],
                    className='mb-3',
                    #style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
                ),
                id='collapse_more_info_hydro_1',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_hydro_1', className='ms-1')
        ],
        fluid=True,
        className="py-1 bg-primary rounded-1 text-white",
    )

    # Combine the sidebar, second row, and the new settings row
    layout = dbc.Container([sidebar, second_row])

    return layout

def make_pedo_2_settings():
    plot_cards = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Einstellungen:", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem'}),
                ],
                color="primary",
            ),
        ]
    )

    return plot_cards

def generate_initial_image_overlay(dataFolder, satellite_data):
    # Pfad zum ersten Bild aus 'satellite_data'
    first_image_path = os.path.join(dataFolder, satellite_data[0]['value'])
    with open(first_image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    # HTML-Struktur mit Bild und Overlay-Play-Symbol
    initial_image_html = html.Div([
        html.Img(src=f"data:image/png;base64,{encoded_image}", style={'width': '80%', 'height': '80vh'}),
        html.Div(html.I(className="fas fa-play-circle", style={'font-size': '4em', 'color': '#007bff', 'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'}), style={'position': 'relative', 'text-align': 'center'}),
    ], style={'position': 'relative', 'text-align': 'center'})
    return initial_image_html

def create_tabs_layout(satellite_data):
    return dcc.Tabs([
        dcc.Tab(label='Zeitraffer', children=[
            html.Div([
                # Play, Stopp und Vorwärts-Buttons über dem Iframe
                dbc.Row([
                    dbc.Col(
                        dbc.Button('Play', id='play-button', n_clicks=0, color='primary', className='mr-2'),
                        width='auto'
                    ),
                    dbc.Col(
                        dbc.Button('Stopp', id='stop-button', n_clicks=0, color='primary', className='mr-2'),
                        width='auto'
                    ),
                    dbc.Col(
                        dbc.Button('Vorwärts', id='next-button', n_clicks=0, color='primary'),
                        width='auto'
                    ),
                ], justify='center', className='mb-3'),
                # Iframe für die Anzeige des Bildes
                html.Iframe(id='image-display', style={'width': '80%', 'height': '80vh', 'border': 'none'}),
                # Intervall für die Play-Funktion
                dcc.Interval(id='play-interval', interval=500, n_intervals=0, disabled=True),
            ], style={'text-align': 'center'}),
        ]),

        dcc.Tab(label='Vergleich', children=[
            dbc.Container([
                dbc.Row(
                    dbc.Col(html.H1("Vorher- Nachher Vergleich", style={'textAlign': 'center'}), width=12)
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.H2("Aufnahme für Vorher-Vergleich auswählen"),
                        dcc.RadioItems(
                            id='before-radio',
                            options=[
                                {'label': data['label'], 'value': data['value']} for data in satellite_data
                            ],
                            value=satellite_data[0]['value'],  # Annahme, dass das erste Element als Standardwert gesetzt wird
                            labelStyle={'display': 'block'},
                        ),
                    ], width=3),
                    dbc.Col([
                        # Hier wird angenommen, dass 'BeforeAfter' ein benutzerdefiniertes Dash-Component ist
                        html.Div(id='image-slider', style={'width': '612px', 'height': '512px'}),
                    ], width=6),
                    dbc.Col([
                        html.H2("Aufnahme für Nachher-vergleich auswählen"),
                        dcc.RadioItems(
                            id='after-radio',
                            options=[
                                {'label': data['label'], 'value': data['value']} for data in satellite_data
                            ],
                            value=satellite_data[-1]['value'],  # Annahme, dass das letzte Element als Standardwert gesetzt wird
                            labelStyle={'display': 'block'},
                        ),
                    ], width=3),
                ]),
            ]),
        ]),
    ])