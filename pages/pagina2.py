from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from dash import html, dcc
import data

df_1 = data.df_1.copy()  # Se precisar modificar o DataFrame sem afetar os outros
ultimo_mes = df_1['Data'].max()
dropdown_options = list(df_1['Investimento'].unique())

df_acumulado = data.df_3[data.df_3['Data'] == ultimo_mes].copy()
df_acumulado = df_acumulado.sort_values(by=['Acumulado 12 Meses'], ascending=False)
df_12meses = df_acumulado[['Banco', 'Investimento', 'Acumulado 12 Meses']].copy()  # Criando cópia

df_12meses['Acumulado 12 Meses'] = df_12meses['Acumulado 12 Meses'].apply(lambda x: f'{x:.2%}')

fig=go.Figure()


layout = dbc.Container(
    fluid=True,  # Ocupa toda a largura disponível
    style={
        'overflowX': 'auto',  # Habilita a barra de rolagem horizontal
        'width': '100%',  # Largura total
        'padding': '20px',  # Espaçamento interno
    },
    children=[dbc.Row(
        children=[dbc.Col(
            children=[dbc.Card(
                children=[dbc.CardHeader('Rendimento acumulado em 12 Meses', className='paragrafo-personalizado'),
                          dbc.CardBody(
                              html.Div(
                                  dbc.Table(
                                      id='Tabela1',
                                      children=[
                                          html.Thead(  # Cabeçalho da tabela
                                              html.Tr([html.Th(col, className='intra-header')
                                                       for col in df_12meses.columns])
                                          ),
                                          html.Tbody(  # Corpo da tabela
                                              [html.Tr([html.Td(df_12meses.iloc[i][col], className='intra-tabela')
                                                        for col in df_12meses.columns]) for i in range(len(df_12meses))]
                                          )
                                      ],
                                      bordered=False,  # Adiciona bordas à tabela
                                      hover=True,     # Habilita o efeito de hover
                                      responsive=True,  # Torna a tabela responsiva
                                      striped=False,   # Adiciona listras às linhas
                                      style={'background-color': 'transparent', 'font-family': 'Candal', 'color': 'black'}
                                      ), className='custom-table'
                              )
                          )
                          ],
                color="transparent",  # Cor de fundo
                inverse=True,  # Texto branco
                outline=False,  # Sem borda
                style={
                    'max-height': '50vh',  # Define a altura máxima do card
                    'overflow': 'auto',

                }
            )], width=9, lg=4, md=4, sm=9),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader(
                        dbc.Row(
                            [
                                dbc.Col("Análise de rendimento", width="auto", className="my-auto"),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="entrada-investimentos",
                                        options=dropdown_options,
                                        placeholder="Selecione",
                                        className='dropdown-transparente'
                                    ),
                                    width="auto",
                                ),
                            ],
                            align="center",  # Alinha os itens verticalmente ao centro
                            justify="between",  # Distribui o espaço entre os itens
                            className="w-95",  # Faz a linha ocupar 100% da largura
                        ),
                        className="d-flex align-items-center",  # Alinha o conteúdo do CardHeader verticalmente ao centro
                    ),
                        dbc.CardBody(
                                    dcc.Graph(id='grafico1', figure=fig,
                                              style={"margin-top": "0", 'width': '100%', 'height': '42vh',
                                                     'background-color': 'transparent'}),
                                    style={'background-color': 'transparent'}
                                )

                    ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                    style={
                        'max-height': '50vh',  # Define a altura máxima do card
                    }
                )], width=15, lg=8, md=8, sm=15),
        ], style={"margin-bottom": "20px"}  # Adiciona margem abaixo da linha
    ),
        dbc.Row(children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader('', className='paragrafo-personalizado'),
                        dbc.CardBody(
                            children=[
                                dbc.Col(

                                )
                            ], className="card-body-left"
                        )
                    ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                ), width=12, lg=6, md=6, sm=12
            ),
            dbc.Col(
                    dbc.Card(
                        children=[
                            dbc.CardHeader('', className='paragrafo-personalizado'),
                            dbc.CardBody(
                                children=[
                                    dbc.Col(

                                    )
                                ]
                            )
                        ],
                        color="transparent",  # Cor de fundo
                        inverse=True,  # Texto branco
                        outline=False,  # Sem borda
                    ), width=6, lg=3, md=3, sm=6
            ),
            dbc.Col(
                dbc.Card(
                        children=[
                            dbc.CardHeader('', className='paragrafo-personalizado'),
                            dbc.CardBody(
                                children=[
                                    dbc.Col(
                                            )
                                ]
                            )
                        ],
                        color="transparent",  # Cor de fundo
                        inverse=True,  # Texto branco
                        outline=False,  # Sem borda
                    ), width=6, lg=3, md=3, sm=6),
             ]),
        ],

)


@callback(
    Output('grafico1', 'figure'),
    Input('entrada-investimentos', 'value')
)
def update_output(value):
    if value == None:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Data"),
            yaxis=dict(
                title='Rendimento (%)',
                titlefont=dict(color='white'),
                tickfont=dict(color='white'),
                tickformat='0.00%',
                showgrid=False,
                zeroline=False
            ),
            yaxis2=dict(
                title='saldo e movimentação',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            legend=dict(x=0.1, y=1.2),
            margin=dict(l=50, r=50, t=80, b=50)  # Ajuste das margens
        )
    else:
        tabela_filtrada = data.carregar_dados_filtrados(value)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tabela_filtrada['Data'],
            y=tabela_filtrada['Rendimento'],
            name='Crescimento',
            mode='lines',
            line=dict(color='#e87722', width=2),
            yaxis='y1'
        ))
        fig.add_trace(go.Bar(
            x=tabela_filtrada['Data'],
            y=tabela_filtrada['Movimentação'],
            name='Movimentação',  # Nome da série na legenda
            marker_color='blue', # Cor das barras
            yaxis='y2'
        ))
        fig.add_trace(go.Bar(
            x=tabela_filtrada['Data'],
            y=tabela_filtrada['Saldo'],
            name='Saldo',  # Nome da série na legenda
            marker_color='purple',  # Cor das barras
            yaxis = 'y2'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',  # Fundo da área de plotagem transparente
            title=f'Evolução de {value}',
            xaxis=dict(title="Data"),
            yaxis=dict(
                title='Rendimento (%)',
                titlefont=dict(color='white'),
                tickfont=dict(color='white'),
                tickformat='0.00%',
                showgrid=False,
                zeroline=False
            ),
            yaxis2=dict(
                title='saldo e movimentação',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            legend=dict(x=0.1, y=1.2),
            margin=dict(l=50, r=50, t=90, b=50)  # Ajuste das margens
        )
    return fig