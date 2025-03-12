from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import funcoes as fc
import datetime as dt
import data


df_1 = data.df_1
df_2 = data.df_2
Saldo = data.Saldo
data = dt.datetime(2024, 1, 3)
nova_data = fc.mes_anterior(data)

ultimo_dado = df_1['Data'].iloc[-1]
Saldo = df_2['Saldo'].iloc[-1]

df_ultimo_mes = df_1[df_1['Data'] == ultimo_dado]
movimentacao_total = df_ultimo_mes['Movimentação'].sum()

valores = (df_2['Rendimento'].values)
inflacao = (df_2['Inflação'].values)

resultado = [valores[0] + 1]
resultado_12_meses = df_2['Rendimento'].iloc[-1]+1

resultado_inflacao = [inflacao[0]+1]
resultado_inflacao_12_meses = df_2['Inflação'].iloc[-1]+1

for i in range(1, len(valores)):
    resultado.append(resultado[i-1] * (valores[i]+1))
    resultado_inflacao.append(resultado_inflacao[i-1]*(inflacao[i]+1))
for i in range(1, 11):
    resultado_12_meses = resultado_12_meses * (valores[-i-1] + 1)
    resultado_inflacao_12_meses = (resultado_inflacao_12_meses * (inflacao[-i-1] + 1))

df_2['Evolução'] = [r - 1 for r in resultado]
df_2['Inflação global'] = [p - 1 for p in resultado_inflacao]
resultado_12_meses = resultado_12_meses-1
resultado_inflacao_12_meses = resultado_inflacao_12_meses-1

df_bancos = df_ultimo_mes.groupby("Banco")['Saldo'].sum().reset_index()
df_risco = df_ultimo_mes.groupby("Risco")['Saldo'].sum().reset_index()

grafico_evolucao = go.Figure()
grafico_evolucao.add_trace(go.Bar(
            x=df_2['Data'],
            y=df_2['Saldo'],
            name='Saldo',  # Nome da série na legenda
            marker_color='blue',  # Cor das barras
            yaxis='y1'
        ))
grafico_evolucao.add_trace(go.Scatter(
            x=df_2['Data'],
            y=df_2['Evolução'],
            name='Evolução',
            mode='lines',
            line=dict(color='#e87722', width=2),
            yaxis='y2'
        ))
grafico_evolucao.add_trace(go.Scatter(
            x=df_2['Data'],
            y=df_2['Inflação global'],
            name='Inflação Acumulada',
            mode='lines',
            line=dict(color='#058549', width=2),
            yaxis='y2'
        ))
grafico_evolucao.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',   # Fundo da área de plotagem transparente
            margin=dict(
                l=50,  # Margem esquerda
                r=50,  # Margem direita
                t=0,  # Margem superior
                b=50  # Margem inferior
            ),
            yaxis=dict(
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue'),
                tickformat='0.0f',
                tickprefix='R$',
                showgrid=False,
                zeroline=True
            ),
            yaxis2=dict(
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                tickformat='0.0%',
                overlaying='y',
                side='right',
                showgrid=False,
                zeroline=False
            ),
            legend=dict(x=0.1, y=1.1)
)

grafico_bancos = go.Figure()
grafico_bancos.add_pie(
    labels=df_bancos['Banco'],
    values=df_bancos['Saldo'],
    hole=0.5,
    textinfo='label+percent',
    insidetextorientation='radial'
)
grafico_bancos.update_layout(
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(
        l=0,  # Margem esquerda
        r=0,  # Margem direita
        t=0,  # Margem superior
        b=50  # Margem inferior
    ),
)

grafico_risco = go.Figure()
grafico_risco.add_pie(
    labels=df_risco['Risco'],
    values=df_risco['Saldo'],
    hole=0.5,
    textinfo='label+percent',
    insidetextorientation='radial'
)
grafico_risco.update_layout(
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(
        l=0,  # Margem esquerda
        r=0,  # Margem direita
        t=0,  # Margem superior
        b=50  # Margem inferior
    ),
)

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
                children=[dbc.CardHeader('Inflação em 12 meses', className='paragrafo-personalizado'),
                          dbc.CardBody(html.H4(f"R$ {resultado_inflacao_12_meses:.2%}",
                                               className='valor-personalizado'),
                                       className="d-flex justify-content-center")
                          ],
                color="transparent",  # Cor de fundo
                inverse=True,  # Texto branco
                outline=False,  # Sem borda
            )], width=6, lg=3),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader('Rendimento em 12 meses', className='paragrafo-personalizado'),
                              dbc.CardBody(html.H4(f"{resultado_12_meses:.2%}",
                                                   className='valor-personalizado'),
                                           className="d-flex justify-content-center")
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )], width=6, lg=3),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader('Último aporte', className='paragrafo-personalizado'),
                              dbc.CardBody(html.H4(f"R$ {movimentacao_total:.2f}",
                                                   className='valor-personalizado'),
                                           className="d-flex justify-content-center")
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )], width=6, lg=3),
            dbc.Col(children=[dbc.Card(
                children=[dbc.CardHeader('Saldo dos Investimentos', className='paragrafo-personalizado'),
                          dbc.CardBody(html.H4(f"R$ {Saldo:.2f}", className='valor-personalizado'),
                                       className="d-flex justify-content-center")
                          ],
                color="transparent",  # Cor de fundo
                inverse=True,  # Texto branco
                outline=False,  # Sem borda
            )], width=6, lg=3)
        ], style={"margin-bottom": "20px"}  # Adiciona margem abaixo da linha
    ),
        dbc.Row(children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader('Evolução dos Investimentos', className='paragrafo-personalizado'),
                        dbc.CardBody(
                            children=[
                                dbc.Col(
                                    dcc.Graph(id='grafico1', figure=grafico_evolucao,
                                              style={"margin-top": "0", 'width': '100%', 'height': '42vh'})
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
                            dbc.CardHeader('Bancos', className='paragrafo-personalizado'),
                            dbc.CardBody(
                                children=[
                                    dbc.Col(dcc.Graph(id='grafico2', figure=grafico_bancos, style={'height': '42vh'})
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
                            dbc.CardHeader('Risco', className='paragrafo-personalizado'),
                            dbc.CardBody(
                                children=[
                                    dbc.Col(dcc.Graph(id='grafico3', figure=grafico_risco, style={'height': '42vh'})
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
