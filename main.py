import dash
from dash import dcc, html, Input, Output, State
from pages import inicio, pagina2
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    fluid=True,
    children=[
        dcc.Location(id='url', refresh=False),  # Componente para gerenciar a URL
        dbc.Row(
            dbc.Col(
               children=[
                    html.Button(
                        html.Span('☰'),
                        id='menu-button',
                        style={'fontSize': '24px', 'border': 'none', 'background': 'none', 'cursor': 'pointer'}
                    ),
                    html.H1('Dashboard de Investimentos', className='titulo-personalizado')
               ], style={'position': 'aboslute', 'top': '10', 'left': '0', 'width': '100%',
                         'backgroundColor': 'transparent', 'padding': '10px', 'zIndex': '1000'}
            ),
        ),
        dbc.Offcanvas(
            children=[
                dcc.Link('Home', href='/', style={'display': 'block', 'padding': '10px',
                                                  'textDecoration': 'none', 'color': '#333'}),
                dcc.Link('Investimentos', href='/pagina2', style={'display': 'block', 'padding': '10px',
                                                               'textDecoration': 'none', 'color': '#333'}),
                dcc.Link('', href='/pagina3', style={'display': 'block', 'padding': '10px',
                                                             'textDecoration': 'none', 'color': '#333'})
            ],
            id="menu-column",
            is_open=False,  # Menu inicialmente fechado
            placement="start",  # Menu aparece à esquerda
            style={'width': '250px', 'backgroundColor': '#f8f9fa'}
        ),
        html.Div(id='page-content', style={'marginTop': '10px'})
    ]
)


# Callback para abrir/fechar o menu
@app.callback(
    dash.dependencies.Output("menu-column", "is_open"),
    [dash.dependencies.Input("menu-button", "n_clicks")],
    [dash.dependencies.State("menu-column", "is_open")],
)
def toggle_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_pages(pathname):
    if pathname == '/':
        return inicio.layout
    elif pathname == '/pagina2':
        return pagina2.layout

    else:
        return '404 - Página não encontrada'


if __name__ == '__main__':
    app.run_server(debug=True)
