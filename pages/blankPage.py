from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------
# Layout for the 404 page
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Page not found :(", className='text-center'),
            
            # Card displaying a 404 image
            dbc.Card([
                dbc.CardImg(
                    src="assets/image404.png",
                    top=True,
                    style={"opacity": 0.8},
                )
            ]),
        ], width={'size': 4, 'offset': 4}
        )
    ], className='my-5'),

    # Row containing a button to go back
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button("Go Back!", id='btn_backToWfa', size='lg', color='primary')
            ], className='d-grid gap-2 col-6 mx-auto'
            )
        ], width={'size': 8, 'offset': 2})
    ], className='my-5')
])

# ...
# Callbacks
# ...

# Callback to handle the "Go Back" button click and redirect to the root URL
@callback(
    Output(component_id='url', component_property='pathname'),
    Input(component_id='btn_backToWfa', component_property='n_clicks'),
    prevent_initial_call=True
)
def redirect_to_root(_):
    return '/'
