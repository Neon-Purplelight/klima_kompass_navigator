from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import numpy as np
import os

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
            dbc.NavItem(dbc.NavLink('Home', href='/', id='navlink')),
            dbc.NavItem(dbc.NavLink('Klimatologie', href='/klima_1', id='navlink')),
            dbc.NavItem(dbc.NavLink('Hydrologie', href='/hydro_1', id='navlink')),
            dbc.NavItem(dbc.NavLink('Pedologie', href='/pedo_1', id='navlink')),
            dbc.NavItem(dbc.NavLink('Ökologie', href='/oeko_1', id='navlink')),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem('Lorem', id='citeDropdown'),
                    dbc.DropdownMenuItem('Ipsum', id='aboutUsDropdown'),
                ],
                nav=True,
                in_navbar=True,
                label='More',
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

def make_CC_licenseBanner():
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
# start_page functions
# ------------------------------------------------------------------------------
def make_start_page_sidebar():
    # Bootstrap Sidebar
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Unterseite 1", href="/", id="navlink")),
            dbc.NavItem(dbc.NavLink("Unterseite 2", href="/", id="navlink")),
        ],
        brand=html.Span("Start:", style={"text-decoration": "underline"}),
        brand_href="",
        color="primary",
        dark=True,
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
                    html.P("Die Diskussionen über den Klimawandel sind von Emotionen, politischen und wirtschaftlichen Motivationen sowie persönlichen Vorurteilen geprägt. Um einen Beitrag zur Diskussion liefern zu können ist es daher wichtig, die Datengrundlage sowie die Methodik zur Erstellung von Infografiken so transparent und klar wie möglich darzulegen [...]"),
                    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),
                ],
                className='mb-3',
                style={'max-width': '600px'}
            ),

            html.Div(
                [
                    html.H4("Weitere Informationen", id='more_info_button_start_page', className="fa-solid fa-book-open ms-3 mt-1 primary", n_clicks=0),
                ],
            ),

            dbc.Collapse(
                [
                    html.Div(
                        [
                            html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),
                        ],
                        className='mb-3',
                        style={'max-width': '600px'}
                    ),
                    html.Hr(),
                    html.H4("Verwendete Datensätze:"),
                    html.P([
                        "Die hier verwendeten Datensätze wurden z.T. weiter prozessiert. Wie genau, können Sie im ",
                        html.A("Quellcode", href="https://github.com/Neon-Purplelight/klima_kompass_navigator", target="_blank", style={"color": "white"}),
                        " einsehen."
                    ]),
                ],
                id='collapse_more_info_start_page',
                is_open=False,
            ),
            dbc.Tooltip("Weitere Infos.", target='more_info_button_start_page', className='ms-1')
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
                html.P(["Die ",
                        html.A("MCC Carbon Clock", href="https://www.mcc-berlin.net/en/research/co2-budget.html"),
                        " zeigt, wie viel CO2 in die Atmosphäre freigesetzt werden kann, um die globale Erwärmung auf maximal 1,5 °C bzw. 2 °C zu begrenzen. Mit nur einem Klick können Sie die Schätzungen für beide Temperaturziele vergleichen und sehen, wie viel Zeit in jedem Szenario noch bleibt."
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

# ------------------------------------------------------------------------------
# klima_1 functions
# ------------------------------------------------------------------------------
def make_klima_1_sidebar():
    # Bootstrap Sidebar
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("CO2 und das Klima", href="/klima_1", id="navlink")),
            dbc.NavItem(dbc.NavLink("CO2 Emittenten", href="/klima_2", id="navlink")),
            # dbc.NavItem(dbc.NavLink("Sektorenbetrachtung", href="/klima_3", id="navlink")),
        ],
        brand=html.Span("Klimatologie:", style={"text-decoration": "underline"}),
        brand_href="https://de.wikipedia.org/wiki/Klimatologie",
        color="primary",
        dark=True,
    )

    # Second row with sample text and collapse component
    second_row = dbc.Container(
        [
            html.Div(
                [
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
                ],
                className='mb-3',
                style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
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
                            " (Datensatz wird fortlaufend aktualisiert).",
                        ]),

                        html.P([  
                            "Die Temperaturdaten stammen von der National Aeronautics and Space Administration (",
                            html.A("NASA", href="https://www.nasa.gov/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ") und stellen eine Schätzung der globalen Veränderung der Oberflächentemperatur dar. Weitere Informationen zum Datensatz finden sich ",
                            html.A("hier", href="https://data.giss.nasa.gov/gistemp/", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ".",
                        ]),
                    ],
                    className='mb-3',
                    style={'max-width': '600px'}  # Adjust the max-width to control the length of the div
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

def make_klima_1_settings(default_value='average_temp', options=None):
    # Klima_1 settings
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
                    "ein spezielles Diagramm nutzen, das zwei vertikale Achsen hat, aber dieselbe Zeit auf der horizontalen Achse. Leider kann dies nicht direkt mit einer bestimmten Software umgesetzt werden, ",
                    "aber wir können auf eine etwas fortgeschrittenere Methode zurückgreifen."
                ]),
                html.Hr(),
                html.P([
                    "Auf diesem Diagramm siehst du, dass auf der linken Seite die Temperaturentwicklung und auf der rechten Seite die CO₂-Emissionen abgebildet sind. ",
                    "Das Streudiagramm der CO₂-Emissionen erscheint vielleicht seltsam, aber es dient dazu, den Zusammenhang zwischen den Daten zu verdeutlichen. ",
                    "Für ein allgemeines Publikum könnte jedoch diese Darstellung helfen, die Verbindung zwischen steigenden CO₂-Emissionen und Temperaturveränderungen besser zu verstehen."
                ]),
                html.Hr(),
                html.P([
                    "Wir können den wissenschaftlichen Konsens akzeptieren, dass CO₂-Emissionen die globale Erwärmung verstärken, müssen jedoch gleichzeitig anerkennen, ",
                    "dass auch andere Faktoren eine Rolle spielen. Temperaturveränderungen sind nicht allein darauf zurückzuführen, dass Menschen Treibhausgase in die Atmosphäre pumpen. ",
                    "Wie die ",
                    html.A("Umweltschutzbehörde der Vereinigten Staaten (EPA)", href="https://www.epa.gov/climatechange-science/causes-climate-change"),
                    " klarstellt, gibt es auch andere Faktoren wie solare Aktivität und Veränderungen in der ",
                    "Reflektivität der Erde aufgrund von beispielsweise Entwaldung. Es gibt auch Treibhausgase neben Kohlendioxid, wie Methan und Lachgas. Die EPA stellt auch klar, ",
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

# ------------------------------------------------------------------------------
# klima_2 functions
# ------------------------------------------------------------------------------
def make_klima_2_sidebar():
    # Bootstrap Sidebar
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("CO2 und das Klima", href="/klima_1", id="navlink")),
            dbc.NavItem(dbc.NavLink("CO2 Emittenten", href="/klima_2", id="navlink")),
            # dbc.NavItem(dbc.NavLink("Sektorenbetrachtung", href="/klima_3", id="navlink")),
        ],
        brand=html.Span("Klimatologie:", style={"text-decoration": "underline"}),
        brand_href="https://de.wikipedia.org/wiki/Klimatologie",
        color="primary",
        dark=True,
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
                style={'max-width': '600px'}
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
                            " (Datensatz wird fortlaufend aktualisiert).",
                        ]),

                        html.P([  
                            "Der umfangreiche Owid Datensatz wurde nur teilweise übernommen, umstrukturiert und um einige Datenpunkte ergänzt (",
                            html.A("link", href="https://github.com/owid/owid-datasets/tree/master/datasets/Countries%20Continents", target="_blank", style={"color": "white", "text-decoration": "underline"}),
                            ") (Stand: 2015)."
                        ]),
                    ],
                    className='mb-3',
                    style={'max-width': '600px'}
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

