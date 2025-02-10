from dash import html, dcc, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import funcoes as fc
import datetime as dt
from dash import html, dcc

dataframe = pd.read_excel("banco de dados.xlsx", sheet_name="Banco de Dados")
dataframe['Movimentação']=dataframe['Depósito']-dataframe['Retiradas']
data = dt.datetime(2024, 1, 3)
nova_data = fc.mes_anterior(data)
dash_1 = dataframe.loc[(dataframe['Data'] == data)]
dataframe['Data'] = dataframe["Data"].dt.strftime('%m/%Y')
dash_1 = dash_1.sort_values(['Saldo', 'Banco'])
ultimo_dado=dataframe['Data'].iloc[-1]
Saldo=dataframe['Saldo'].loc[(dataframe['Data'] == ultimo_dado)].sum()

layout = html.Div  ([
    html.H1('Página 2'),
    html.P('Este é a página 2'),
    dcc.Link('Ir para inicio', href ='/')
])



fig = px.bar(dash_1, x="Data", y="Saldo", color="Investimento", barmode="group", width=800, height=400)
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
    plot_bgcolor='rgba(0,0,0,0)',   # Fundo da área de plotagem transparente
)

investimentos = list(dataframe["Investimento"].unique())

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("Conteúdo Principal", className='intra_pagina'),
                html.P(f"o saldo é de R${Saldo:.2f}", className='intra_pagina'),
                html.Div(
                    style={
                        'display': 'grid',
                        'gridTemplateColumns': '200px 1fr',  # Dropdown com 200px, gráfico ocupa o restante
                        'gap': '20px',  # Espaçamento entre os elementos
                    },
                    children=[
                        dcc.Dropdown(
                            investimentos,
                            value='CDB',
                            id='entrada-investimentos',
                            className='dropdown-transparente',
                        ),
                        dcc.Graph(
                            id='grafico1',
                            figure=fig,
                            className='grafico',
                        )
                    ]
                )
            ]
        )
    ]
)

@callback(
    Output('grafico1', 'figure'),
    Input('entrada-investimentos', 'value')
)
def update_output(value):
    if value == 'Todos os Investimentos':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dataframe['Data'],
            y=dataframe['Saldo'],
            name='Saldo',
            mode='lines',
            line=dict(color='#e87722', width=2),
            yaxis='y1'
        ))
        fig.add_trace(go.Bar(
            x=dataframe['Data'],
            y=dataframe['Movimentação'],
            name='Vendas',  # Nome da série na legenda
            marker_color='blue'  # Cor das barras
        ))
        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
                            plot_bgcolor='rgba(0,0,0,0)',   # Fundo da área de plotagem transparente
                            width=800,  # Largura do gráfico em pixels
                            height=500  # Altura do gráfico em pixels
        )
    else:
        tabela_filtrada = dataframe.loc[dataframe['Investimento'] == value, :]
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
            plot_bgcolor='rgba(0,0,0,0)',   # Fundo da área de plotagem transparente
            width=800,  # Largura do gráfico em pixels
            height=500,  # Altura do gráfico em pixels
            title=f'Evolução do {value}',
            xaxis=dict(title="Data"),
            yaxis=dict(
                title='Crescimento (%)',
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue'),
                tickformat='0.00%',
                showgrid=False
            ),
            yaxis2=dict(
                title='saldo e movimentação',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.1, y=1.1)
        )
    return fig
