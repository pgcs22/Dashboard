from dash import html, dcc, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import funcoes as fc
import datetime as dt


df_1 = pd.read_excel("banco de dados.xlsx", sheet_name="Banco de Dados")
df_1['Movimentação']= df_1['Depósito'] - df_1['Retiradas']
df_2 = pd.read_excel("banco de dados.xlsx")
data = dt.datetime(2024, 1, 3)
nova_data = fc.mes_anterior(data)



ultimo_dado = df_2['Mês'].iloc[-1]
Saldo = df_2['Saldo'].iloc[-1]

df_ultimo_mes = df_1[df_1['Data'] == ultimo_dado]
movimentacao_total = df_ultimo_mes['Movimentação'].sum()

valores = (df_2['Rendimento'].values)

resultado = [valores[0] + 1]
resultado_12_meses = df_2['Rendimento'].iloc[-1]+1

for i in range(1, len(valores)):
    resultado.append(resultado[i-1] * (valores[i]+1))
for i in range(1, 11):
    resultado_12_meses = resultado_12_meses * (valores[-i-1] + 1)

df_2['Evolução'] = [r - 1 for r in resultado]
resultado_12_meses = resultado_12_meses-1


grafico_evolucao = go.Figure()
grafico_evolucao.add_trace(go.Bar(
            x=df_2['Mês'],
            y=df_2['Saldo'],
            name='Saldo',  # Nome da série na legenda
            marker_color='blue', # Cor das barras
            yaxis='y2'
        ))
grafico_evolucao.add_trace(go.Scatter(
            x=df_2['Mês'],
            y=df_2['Evolução'],
            name='Evolução',
            mode='lines',
            line=dict(color='#e87722', width=2),
            yaxis='y1'
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
                tickformat='0.00%',
                showgrid=False,
                zeroline=False
            ),
            yaxis2=dict(
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',
                side='right',
                showgrid=False,

            ),
            legend=dict(x=0.1, y=1.1)
)

layout = dbc.Container(
    children=[dbc.Row(
        children=[dbc.Col(
            children=[dbc.Card(
                children=[dbc.CardHeader('Saldo dos Investimentos', className='paragrafo-personalizado'),
                          dbc.CardBody(html.H4(f"R$ {Saldo:.2f}", className='valor-personalizado'), className="d-flex justify-content-center")
                          ],
                color="transparent",  # Cor de fundo
                inverse=True,  # Texto branco
                outline=False,  # Sem borda
            )],width=6, lg=3),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader('Rendimento em 12 meses', className='paragrafo-personalizado'),
                              dbc.CardBody(html.H4(f"{resultado_12_meses:.2%}", className='valor-personalizado'), className="d-flex justify-content-center")
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )],width=6, lg=3),
            dbc.Col(
                children=[dbc.Card(
                    children=[dbc.CardHeader('Último aporte', className='paragrafo-personalizado'),
                              dbc.CardBody(html.H4(f"R$ {movimentacao_total:.2f}", className='valor-personalizado'), className="d-flex justify-content-center")
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )],width=6, lg=3),
            dbc.Col(children=[dbc.Card(
                    children=[dbc.CardHeader('Total aportado', className='paragrafo-personalizado'),
                              dbc.CardBody(html.H4(f"R$ {df_1['Movimentação'].sum():.2f}", className='valor-personalizado'), className="d-flex justify-content-center")
                              ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )],width=6, lg=3)
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
                                    dcc.Graph(id='grafico1', figure=grafico_evolucao, style={"margin-top": "0", 'width': '42.25vw', 'height': '45vh'}),
                                    width=6, lg=3
                                )
                            ], style={"padding": "0"}
                        )
                    ],
                    color="transparent",  # Cor de fundo
                    inverse=True,  # Texto branco
                    outline=False,  # Sem borda
                )
            ),
            dbc.Col(),
            dbc.Col(),
            dbc.Col()
        ]),
        dbc.Row()]

)