def make_klima_2_settings(default_value='co2_emissions_per_country', options=None):
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
# hydro_1 functions
# ------------------------------------------------------------------------------
def make_hydro_1_settings(default_value='months', options=None):
    if options is None:
        options = [
            {'label': 'Veränderungen des arktischen Eisschildes Innerhalb eines Jahres', 'value': 'months'},
            {'label': 'Veränderungen des arktischen Eisschildes Innerhalb mehrerer Jahre', 'value': 'years'},
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

        // Set max bounds to restrict panning
        map.setMaxBounds(boundingBox);
        map.on('drag', function () {{
            map.panInsideBounds(boundingBox, {{ animate: false }});
        }});

        // Add a tile layer (Esri World Imagery in this case)
        {esri_imagery_layer}
    """

    # Add GeoJSON layers for the selected months
    for selected_month in selected_months:
        # Find the corresponding filename from available_months
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
    output_file = os.path.join('data', 'originalData', 'map_with_selected_months.html')

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

        // Set max bounds to restrict panning
        map.setMaxBounds(boundingBox);
        map.on('drag', function () {{
            map.panInsideBounds(boundingBox, {{ animate: false }});
        }});

        // Add a tile layer (Esri World Imagery in this case)
        {esri_imagery_layer}
    """

    # Add GeoJSON layers for the selected months
    for selected_year in selected_years:
        # Find the corresponding filename from available_months
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
    output_file = os.path.join('data', 'originalData', 'map_with_selected_years.html')

    # Save the HTML content to a file
    with open(output_file, 'w') as file:
        file.write(html_content)