from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime as dt
from dash import html, dcc

dataframe = pd.read_excel("banco de dados.xlsx", sheet_name="Banco de Dados")
dataframe = dataframe.dropna(axis=1, how='all')
dataframe['Movimentação'] = dataframe['Depósito']-dataframe['Retiradas']
ultimo_mes = dataframe['Data'].max()

df_1 = dataframe.sort_values(by=['Investimento', 'Data'])

df_1['Acumulado 12 Meses'] = df_1.groupby('Investimento')['Rendimento']\
    .rolling(window=12, min_periods=1).apply(lambda x: (1 + x).prod() - 1, raw=True)\
    .reset_index(level=0, drop=True)

df_1['Acumulado 12 Meses'] = df_1.groupby('Investimento')['Acumulado 12 Meses'].shift(1)

df_acumulado = df_1[df_1['Data'] == ultimo_mes]
df_acumulado = df_acumulado.sort_values(by=['Acumulado 12 Meses'], ascending=[False])
df_12meses = df_acumulado[['Banco', 'Investimento', 'Acumulado 12 Meses']]

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
                             dash_table.DataTable(
                                 id='Tabela1',
                                 columns=[
                                     {'name': 'Banco', 'id': 'Banco'},
                                     {'name': 'Investimento', 'id': 'Investimento'},
                                     {"name": "Acumulado 12 Meses", "id": "Acumulado 12 Meses",
                                      "type": "numeric", "format": {"specifier": ".2%"}}
                                 ],
                                 data=df_12meses.to_dict('records'),
                                 style_table={'overflowX': 'auto', 'overflowY': 'auto', 'textAlign': 'left'},
                                 style_cell={
                                     'textAlign': 'left',  # Alinhamento do texto
                                     'padding': '10px',  # Espaçamento interno
                                     'color': 'white',  # Cor da fonte
                                     'fontFamily': 'Candal',  # Fonte do texto
                                     'fontSize': '14px',  # Tamanho da fonte
                                     'textAlign': 'center',
                                     'backgroundColor': 'Transparent'
                                 },
                                 style_header={'backgroundColor': 'Transparent',
                                               'fontWeight': 'bold',
                                               'textAlign': 'center',
                                               'color': 'white'},
                                 style_as_list_view=True
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
                    children=[dbc.CardHeader('', className='paragrafo-personalizado'),
                              dbc.CardBody()
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )], width=6, lg=3),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader('', className='paragrafo-personalizado'),
                              dbc.CardBody()
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )], width=6, lg=3),
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
                                    dcc.Graph(

                                    )
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
